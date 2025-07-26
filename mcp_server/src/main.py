from fastmcp import FastMCP
from typing import List, Optional, Dict
import hue
import os
from datetime import datetime
from helpers import rgb_to_hue_state
from starlette.responses import JSONResponse


mcp = FastMCP(
    name="phillips-hue-mcp-server",
    instructions="A server for controlling Phillips Hue lights and managing room configurations."
)


@mcp.custom_route("/mcp/", methods=["GET"])
async def mcp_probe(request):
    # Let Inspector connect even if it doesn't accept SSE
    return JSONResponse(content={"ok": True})


@mcp.tool()
def set_room_lights(
    room: str,
    on: Optional[str] = None,
    red: Optional[str] = None,
    green: Optional[str] = None,
    blue: Optional[str] = None
) -> Dict:
    """Set all lights in a room to a given state (on/off, color). Use RGB values (0-255) for color."""
    groups = hue.get_groups()
    for gid, g in groups.items():
        if g.get("type") == "Room" and g.get("name", "").lower() == room.lower():
            # Convert RGB to Hue state
            if red is not None and green is not None and blue is not None:
                # Convert string RGB values to integers
                r = int(red) if isinstance(red, str) else red
                g = int(green) if isinstance(green, str) else green
                b = int(blue) if isinstance(blue, str) else blue
                action = rgb_to_hue_state(r, g, b, on=True if on is None else on.lower() in ['true', '1', 'yes', 'on'])
            else:
                # Just set on/off without changing color
                action = {"on": on.lower() in ['true', '1', 'yes', 'on'] if on is not None else True}
            return hue.set_group_action(gid, action)
    return {"error": f"Room '{room}' not found"}

@mcp.tool()
def set_light_state(
    light_id: str,
    on: Optional[str] = None,
    red: Optional[str] = None,
    green: Optional[str] = None,
    blue: Optional[str] = None
) -> Dict:
    """Set a specific light to a given state by its ID. Use RGB values (0-255) for color."""
    # Convert RGB to Hue state
    if red is not None and green is not None and blue is not None:
        # Convert string RGB values to integers
        r = int(red) if isinstance(red, str) else red
        g = int(green) if isinstance(green, str) else green
        b = int(blue) if isinstance(blue, str) else blue
        state = rgb_to_hue_state(r, g, b, on=True if on is None else on.lower() in ['true', '1', 'yes', 'on'])
    else:
        # Just set on/off without changing color
        state = {"on": on.lower() in ['true', '1', 'yes', 'on']} if on is not None else {}
    return hue.set_light_state(light_id, state)


@mcp.tool()
def get_lights() -> Dict:
    """Get all lights with their current states and names. 
    Note: This was originally a resource but converted back to tool because Claude Desktop UI isn't intuitive with resources."""
    return hue.get_lights()


@mcp.tool()
def get_rooms() -> Dict:
    """Get all rooms (groups of type 'Room') with their light configurations. 
    Note: This was originally a resource but converted back to tool because Claude Desktop UI isn't intuitive with resources."""
    groups = hue.get_groups()
    return {gid: g for gid, g in groups.items() if g.get("type") == "Room"}


@mcp.tool()
def get_server_status() -> Dict:
    """Get the current status of the Phillips Hue MCP server. 
    Note: This was originally a resource but converted back to tool because Claude Desktop UI isn't intuitive with resources."""
    return {
        "status": "running",
        "service": "phillips-hue-mcp-server",
        "timestamp": datetime.now().isoformat(),
        "hue_bridge_ip": os.environ.get("HUE_BRIDGE_IP", "not_set"),
        "hue_username": os.environ.get("HUE_USERNAME", "not_set"),
        "auth_required": False,
        "auth_provider": "None"
    }


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

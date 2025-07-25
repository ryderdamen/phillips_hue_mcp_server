from mcp.server.fastmcp import FastMCP
from typing import List, Optional
import hue
from fastapi import Depends
from authentication import verify_google_token
import os


mcp = FastMCP(name="hue_bridge", host="0.0.0.0", port=8000)
app = mcp.app


@app.get("/.well-known/oauth-protected-resource")
def oauth_metadata():
    return {
        "issuer": "https://accounts.google.com",
        "authorization_server": "https://accounts.google.com",
        "resource": os.environ['TAILSCALE_FUNNEL_URL'],
        "scopes": {
            "openid": "Basic identity",
            "email": "User email"
        }
    }


@mcp.tool()
def list_lights(user=Depends(verify_google_token)) -> dict:
    """List all lights with their names and IDs."""
    return hue.get_lights()


@mcp.tool()
def get_rooms(user=Depends(verify_google_token)) -> dict:
    """List all rooms (groups of type 'Room') and their light IDs."""
    groups = hue.get_groups()
    return {gid: g for gid, g in groups.items() if g.get("type") == "Room"}


@mcp.tool()
def set_room_lights(
    room: str,
    on: bool,
    hue_value: Optional[int] = None,
    sat: Optional[int] = None,
    bri: Optional[int] = None,
    user=Depends(verify_google_token)
) -> dict:
    """Set all lights in a room to a given state (on/off, color, brightness)."""
    groups = hue.get_groups()
    for gid, g in groups.items():
        if g.get("type") == "Room" and g.get("name", "").lower() == room.lower():
            action = {"on": on}
            if hue_value is not None:
                action["hue"] = hue_value
            if sat is not None:
                action["sat"] = sat
            if bri is not None:
                action["bri"] = bri
            return hue.set_group_action(gid, action)
    return {"error": f"Room '{room}' not found"}


@mcp.tool()
def set_named_lights_in_room(
    room: str,
    name_query: str,
    on: Optional[bool] = None,
    hue_value: Optional[int] = None,
    sat: Optional[int] = None,
    bri: Optional[int] = None,
    user=Depends(verify_google_token)
) -> dict:
    """Set lights in a room whose name matches name_query (case-insensitive substring) to a given state."""
    groups = hue.get_groups()
    lights = hue.get_lights()
    for gid, g in groups.items():
        if g.get("type") == "Room" and g.get("name", "").lower() == room.lower():
            results = {}
            for lid in g.get("lights", []):
                lname = lights.get(lid, {}).get("name", "")
                if name_query.lower() in lname.lower():
                    state = {}
                    if on is not None:
                        state["on"] = on
                    if hue_value is not None:
                        state["hue"] = hue_value
                    if sat is not None:
                        state["sat"] = sat
                    if bri is not None:
                        state["bri"] = bri
                    results[lid] = hue.set_light_state(lid, state)
            return results
    return {"error": f"Room '{room}' not found"}


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

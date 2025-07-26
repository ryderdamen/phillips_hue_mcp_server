from fastmcp import FastMCP
from typing import List, Optional, Dict
import hue
import os
from datetime import datetime
from oauth import require_auth, create_oauth_metadata
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware


# Create MCP server
mcp = FastMCP(
    name="phillips-hue-mcp-server",
    instructions="A server for controlling Phillips Hue lights and managing room configurations. Requires Google OAuth authentication."
)

# Add OAuth metadata endpoint
@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET", "OPTIONS"])
async def oauth_metadata(request):
    """Return OAuth metadata for client configuration."""
    if request.method == "OPTIONS":
        return JSONResponse(content={}, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        })
    return JSONResponse(content=create_oauth_metadata(), headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })

@mcp.custom_route("/.well-known/oauth-authorization-server", methods=["GET", "OPTIONS"])
async def oauth_authorization_server(request):
    """Return OAuth authorization server metadata for client discovery."""
    if request.method == "OPTIONS":
        return JSONResponse(content={}, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        })
    return JSONResponse(content={
        "issuer": "https://accounts.google.com",
        "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_endpoint": "https://oauth2.googleapis.com/token",
        "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
        "response_types_supported": ["code"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"],
        "scopes_supported": ["openid", "email", "profile"],
        "registration_endpoint": None  # Google doesn't support dynamic registration
    }, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })

@mcp.custom_route("/oauth/callback", methods=["GET", "OPTIONS"])
async def oauth_callback(request):
    """Handle OAuth callback from Google."""
    if request.method == "OPTIONS":
        return JSONResponse(content={}, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        })
    
    # For now, just return a success message
    # In a full implementation, you'd exchange the code for tokens here
    return JSONResponse(content={
        "status": "success",
        "message": "OAuth callback received. Please configure your client with the Google OAuth client credentials."
    }, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })


@mcp.custom_route("/mcp/", methods=["GET"])
async def mcp_probe(request):
    # Let Inspector connect even if it doesn't accept SSE
    return JSONResponse(content={"ok": True})

@mcp.tool()
@require_auth
def list_lights() -> Dict:
    """List all lights with their names and IDs. Requires Google OAuth authentication."""
    return hue.get_lights()

@mcp.tool()
@require_auth
def get_rooms() -> Dict:
    """List all rooms (groups of type 'Room') and their light IDs. Requires Google OAuth authentication."""
    groups = hue.get_groups()
    return {gid: g for gid, g in groups.items() if g.get("type") == "Room"}

@mcp.tool()
@require_auth
def set_room_lights(
    room: str,
    on: bool,
    hue_value: Optional[int] = None,
    sat: Optional[int] = None,
    bri: Optional[int] = None
) -> Dict:
    """Set all lights in a room to a given state (on/off, color, brightness). Requires Google OAuth authentication."""
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
@require_auth
def set_named_lights_in_room(
    room: str,
    name_query: str,
    on: Optional[bool] = None,
    hue_value: Optional[int] = None,
    sat: Optional[int] = None,
    bri: Optional[int] = None
) -> Dict:
    """Set lights in a room whose name matches name_query (case-insensitive substring) to a given state. Requires Google OAuth authentication."""
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

@mcp.tool()
@require_auth
def set_light_state(
    light_id: str,
    on: Optional[bool] = None,
    hue_value: Optional[int] = None,
    sat: Optional[int] = None,
    bri: Optional[int] = None
) -> Dict:
    """Set a specific light to a given state by its ID. Requires Google OAuth authentication."""
    state = {}
    if on is not None:
        state["on"] = on
    if hue_value is not None:
        state["hue"] = hue_value
    if sat is not None:
        state["sat"] = sat
    if bri is not None:
        state["bri"] = bri
    return hue.set_light_state(light_id, state)

@mcp.tool()
def get_server_status() -> Dict:
    """Get the current status of the Phillips Hue MCP server. No authentication required."""
    return {
        "status": "running",
        "service": "phillips-hue-mcp-server",
        "timestamp": datetime.now().isoformat(),
        "hue_bridge_ip": os.environ.get("HUE_BRIDGE_IP", "not_set"),
        "hue_username": os.environ.get("HUE_USERNAME", "not_set"),
        "auth_required": True,
        "auth_provider": "Google OAuth"
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

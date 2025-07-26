# Phillips Hue MCP Server
A deployable MCP server, that allows for control of Phillips Hue lights on your LAN.

**Note:** This is a proof of concept, and is not yet tested with an actual Hue system - only a mocked system.

## Local Development
To run the mock server and the MCP server, use the following command:
```sh
make run
```

Debugging can be done with MCP inspector
```sh
npx @modelcontextprotocol/inspector
```

And the full implementation can be tested with Claude Desktop, by updating the developer MCP config file.
```json
{
    "mcpServers": {
      "phillips-hue": {
        "command": "npx",
        "args": [
          "mcp-remote",
          "http://localhost:8000/mcp/",
          "--allow-http"
        ]
      }
    }
  }
   
```

## Examples of things you can say

> Turn off all the lights in the living room.

> Which lights are on in the bedroom?

> Set all the floor lamps to red

---

## Future
- Authentication
    - OAuth based authentication/proxy, for limiting access to specific people
- Remote Access
    - Tailscale Funnel deployment, so you can control your lights away from home
- Managed MCP-Hue-Bridge Authentication
    - Currently the API / Authentication is mocked; I'd like to implement it properly
- Enhanced Features
    - Better scene management

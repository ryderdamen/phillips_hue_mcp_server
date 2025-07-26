# Phillips Hue MCP Server
A MCP server that lets you control a local phillips hue bridge, so you can control your lights more intuitively with ChatGPT or another public LLM.

## URL
The public URL for the MCP server is as follows.
```txt
https://ryders-macbook-pro.tail2b9210.ts.net/mcp/
```

## Architecture
A running server on your network, on a raspberry pi, with direct LAN access to the phillips hue bridge (mocked for this example). Exposed over the public web with tailscale funnel, and secured with OAuth using the newly developed standards for MCP, and Google as an identity provider.


## work in progress, because im at 4% battery, and there's a power outage. Not yet ready.

### to do
- test oauth logic
- test full implementation with chatgpt or another public LLM
- implement script for tailscale funnel setup, etc.
- implement more hue endpoionts to make sure i can capture every behaviour i want (turn on only the floor lamps in the kitchen, and set them to red, and make the ceiling ones green.)
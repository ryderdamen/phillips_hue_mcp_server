import asyncio
from fastmcp import Client

async def test():
    client = Client("http://localhost:8000/mcp")
    async with client:
        tools = await client.list_tools()
        print("Available tools:", [t.name for t in tools])

        result = await client.call_tool("list_lights", {})
        print("Result from list_lights:", result.content)

if __name__ == "__main__":
    asyncio.run(test())

"""A minimal MCP client: connect to the server, list its tools, call one.

Claude Code does exactly these steps for you. This file shows them in plain Python.
Usage: python client.py            (starts server.py itself over stdio)
       python client.py http://127.0.0.1:8000/mcp   (talks to a running HTTP server)
"""
import asyncio
import json
import sys

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters


async def main(target: str | None) -> None:
    server = target or StdioServerParameters(command=sys.executable, args=["server.py"])
    async with Client(server) as client:
        tools = await client.list_tools()
        for tool in tools.tools:
            print("TOOL", tool.name, "|", tool.description)
            print("  inputSchema:", json.dumps(tool.input_schema))
            print("  annotations:", tool.annotations.model_dump(exclude_none=True) if tool.annotations else None)
        result = await client.call_tool("add_note", {"text": "Ship the MCP server", "tag": "todo"})
        print("CALL add_note ->", result.content[0].text)
        result = await client.call_tool("search_notes", {"query": "mcp"})
        print("CALL search_notes ->", result.content[0].text)


asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else None))

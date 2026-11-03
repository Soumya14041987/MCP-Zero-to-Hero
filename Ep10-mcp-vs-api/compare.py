"""Side by side: what a caller must know in advance (REST) vs what it can ask (MCP).

Needs rest_api.py running on 8001. The MCP server is started by this script over stdio.
"""
import asyncio
import json
import sys
import urllib.error
import urllib.request

from mcp.client import Client
from mcp.client.stdio import StdioServerParameters


def rest_call(city: str):
    # The caller hard-codes the URL, the parameter name and the response shape.
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:8001/forecast?city={city}") as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.load(e)


async def main() -> None:
    print("== REST: you must already know the endpoint ==")
    print(rest_call("Kolkata"))
    print(rest_call("Delhi"))

    print("\n== MCP: ask the server what it can do ==")
    params = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])
    async with Client(params) as client:
        tools = await client.list_tools()
        for t in tools.tools:
            print("TOOL", t.name, "|", t.description)
            print("  inputSchema:", json.dumps(t.input_schema))
        ok = await client.call_tool("get_forecast", {"city": "Kolkata"})
        print("CALL ok  ->", ok.is_error, ok.content[0].text)
        bad = await client.call_tool("get_forecast", {"city": "Delhi"})
        print("CALL bad ->", bad.is_error, bad.content[0].text)


asyncio.run(main())

"""Check Blender MCP from outside Claude: list the tools, read the scene, add a cube.

Needs: Blender open with the addon server started, and `pip install "mcp>=1.26,<2"`.
Run:   python check_tools.py
"""
import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CUBE = "import bpy\nbpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))\nprint('cube added')"


async def main() -> None:
    env = dict(os.environ, DISABLE_TELEMETRY="true")
    params = StdioServerParameters(command="uvx", args=["mcp-for-blender"], env=env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("TOOLS", [t.name for t in tools.tools])
            for name, args in [("get_scene_info", {}), ("execute_blender_code", {"code": CUBE})]:
                result = await session.call_tool(name, args)
                print(f"\n{name} (isError={result.isError})")
                print("".join(c.text for c in result.content if hasattr(c, "text")))


asyncio.run(main())

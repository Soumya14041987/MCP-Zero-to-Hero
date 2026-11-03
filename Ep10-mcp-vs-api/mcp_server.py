"""The same forecast, exposed as an MCP tool. SDK 2.x (MCPServer).

Run over stdio: python mcp_server.py
Run over HTTP:  python mcp_server.py --http   -> http://127.0.0.1:8000/mcp
"""
import sys

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

FORECASTS = {"kolkata": 31, "mumbai": 33}
mcp = MCPServer("weather", instructions="Weather forecasts by city.")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def get_forecast(city: str) -> str:
    """Get today's temperature in Celsius for a city. Known cities: Kolkata, Mumbai."""
    temp = FORECASTS.get(city.lower())
    if temp is None:
        raise ToolError(f"Unknown city {city!r}. Try Kolkata or Mumbai.")
    return f"{city.title()}: {temp} C"


if __name__ == "__main__":
    mcp.run("streamable-http" if "--http" in sys.argv else "stdio")

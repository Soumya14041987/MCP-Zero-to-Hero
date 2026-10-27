"""Notes MCP server: three tools that save, list and search short notes in notes.json.

Run over stdio (Claude Code starts it for you):   python server.py
Run as an HTTP service (you start it yourself):  python server.py --http
"""
import json
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

STORE = Path(__file__).with_name("notes.json")
mcp = MCPServer(
    "notes",
    instructions="Personal notes. Use add_note to save, list_notes to browse, search_notes to find text.",
)


def _load() -> list[dict]:
    return json.loads(STORE.read_text()) if STORE.exists() else []


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def add_note(text: str, tag: str = "general") -> str:
    """Save a short note. Use a tag such as 'idea' or 'todo' to group notes."""
    notes = _load()
    notes.append({"id": len(notes) + 1, "tag": tag, "text": text})
    STORE.write_text(json.dumps(notes, indent=2))
    return f"Saved note {len(notes)} with tag '{tag}'"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_notes(tag: str | None = None) -> list[dict]:
    """List saved notes. Pass a tag to see only that tag."""
    return [n for n in _load() if tag is None or n["tag"] == tag]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search_notes(query: str) -> list[dict]:
    """Find notes whose text contains the query, ignoring case."""
    return [n for n in _load() if query.lower() in n["text"].lower()]


if __name__ == "__main__":
    mcp.run("streamable-http" if "--http" in sys.argv else "stdio")

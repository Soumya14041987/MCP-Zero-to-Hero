from mcp.server.mcpserver import MCPServer

mcp = MCPServer("notes")
NOTES: list[str] = []

@mcp.tool()
def add_note(text: str) -> str:
    """Save a short note."""
    NOTES.append(text)
    return f"Saved note {len(NOTES)}"

@mcp.tool()
def list_notes() -> list[str]:
    """Return every saved note."""
    return NOTES

if __name__ == "__main__":
    mcp.run()

MCP Zero to Hero: Study Notes

Notes, commands and architecture diagrams for the MCP Zero to Hero video series by Soumyadip Chatterjee.
Channel: https://www.youtube.com/@soumyadipchatterjee2267

Each episode has its own folder with a notes.md file. Diagrams are written in Mermaid, which GitHub renders directly in the browser.

Episodes

| Episode | Topic | Video | Notes |
|---|---|---|---|
| Ep1 | What is MCP? The 2026 update | https://www.youtube.com/watch?v=8BodrmxG5U0 | [Ep1-what-is-mcp](Ep1-what-is-mcp/notes.md) |
| Ep2 | The six MCP primitives | https://www.youtube.com/watch?v=Q3_SuoMzg4M | [Ep2-six-mcp-primitives](Ep2-six-mcp-primitives/notes.md) |
| Ep3 | N x M to 1, interoperability | https://www.youtube.com/watch?v=ymdCgRUyR1g | [Ep3-n-by-m-interoperability](Ep3-n-by-m-interoperability/notes.md) |
| Ep4 | Transport: stdio vs Streamable HTTP | https://www.youtube.com/watch?v=-kBbfsKatxI | [Ep4-transport-stdio-vs-streamable-http](Ep4-transport-stdio-vs-streamable-http/notes.md) |
| Ep5 | MCP tools in depth | https://www.youtube.com/watch?v=Q8binp4EQV8 | [Ep5-mcp-tools-in-depth](Ep5-mcp-tools-in-depth/notes.md) |
| Ep6 | Build your first MCP server in Python | https://www.youtube.com/watch?v=RGryq0Zt9og | [Ep6-build-first-mcp-server-python](Ep6-build-first-mcp-server-python/notes.md) |
| Ep7 | Connect any MCP server to Claude, Copilot, Cursor | https://www.youtube.com/watch?v=OA19pBHJUMg | [Ep7-connect-mcp-to-claude-copilot-cursor](Ep7-connect-mcp-to-claude-copilot-cursor/notes.md) |

Episode numbers follow the playlist publish order. More episodes will be added as the series continues.

Quick command cheat sheet

```bash
# Ep6: project setup and test
uv init mcp-demo && cd mcp-demo && uv venv
uv add "mcp[cli]"
uv run mcp dev server.py
uv run mcp run server.py --transport streamable-http

# Ep7: connect to Claude Code
claude mcp add --transport http NAME URL
claude mcp add --transport stdio NAME -- COMMAND ARGS
claude mcp list
```

Official references

- Model Context Protocol docs: https://modelcontextprotocol.io
- Specification: https://modelcontextprotocol.io/specification
- Python SDK: https://github.com/modelcontextprotocol/python-sdk

Source and accuracy

Notes were written from the video transcripts. Code in Ep6 is rebuilt from the on-screen steps described in the video, so check it against the current SDK README before relying on it.

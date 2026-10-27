Episode 9: Build a Custom MCP Server From Scratch and Run It in Claude Code (stdio and HTTP)

Video: (add the YouTube link after upload)
Tested on: Claude Code 2.1.311, MCP Python SDK 2.3.0, Python 3.11 or newer

Core idea: Claude Code is the host, and the MCP client lives inside it. Your server is a separate program. You will build one, run it over stdio and over HTTP, and see every message the client sends.

Folder contents: notes.md (this file), server.py (the notes server), client.py (a minimal MCP client), slow.py (a deliberately slow server for the timeout demo).

Step 0: Check your tools

```bash
python3 --version        # 3.11 or newer
claude --version         # Claude Code, 2.1.x was used here
```

Step 1: Folder, virtual environment, SDK

```bash
mkdir mcp-notes && cd mcp-notes
python3 -m venv .venv
.venv/bin/pip install mcp
.venv/bin/pip show mcp | head -2    # Version: 2.3.0 was used here
# copy server.py, client.py and slow.py from this folder into mcp-notes
```

SDK 2.x renamed FastMCP to MCPServer. The import from Episode 6 fails on 2.x with ModuleNotFoundError:

```python
# SDK 1.x (Episode 6)   from mcp.server.fastmcp import FastMCP
# SDK 2.x (this video)  from mcp.server.mcpserver import MCPServer
```

Claude Code only shows "Failed to connect: CONNECTION_CLOSED" in that case. The traceback is hidden, so run python server.py by hand when a server will not connect.

Step 2: Define a tool (server.py)

A tool is a Python function with the @mcp.tool() decorator.
- The function name becomes the tool name.
- The type hints become the inputSchema.
- The docstring becomes the description. The model reads only this, so write it for the model.
- annotations (readOnlyHint, destructiveHint) tell the client which tools are safe.
- MCPServer("notes", instructions=...) sends usage hints in the initialize result.

server.py has three tools: add_note, list_notes, search_notes. Notes are stored in notes.json next to server.py.

Step 3: Run it by hand over stdio and see the wire

MCP over stdio is JSON-RPC, one message per line. Send the three messages a client sends:

```bash
(printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"hand","version":"0"}}}' \
 '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add_note","arguments":{"text":"demo","tag":"demo"}}}'; sleep 2) \
 | .venv/bin/python server.py
```

The sleep keeps stdin open so the server can answer before it sees end of input.

What comes back:
1. initialize result: protocolVersion, capabilities, serverInfo, and your instructions.
2. tools/list result: for each tool, name, description, inputSchema, outputSchema and annotations.
3. tools/call result: content (a list of text blocks), isError (false) and structuredContent.

A tool that fails returns a normal result with isError true (Episode 8 covers this).

Step 4: A minimal client (client.py)

This is what Claude Code does for you, in plain Python:

```bash
.venv/bin/python client.py
```

Output (trimmed):

```
TOOL add_note | Save a short note. Use a tag such as 'idea' or 'todo' to group notes.
  inputSchema: {...}
  annotations: {'readOnlyHint': False, 'destructiveHint': False}
CALL add_note -> Saved note 1 with tag 'todo'
```

Where the client is: Claude Code (the host) holds one MCP client connection per server you add. Your server never talks to the model directly.

Step 5: Register with Claude Code over stdio

```bash
claude mcp add notes -- .venv/bin/python server.py
claude mcp list
# notes: .venv/bin/python server.py - √ Connected
claude mcp get notes
```

The two dashes separate Claude's own flags from your server's command. Claude Code records the absolute path of the command. Inside a Claude Code session, run /mcp to see the connection. The model sees each tool as mcp__notes__add_note (mcp__SERVER__TOOL).

Step 6: Deploy over HTTP

```bash
# terminal 1: you run the server (serves http://127.0.0.1:8000/mcp)
.venv/bin/python server.py --http

# terminal 2: register the URL
claude mcp add --transport http notes-http http://127.0.0.1:8000/mcp
claude mcp list
# notes-http: http://127.0.0.1:8000/mcp (HTTP) - √ Connected

# the same client works against the URL
.venv/bin/python client.py http://127.0.0.1:8000/mcp
```

Same server, same tools. With HTTP you can run it on another machine, and Claude Code only needs the URL. Add -H "Authorization: Bearer ..." to claude mcp add for a server that needs a header.

Step 7: Scopes

```bash
claude mcp add -s local   notes -- .venv/bin/python server.py   # default, private, this project
claude mcp add -s user    notes -- .venv/bin/python server.py   # all your projects
claude mcp add -s project notes -- .venv/bin/python server.py   # writes .mcp.json, shared through git
```

local and user entries live in ~/.claude.json. The project scope entry lives in .mcp.json in the repo. A project server shows "Pending approval (run claude to approve)" in claude mcp list until you approve it.

Step 8: The failure nobody shows, a slow start

```bash
claude mcp add slow -- .venv/bin/python slow.py     # sleeps 5 seconds before it starts
MCP_TIMEOUT=1000  claude mcp list   # × Failed to connect — MCP server "slow" connection timed out after 1000ms
MCP_TIMEOUT=15000 claude mcp list   # √ Connected
claude mcp remove slow
```

MCP_TIMEOUT is the server startup timeout in milliseconds. Two related settings exist, MCP_TOOL_TIMEOUT for slow tool calls and MAX_MCP_OUTPUT_TOKENS for big results. Their defaults and behaviour were not tested in this video, so check the Claude Code docs for your version.

Step 9: Share it with your team

```bash
claude mcp add -s project notes -- .venv/bin/python server.py
cat .mcp.json
```

The file records the absolute path of your Python. Before you commit, change it to one that works for your team. Undo with:

```bash
claude mcp remove -s project notes
claude mcp reset-project-choices
```

What was tested and what was not
- Tested: Steps 0 to 9, in a container with Claude Code 2.1.311 and mcp 2.3.0, using claude mcp add, list, get and remove.
- Not tested: using the tools inside a live Claude Code conversation (the container had no Claude login), so the mcp__notes__add_note name is how Claude Code names tools by documentation, not something captured from a session. MCP_TOOL_TIMEOUT and MAX_MCP_OUTPUT_TOKENS were not exercised.

Next: Episode 10.

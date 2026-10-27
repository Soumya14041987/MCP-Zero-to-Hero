Episode 9: Claude Code MCP, Ship Your Own Server End to End

Video: (add the YouTube link after upload)
Tested on: Claude Code 2.1.311, mcp Python SDK 2.3.0, MCP Inspector 2.12.0, Python 3.13, Node 22. Commands were run on Linux.

Core idea: a fresh install of the MCP Python SDK is now version 2. The `FastMCP` import used in Ep6 fails there, and Claude Code only reports "Failed to connect: CONNECTION_CLOSED" because the Python traceback stays hidden. Build with the new import, register the server after the `--`, pick the scope on purpose, verify with Inspector, then share `.mcp.json`.

Folder contents: notes.md (this file) and server.py (the notes server).

Step 0: Prerequisites

```bash
claude --version        # 2.1.x
python3 --version       # 3.10 or newer
node -v                 # 22.19 or newer, for the Inspector from Ep8
```

Step 1: Create the project and install the SDK

```bash
mkdir mcp-demo && cd mcp-demo
git init
python3 -m venv .venv
.venv/bin/pip install "mcp[cli]"
.venv/bin/pip show mcp | sed -n 2p      # Version: 2.x
```

With uv, as in Ep6: `uv init mcp-demo && cd mcp-demo && uv add "mcp[cli]"`. The registration commands below use `.venv/bin/python`; with uv use the path to its virtual environment's Python.

Step 2: See the failure (the old Ep6 import)

```bash
cat > server_old.py <<'PY'
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes")
PY

.venv/bin/python server_old.py
# ModuleNotFoundError: No module named 'mcp.server.fastmcp'.
# This is mcp 2.x, where FastMCP was renamed to MCPServer ...

claude mcp add notes-old -- "$PWD/.venv/bin/python" "$PWD/server_old.py"
claude mcp list
# notes-old: ... - × Failed to connect — CONNECTION_CLOSED: Connection closed
claude mcp remove notes-old
```

Claude Code shows only the connection error. The real traceback appears when you run the file yourself. If you must keep Ep6 code unchanged, pin the old SDK instead with `.venv/bin/pip install "mcp[cli]<2"` (not tested here).

Step 3: Build the server with the new import

Save `server.py` from this folder. It registers two tools, `add_note` and `list_notes`, using `from mcp.server.mcpserver import MCPServer`.

```bash
.venv/bin/python -c "import mcp.server.mcpserver as m; print('ok MCPServer')"
# ok MCPServer
```

Step 4: Register it with Claude Code (local scope, the default)

```bash
claude mcp add notes -- "$PWD/.venv/bin/python" "$PWD/server.py"
claude mcp list
# notes: ... - √ Connected
claude mcp get notes
# Scope: Local config (private to you in this project)
```

Everything after the two dashes belongs to your server's own command. Options meant for Claude (for example `-e KEY=value` or `-s project`) go before the two dashes.

Step 5: Scopes

| Scope | Flag | Who gets it |
|---|---|---|
| local | `-s local` (default) | You, in this project only |
| user | `-s user` | You, in every project |
| project | `-s project` | Everyone who has the repo, through `.mcp.json` |

```bash
claude mcp remove notes
claude mcp add -s project notes -- "$PWD/.venv/bin/python" "$PWD/server.py"
cat .mcp.json
claude mcp list
# notes: ... - ⏸ Pending approval (run `claude` to approve)
```

A project-scoped server is not connected until each person approves it inside Claude Code (run `claude`). Until then `claude mcp list` shows "Pending approval".

Step 6: Verify with MCP Inspector (Ep8)

```bash
npx -y @modelcontextprotocol/inspector --cli "$PWD/.venv/bin/python" "$PWD/server.py" --method tools/list
npx -y @modelcontextprotocol/inspector --cli "$PWD/.venv/bin/python" "$PWD/server.py" \
  --method tools/call --tool-name add_note --tool-arg text=hello
echo $?
# "text": "Saved note 1" ... "isError": false  and exit code 0
```

If Inspector passes and Claude Code still fails, the problem is the registration (path, scope or approval), not your server.

Step 7: Ship it to your team

`claude mcp add` records the absolute path of your machine in `.mcp.json`. Before you commit, replace both paths with ones that work for your team (for example a path every teammate creates the same way). Not tested here: relative paths in `.mcp.json`.

```bash
git add .mcp.json server.py
git commit -m "Add notes MCP server"
```

Step 8: Undo and reset

```bash
claude mcp remove -s project notes
claude mcp reset-project-choices
# Project-scoped (.mcp.json) server approvals and rejections stored for this project have been reset.
```

Not covered because it needs a logged-in Claude Code session: calling the tools from inside Claude Code (`/mcp`, then ask Claude to add a note). Registration, health and Inspector results above were all run.

Official reference: https://code.claude.com/docs/en/mcp

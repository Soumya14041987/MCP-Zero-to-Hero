# Ep 9 commands, step by step

Tested on Claude Code 2.1.311, MCP Python SDK 2.3.0, Python 3.11 or newer.

## Step 0: Check your tools

```bash
python3 --version
claude --version
```

## Step 1: Folder, virtual environment, SDK

```bash
mkdir mcp-notes && cd mcp-notes
python3 -m venv .venv
.venv/bin/pip install mcp
.venv/bin/pip show mcp | head -2
# copy server.py, client.py and slow.py from this folder into mcp-notes
```

## Step 2: Run the server by hand over stdio

```bash
(printf '%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"hand","version":"0"}}}' \
 '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
 '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add_note","arguments":{"text":"demo","tag":"demo"}}}'; sleep 2) \
 | .venv/bin/python server.py
```

## Step 3: Run the minimal client

```bash
.venv/bin/python client.py
```

## Step 4: Register with Claude Code over stdio

```bash
claude mcp add notes -- .venv/bin/python server.py
claude mcp list
claude mcp get notes
```

## Step 5: Deploy over HTTP

```bash
# terminal 1
.venv/bin/python server.py --http

# terminal 2
claude mcp add --transport http notes-http http://127.0.0.1:8000/mcp
claude mcp list
.venv/bin/python client.py http://127.0.0.1:8000/mcp
```

## Step 6: Scopes

```bash
claude mcp add -s local   notes -- .venv/bin/python server.py
claude mcp add -s user    notes -- .venv/bin/python server.py
claude mcp add -s project notes -- .venv/bin/python server.py
```

## Step 7: The slow-start failure

```bash
claude mcp add slow -- .venv/bin/python slow.py
MCP_TIMEOUT=1000  claude mcp list
MCP_TIMEOUT=15000 claude mcp list
claude mcp remove slow
```

## Step 8: Share it with your team

```bash
claude mcp add -s project notes -- .venv/bin/python server.py
cat .mcp.json
# edit the absolute Python path in .mcp.json before you commit
```

## Step 9: Clean up

```bash
claude mcp remove notes
claude mcp remove notes-http
claude mcp remove -s project notes
claude mcp reset-project-choices
```

Episode 10: MCP vs API

Tested on: MCP Python SDK 2.3.0 (protocol 2026-07-28), Python 3.13

Core idea: MCP does not replace your API. An API is a contract for a developer who reads docs at build time. An MCP tool is described for a model that discovers it at run time. Most MCP servers wrap an API.

Files: rest_api.py (REST, standard library only), mcp_server.py (same forecast as an MCP tool), compare.py (calls both), run-output.txt, wire-output.txt.

```bash
python3 -m venv .venv && .venv/bin/pip install mcp
.venv/bin/python rest_api.py &       # REST on 127.0.0.1:8001
.venv/bin/python compare.py          # REST call, then MCP tools/list, ok call, error call
```

Raw MCP over stdio, no handshake (spec 2026-07-28 removed initialize; each request carries _meta):

```bash
M='"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28","io.modelcontextprotocol/clientInfo":{"name":"hand","version":"0"},"io.modelcontextprotocol/clientCapabilities":{}}'
(printf '%s\n' "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\",\"params\":{$M}}"; sleep 2) | .venv/bin/python mcp_server.py
```

Older servers (spec 2025-11-25 and earlier) still need the initialize handshake shown in Episode 9.

Use ToolError (mcp.server.mcpserver.exceptions) to control the error text a model sees; any other exception is wrapped as "Error executing tool NAME: ...".

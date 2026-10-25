Episode 8: MCP Inspector, Debug Any MCP Server Before It Breaks Your Agent

Video: (add the YouTube link after upload)
Tested on: MCP Inspector 2.12.0, Node 22.19 or newer

Core idea: a tool call can return isError: true while the protocol log still shows OK. There are two failure layers, and the CLI exit codes let CI catch both.

Folder contents: notes.md (this file) and server.mjs (the tiny weather server used in the video).

Step 0: Check Node

```bash
node -v   # must be v22.19.0 or newer
```

Step 1: Set up the demo server

```bash
mkdir mcp-inspector-demo && cd mcp-inspector-demo
npm init -y
npm pkg set type=module
npm install @modelcontextprotocol/sdk zod
# save server.mjs from this folder next to package.json
```

server.mjs registers one tool, get_forecast. Kolkata and Pune return a temperature. Any other city returns isError: true with the text "Unknown city: <city>".

Step 2: Check the Inspector version

```bash
npx @modelcontextprotocol/inspector --version   # 2.12.0
```

Step 3: Web UI, explore

```bash
npx @modelcontextprotocol/inspector node server.mjs
```

The web server listens on port 6274. The old proxy on 6277 from version 1 is gone.
1. Open the printed URL, flip the connect switch.
2. The protocol panel shows initialize, the initialized notification and tools/list, each with its timing.
3. Tools tab, get_forecast, city = Kolkata, Execute. Result: Kolkata: 31°C.
4. Same tool, city = Delhi, Execute. The result panel says Tool Error, but the tools/call message in the protocol log still says OK.

Step 4: The two failure layers

| Layer | What you see | Meaning |
|---|---|---|
| Protocol error | JSON-RPC error object instead of a result | The request itself failed |
| Tool error | Normal result with isError: true | The request worked, the tool failed. By design, so the model can read the error and recover |

Step 5: CLI, for CI

```bash
# exit 0
npx @modelcontextprotocol/inspector --cli node server.mjs \
  --method tools/call --tool-name get_forecast --tool-arg city=Kolkata

# exit 5, one line JSON error on stderr
npx @modelcontextprotocol/inspector --cli node server.mjs \
  --method tools/call --tool-name get_forecast --tool-arg city=Delhi
echo $?

# exit 4, unreachable
npx @modelcontextprotocol/inspector --cli \
  --server-url http://127.0.0.1:9/mcp --method tools/list
echo $?
```

Exit codes: 0 success, 1 usage error, 2 no MCP App, 3 auth required, 4 unreachable, 5 tool error or tool not found.

In version 1 a failed tool call exited 0, so CI walked past it. Version 2 exits 5 and stops the pipeline.

Step 6: JSON output and strict mode

```bash
npx @modelcontextprotocol/inspector --cli node server.mjs \
  --method tools/call --tool-name get_forecast --tool-arg city=Kolkata \
  --format json | jq .

npx @modelcontextprotocol/inspector --cli node server.mjs \
  --method tools/list --strict
```

--format json gives machine readable output to assert on with jq. --strict flags tool schemas that some clients will reject.

Step 7: Secrets in containers

The Inspector keeps OAuth tokens and server env values in the OS keychain. With no keychain, such as in a container, it writes them to an unencrypted file at ~/.mcp-inspector/secrets.json. In CI, use one of:

```bash
export MCP_INSPECTOR_SECRET_STORE=memory
# or encrypt the file
export MCP_INSPECTOR_SECRET_KEY="<a long random value>"
```

Step 8: Web UI or CLI?

The web UI decides what is actually happening, message by message. The CLI decides whether the build passes. Debug in the web UI, guard every release with the CLI.

Next: Episode 9, Claude Code MCP: ship your own server end to end.

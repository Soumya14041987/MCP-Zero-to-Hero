# MCP Security and Governance: study notes

Notes and code for the video "MCP Security Explained: Tool Poisoning, Rug Pulls and How to Stop Them" (video link will be added after upload).

Channel: https://www.youtube.com/@soumyadipchatterjee2267

## What is in this folder

| File | What it is | Tested |
|---|---|---|
| notes.md | These notes | n/a |
| tool_pin.py | Saves a hash of every MCP tool definition and fails when one changes, appears or disappears (rug pull check) | Yes, ran locally |
| test.sh | Runs tool_pin.py on the two sample files | Yes |
| tools_v1.json | Sample tools/list result with 2 tools | Yes |
| tools_v2_changed.json | Same tools, with one sentence added to the read_logs description | Yes |
| tools_v3_duplicate.json | Two tools with the same name, to show duplicates are rejected | Yes |
| run-output.txt | The real output of test.sh | Yes |
| managed-settings.sample.json | Sample Claude Code managed MCP settings | JSON is valid, behaviour not tested |
| agentcore-policy.cedar.example | Example Cedar policy idea for AgentCore Gateway | Example only, not run |

## The running example

A DevOps incident agent reads logs and restarts pods through MCP servers. Three questions decide MCP security:

1. Which servers may the agent trust?
2. Who is the agent acting as?
3. What is each tool allowed to do?

Why it matters: the model reads every tool description as part of its instructions, so a tool is text the agent will follow, and one bad tool can reach everything the agent can reach (the blast radius).

## Attacks to know

- Tool poisoning: hidden instructions inside a tool description.
- Rug pull: a server is approved, then changes its tools later.
- Confused deputy: a server with more power acts for a caller who was never allowed. The MCP specification discusses this for servers that sit in front of third party APIs.

These are described as classes of attack. No incident numbers are used. The tool poisoning and rug pull descriptions come from research papers and security vendor write-ups that I did not read in full, so treat them as background.

## Controls, checked against the official pages (read on 2026-11-11)

1. Allowlist. In Claude Code, `allowedMcpServers` together with `allowManagedMcpServersOnly: true` in a managed settings source makes the allowlist authoritative. Without the flag, allowlists from user and project settings merge and can broaden it. `managed-mcp.json` deploys a fixed set of servers. Source: https://code.claude.com/docs/en/managed-mcp
2. Least privilege. Give each server only the tools the job needs. Codex can allow and deny tools per server with `enabled_tools` and `disabled_tools` in `~/.codex/config.toml` (project `.codex/config.toml` only for trusted projects). Source: https://developers.openai.com/codex/mcp
3. Identity. MCP servers act as OAuth 2.1 resource servers and must publish Protected Resource Metadata (RFC 9728). A server must validate that a token was issued for it as the audience and reject others. Token passthrough, forwarding a client token to another service, is explicitly forbidden. Source: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization and the security best practices page next to it.
4. Approval and audit. Ask a human before risky tools and log every tool call. This is practice advice, not a spec requirement.
5. Gateway and policy. With Amazon Bedrock AgentCore, a Policy attached to a Gateway blocks everything by default, and the policy engine enforces default deny and forbid wins. Sources: https://aws.amazon.com/blogs/security/why-policy-in-amazon-bedrock-agentcore-chose-cedar-for-securing-agentic-workflows/ and the AgentCore developer guide on policy concepts.

## What changed in the spec (from the official changelogs)

| Revision | Authorization change |
|---|---|
| 2025-03-26 | Added an authorization framework based on OAuth 2.1 |
| 2025-06-18 | Servers classified as OAuth resource servers, protected resource metadata added, resource indicators (RFC 8707) required, security best practices page added |
| 2025-11-25 | OpenID Connect discovery, Client ID Metadata Documents added as the recommended client registration method |
| 2026-07-28 | Dynamic Client Registration deprecated, client credentials bound to the authorization server that issued them |

Changelog pages: https://modelcontextprotocol.io/specification/2025-03-26/changelog (and the same path for 2025-06-18, 2025-11-25, 2026-07-28).

## The rug pull check

`tool_pin.py` reads a JSON file shaped like an MCP `tools/list` result, hashes each whole tool definition (name, description, input schema), and compares with the hashes saved at approval time.

Run it:

```bash
./test.sh
```

Output I got (see run-output.txt):

```
approved 2 tools
PASS (2 tools match the approved pins)
CHANGED tool definition: read_logs
FAIL
test ok: change was caught
DUPLICATE tool name(s): read_logs
FAIL
test ok: duplicate tool name was rejected
```

Use it on your own server:

```bash
python3 tool_pin.py approve my-tools.json pins.json   # when you approve the server
python3 tool_pin.py check my-tools.json pins.json     # before every run, exit code 1 on any change
```

It also refuses a tools list where two tools share a name, because a second definition could hide behind an approved name.

Limits: it checks files you give it, not a live server, and it cannot tell whether a change is harmful, only that something changed.

## Not done

- The managed settings sample and the Cedar example were not run against a real Claude Code install or a real AgentCore Gateway. Action and resource names in the Cedar file are placeholders.
- Codex was read from the official docs only, not tested.
- Claude Code's prompt behaviour for servers defined in a project `.mcp.json` was not verified.

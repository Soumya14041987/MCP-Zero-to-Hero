Episode 10: How to Install Blender MCP (control 3D scenes with Claude)

Tested on: mcp-for-blender 2.2.6 (PyPI, formerly blender-mcp), Blender 5.2.3 LTS (bpy module), uv 0.11, Claude Code 2.1.317, Python 3.11
Source: https://github.com/ahujasid/blender-mcp (MIT, third party, not made by Blender)

Core idea: two parts. The Blender addon runs a socket server inside Blender (localhost:9876). The MCP server (uvx mcp-for-blender) talks to Claude on one side and to that socket on the other.

Needs: Blender 3.0 or newer, Python 3.10 or newer, uv (use the official installer, not pip install uv).

Step 1: Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # Linux
brew install uv                                     # macOS
winget install --id=astral-sh.uv -e                 # Windows
```

Step 2: Add the MCP server to Claude

```bash
claude mcp add blender -e DISABLE_TELEMETRY=true -- uvx mcp-for-blender   # Claude Code
claude mcp list                                                           # blender: ... Connected
```

Claude Desktop: Settings, Developer, Edit Config, then paste claude_desktop_config.json from this folder. Fully quit and reopen Claude Desktop (Windows: quit from the system tray).

Step 3: Install the Blender addon

```bash
uvx mcp-for-blender install-addon
```

In Blender: Edit, Preferences, Add-ons, enable "Interface: MCP for Blender". Press N in the 3D viewport, open the MCP for Blender tab, click Start MCP Server.

Step 4: Check it from a script

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp>=1.26,<2"
.venv/bin/python check_tools.py        # prints the nine tools, the scene, then adds a cube
```

run-output.txt is the output from the test run.

When it does not work
- spawn uvx ENOENT in Claude Desktop: use the full path from `which uvx` as the command, then fully quit and reopen.
- "Could not connect to Blender. Make sure the Blender addon is running." comes back as normal text with isError false. Start the server in the Blender panel.
- Only run one MCP server instance at a time.
- Old cached package: `uv cache clean mcp-for-blender blender-mcp`.

Safety
- execute_blender_code runs any Python in Blender. Save your work first.
- The addon socket has no authentication. Keep it on localhost.
- Safe mode: BLENDER_MCP_SAFE_MODE=1 (see claude_desktop_config.safe-mode.json). Tested: with it on, os.system is blocked with an explanation; with it off, the same script runs.
- Telemetry: a minimal anonymous usage record is sent by default. DISABLE_TELEMETRY=true turns it off. Prompts, code and screenshots are opt-in only.

What was tested and what was not
- Tested: pip and uv install of mcp-for-blender 2.2.6, claude mcp add, list and remove, install-addon to a scratch folder (the file equals the repo addon.py), the addon server and MCP server end to end in Blender 5.2.3 run as a Python module (get_addon_status, get_scene_info, execute_blender_code), the Could not connect text, safe mode on and off.
- Not tested: the Blender graphical interface (no Blender app in the container), Claude Desktop, Windows and macOS paths, the curl-to-sh and PowerShell installers, uvx mcp-for-blender setup, asset and 3D generation services, the look tool (needs a viewport).
- The test ran the addon server class through a small harness because there is no Blender GUI to click Start MCP Server. The harness is not part of this folder.

Next: Episode 11.

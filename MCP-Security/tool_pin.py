#!/usr/bin/env python3
"""Pin MCP tool definitions by hash and fail when they change (rug pull check).

Input is a JSON file shaped like the result of an MCP tools/list call:
{"tools": [{"name": "...", "description": "...", "inputSchema": {...}}]}

Usage:
  tool_pin.py approve TOOLS.json PINS.json   record a hash per tool
  tool_pin.py check   TOOLS.json PINS.json   exit 1 if a tool changed, was added or was removed
"""
import hashlib
import json
import sys


def fingerprint(tool):
    # Hash the whole definition, not only the description, so schema changes are caught too.
    canonical = json.dumps(tool, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def load_tools(path):
    with open(path) as f:
        return {t["name"]: fingerprint(t) for t in json.load(f)["tools"]}


def main(argv):
    if len(argv) != 4 or argv[1] not in ("approve", "check"):
        print(__doc__)
        return 2
    mode, tools_path, pins_path = argv[1:]
    current = load_tools(tools_path)
    if mode == "approve":
        with open(pins_path, "w") as f:
            json.dump(current, f, indent=2, sort_keys=True)
        print(f"approved {len(current)} tools")
        return 0
    with open(pins_path) as f:
        pinned = json.load(f)
    problems = []
    for name, digest in current.items():
        if name not in pinned:
            problems.append(f"NEW tool not approved: {name}")
        elif pinned[name] != digest:
            problems.append(f"CHANGED tool definition: {name}")
    for name in pinned:
        if name not in current:
            problems.append(f"REMOVED tool: {name}")
    if problems:
        print("\n".join(problems))
        print("FAIL")
        return 1
    print(f"PASS ({len(current)} tools match the approved pins)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

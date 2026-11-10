#!/usr/bin/env bash
# Local test of tool_pin.py. Expected: approve ok, same file PASS, changed file FAIL, duplicate name FAIL (exit 1).
set -u
cd "$(dirname "$0")"
PIN=$(mktemp)
python3 tool_pin.py approve tools_v1.json "$PIN" || exit 1
python3 tool_pin.py check tools_v1.json "$PIN" || { echo "UNEXPECTED: unchanged file failed"; exit 1; }
if python3 tool_pin.py check tools_v2_changed.json "$PIN"; then
  echo "UNEXPECTED: changed file passed"; exit 1
else
  echo "test ok: change was caught"
fi
if python3 tool_pin.py check tools_v3_duplicate.json "$PIN"; then
  echo "UNEXPECTED: duplicate tool name passed"; exit 1
else
  echo "test ok: duplicate tool name was rejected"
fi
rm -f "$PIN"

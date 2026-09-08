#!/usr/bin/env python3
"""Compare the MCP tools the skills document against the tools the server has.

In September 2026 four tools that had never existed were documented in
linkedin-analytics for months. This is the check that would have caught it the
week it happened.

Needs PUBLORA_DRIFT_KEY: a Starter-plan key with no connected accounts, because
this only ever calls initialize and tools/list.

Usage: PUBLORA_DRIFT_KEY=sk_... python3 scripts/check_mcp_drift.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MCP = "https://mcp.publora.com"
PROTOCOL = "2025-03-26"

# A "### tool_name" heading in a skill is a claim that the tool exists.
HEADING = re.compile(r"^#{3}\s+([a-z][a-z0-9_]*)\s*$", re.M)


def rpc(key: str, method: str, params: dict, session: str | None = None):
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session:
        headers["mcp-session-id"] = session
    req = urllib.request.Request(
        MCP,
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode(),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        session_id = resp.headers.get("mcp-session-id")
        body = resp.read().decode()
    # The server may answer as JSON or as a text/event-stream frame.
    frames = [line[6:] for line in body.splitlines() if line.startswith("data: ")]
    return json.loads(frames[-1] if frames else body), session_id


def live_tools(key: str) -> set[str]:
    _, session = rpc(key, "initialize", {
        "protocolVersion": PROTOCOL,
        "capabilities": {},
        "clientInfo": {"name": "publora-skills-drift-check", "version": "1"},
    })
    payload, _ = rpc(key, "tools/list", {}, session)
    return {t["name"] for t in payload["result"]["tools"]}


def documented() -> dict[str, list[str]]:
    claims: dict[str, list[str]] = {}
    for skill in sorted(SKILLS.glob("*/SKILL.md")):
        for name in HEADING.findall(skill.read_text(encoding="utf-8")):
            claims.setdefault(name, []).append(skill.parent.name)
    return claims


def main() -> int:
    key = os.environ.get("PUBLORA_DRIFT_KEY")
    if not key:
        print("PUBLORA_DRIFT_KEY is not set; skipping drift check.", file=sys.stderr)
        return 0

    live = live_tools(key)
    claims = documented()

    # Only headings that look like MCP tool names are claims about the server.
    # Everything else in a skill is prose, so ignore unknown words unless they
    # share a prefix with a real tool family.
    families = tuple(sorted({t.split("_")[0] + "_" for t in live}))
    relevant = {n: s for n, s in claims.items() if n in live or n.startswith(families)}

    phantom = {n: s for n, s in relevant.items() if n not in live}
    uncovered = sorted(live - set(relevant))

    if uncovered:
        print("Live tools no skill mentions (not fatal):")
        for name in uncovered:
            print(f"  {name}")
        print()

    if phantom:
        print("Documented tools that DO NOT EXIST on the MCP server:")
        for name, skills in sorted(phantom.items()):
            print(f"  {name}  <- {', '.join(skills)}")
        return 1

    print(f"OK: every documented MCP tool exists ({len(live)} live tools).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

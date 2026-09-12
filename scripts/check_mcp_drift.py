#!/usr/bin/env python3
"""Compare what the skills document against what the MCP server actually has.

Two classes of drift, both of which shipped to users in 2026:

* a tool that does not exist. Four were documented in linkedin-analytics for
  months before anyone called one.
* a tool that exists, documented with parameters it does not take.
  `linkedin_create_reshare` was documented with `postedId` when it requires
  `parent`, so every reshare an agent attempted failed validation. The
  existence check passed clean on that for as long as it was wrong.

Needs PUBLORA_DRIFT_KEY: a Starter-plan key with no connected accounts, because
this only ever calls initialize and tools/list.

Usage: PUBLORA_DRIFT_KEY=sk_... python3 scripts/check_mcp_drift.py
"""

from __future__ import annotations

import argparse
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

# Cloudflare rejects the default urllib user agent with a 1010, so the check
# would fail every Monday with an opaque 403. Do not remove this.
USER_AGENT = "publora-skills-drift-check/1 (+https://github.com/publora/skills)"

# A "### tool_name" heading in a skill is a claim that the tool exists. Skills
# also group related tools in one heading, so split on "/" and judge each part.
HEADING = re.compile(r"^#{3}\s+(.+?)\s*$", re.M)
# Under a tool heading, "- `name`: ..." bullets are claims about its parameters.
# Only the FIRST backtick on a bullet is the parameter: a description may name
# another one deliberately ("takes `parent`, not `postedId`").
PARAM_BULLET = re.compile(r"^[-*]\s+`([A-Za-z_][A-Za-z0-9_]*)`", re.M)
# Every real tool is snake_case with at least one underscore, which is also what
# separates a tool claim from an ordinary prose heading.
TOOL_NAME = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")


def rpc(key: str, method: str, params: dict, session: str | None = None):
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": USER_AGENT,
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


def live_tools(key: str) -> list[dict]:
    _, session = rpc(key, "initialize", {
        "protocolVersion": PROTOCOL,
        "capabilities": {},
        "clientInfo": {"name": "publora-skills-drift-check", "version": "1"},
    })
    payload, _ = rpc(key, "tools/list", {}, session)
    return payload["result"]["tools"]


def documented() -> dict[str, list[str]]:
    """Every tool name claimed by a heading, mapped to the skills claiming it."""
    claims: dict[str, list[str]] = {}
    for skill in sorted(SKILLS.glob("*/SKILL.md")):
        for heading in HEADING.findall(skill.read_text(encoding="utf-8")):
            for part in heading.split("/"):
                name = part.strip()
                if TOOL_NAME.match(name):
                    claims.setdefault(name, []).append(skill.parent.name)
    return claims


def documented_params() -> dict[tuple[str, str], set[str]]:
    """Parameter names each skill documents per tool, keyed by (skill, tool).

    Only a heading naming exactly one tool is used: a combined heading such as
    "list_posts / get_post" has no single parameter list to attribute.
    """
    out: dict[tuple[str, str], set[str]] = {}
    for skill in sorted(SKILLS.glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        headings = list(HEADING.finditer(text))
        for i, h in enumerate(headings):
            tool = h.group(1).strip()
            if not TOOL_NAME.match(tool):
                continue
            body = text[h.end():headings[i + 1].start() if i + 1 < len(headings) else len(text)]
            marker = body.find("**Parameters:**")
            if marker == -1:
                continue
            block = body[marker:]
            # stop at the next bold heading, so a later section is not absorbed
            nxt = re.search(r"\n\*\*[A-Z]", block[len("**Parameters:**"):])
            if nxt:
                block = block[:len("**Parameters:**") + nxt.start()]
            names = set(PARAM_BULLET.findall(block))
            if names:
                out[(skill.parent.name, tool)] = names
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-key", action="store_true",
        help="fail instead of skipping when PUBLORA_DRIFT_KEY is missing (use in CI, "
             "so a renamed or expired secret is visible rather than silently green)")
    args = parser.parse_args()

    key = os.environ.get("PUBLORA_DRIFT_KEY")
    if not key:
        if args.require_key:
            print("PUBLORA_DRIFT_KEY is not set. The drift check cannot run, and a check "
                  "that cannot run must not report success.", file=sys.stderr)
            return 2
        print("PUBLORA_DRIFT_KEY is not set; skipping drift check.", file=sys.stderr)
        return 0

    tools = live_tools(key)
    live = {t["name"] for t in tools}
    claims = documented()

    # Every snake_case heading is a claim, including one naming a tool family
    # this server has never had. Filtering by known prefixes would hide exactly
    # the invented tools this check exists to catch.
    phantom = {n: s for n, s in claims.items() if n not in live}
    uncovered = sorted(live - set(claims))

    # A tool can exist and still be documented with parameters it does not take.
    schemas = {t["name"]: set((t.get("inputSchema") or {}).get("properties") or {})
               for t in tools}
    required = {t["name"]: set((t.get("inputSchema") or {}).get("required") or [])
                for t in tools}
    wrong_params: list[str] = []
    missing_required: list[str] = []
    for (skill, tool), names in sorted(documented_params().items()):
        if tool not in schemas:
            continue
        for bad in sorted(names - schemas[tool]):
            wrong_params.append(
                f"  {skill}: {tool} has no parameter '{bad}' "
                f"(it takes: {', '.join(sorted(schemas[tool])) or 'none'})")
        for miss in sorted(required[tool] - names):
            missing_required.append(
                f"  {skill}: {tool} requires '{miss}', which the skill never mentions")

    if uncovered:
        print("Live tools no skill mentions (not fatal):")
        for name in uncovered:
            print(f"  {name}")
        print()

    if missing_required:
        print("Required parameters a skill never mentions:")
        print("\n".join(missing_required))
        print()

    failed = False
    if phantom:
        print("Documented tools that DO NOT EXIST on the MCP server:")
        for name, skills in sorted(phantom.items()):
            print(f"  {name}  <- {', '.join(skills)}")
        failed = True

    if wrong_params:
        print("Documented parameters that DO NOT EXIST on the tool:")
        print("\n".join(wrong_params))
        failed = True

    if failed:
        return 1

    print(f"OK: every documented MCP tool exists and every documented parameter "
          f"is real ({len(live)} live tools).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

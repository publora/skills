#!/usr/bin/env python3
"""Check that every documentation link in the repo still resolves.

Skips API endpoints and placeholder hosts: `api.publora.com` answers a GET on a
POST route with 404 and an unauthenticated request with 401, which are correct
responses rather than broken links.

Usage: python3 scripts/check_links.py
"""

from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
URL = re.compile(r"https?://[^\s)>\"'`,\\]+")
TRAILING = ".,;:"

# Hosts whose responses do not describe whether a link is good.
SKIP_HOSTS = {
    "api.publora.com",    # REST endpoints: GET on a POST route is a correct 404
    "mcp.publora.com",    # JSON-RPC endpoint, always 401 unauthenticated
    "example.com", "docs.example.com",  # deliberate placeholders
    "img.shields.io",     # badge service, renders per-request
}

# A changelog references the release created when its version is tagged, so
# these are forward references by design until the tag exists.
SKIP_PREFIXES = (
    "https://github.com/publora/skills/releases/tag/",
    "https://github.com/publora/skills/compare/",
)


def documents() -> list[Path]:
    docs = sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)
    return docs


def check(url: str) -> str | None:
    req = urllib.request.Request(url, method="GET", headers={
        "User-Agent": "publora-skills-link-check",
        "Accept": "text/html,application/xhtml+xml,*/*",
    })
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return None if resp.status < 400 else f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return None if e.code < 400 else f"HTTP {e.code}"
    except Exception as e:  # DNS, TLS, timeout
        return type(e).__name__


def main() -> int:
    seen: dict[str, list[str]] = {}
    for doc in documents():
        for raw in URL.findall(doc.read_text(encoding="utf-8")):
            url = raw.rstrip(TRAILING)
            if urlsplit(url).hostname in SKIP_HOSTS or url.startswith(SKIP_PREFIXES):
                continue
            seen.setdefault(url, []).append(str(doc.relative_to(ROOT)))

    broken: list[str] = []
    for url in sorted(seen):
        problem = check(url)
        if problem:
            broken.append(f"{problem}  {url}\n    in {', '.join(sorted(set(seen[url])))}")

    if broken:
        print("Broken links:\n" + "\n".join("  " + b for b in broken))
        return 1

    print(f"OK: {len(seen)} distinct links resolve "
          f"({len(SKIP_HOSTS)} host patterns skipped by design).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

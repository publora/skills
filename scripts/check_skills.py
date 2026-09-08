#!/usr/bin/env python3
"""Static checks for the Publora skills repo.

Catches the classes of drift that shipped to users in 2026: prices copied into
skill bodies, wrong client config paths, links to hosts we do not control, and
frontmatter that agents match on being malformed.

Usage: python3 scripts/check_skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

# Hosts a skill is allowed to link. Anything else is either an ad, a competitor,
# or a link that will rot without anyone here noticing.
ALLOWED_HOSTS = {
    "publora.com", "www.publora.com", "app.publora.com", "api.publora.com",
    "docs.publora.com", "mcp.publora.com",
    "github.com", "t.me",
    "img.shields.io",  # README badges
    "semver.org",      # versioning spec cited in CHANGELOG
    "example.com", "docs.example.com",
}

# Prices belong on publora.com/pricing, which is generated from billing config.
# A price in a skill is a price that will be wrong within a quarter.
PRICE = re.compile(r"\$\s?\d")

# Config paths that were shipped wrong and must not come back.
BAD_PATHS = [
    "~/.claude/claude_desktop_config.json",
    "publora.com/settings/api",
]

URL = re.compile(r"https?://([^/\s)>\"'`,]+)")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def documents() -> list[Path]:
    """Everything we link-check: skills plus the top-level docs."""
    docs = sorted(SKILLS.rglob("*.md"))
    for extra in ("README.md", "CONTRIBUTING.md", "CHANGELOG.md"):
        p = ROOT / extra
        if p.is_file():
            docs.append(p)
    return docs


def acted_on(path: Path) -> bool:
    """True for documents an agent or a new user follows as instructions.

    CONTRIBUTING and CHANGELOG quote the wrong prices and paths on purpose, as
    the record of what went stale. Flagging those would punish writing the
    history down.
    """
    return SKILLS in path.parents or path.name == "README.md"


def check_frontmatter(path: Path, text: str, fail) -> None:
    if path.name != "SKILL.md":
        return
    m = FRONTMATTER.match(text)
    if not m:
        fail(path, "missing YAML frontmatter")
        return
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name or not desc:
        fail(path, "frontmatter needs both name and description")
        return
    if name.group(1).strip() != path.parent.name:
        fail(path, f"name '{name.group(1).strip()}' does not match folder '{path.parent.name}'")
    d = desc.group(1).strip()
    if not 60 <= len(d) <= 400:
        fail(path, f"description is {len(d)} chars, want 60-400")
    if "—" in d or "–" in d:
        fail(path, "description contains an em or en dash")


def main() -> int:
    problems: list[str] = []

    def fail(path: Path, msg: str) -> None:
        problems.append(f"{path.relative_to(ROOT)}: {msg}")

    for path in documents():
        text = path.read_text(encoding="utf-8")
        check_frontmatter(path, text, fail)

        for lineno, line in enumerate(text.splitlines(), 1):
            if not acted_on(path):
                break
            if PRICE.search(line):
                fail(path, f"line {lineno}: price literal, link publora.com/pricing instead")
            for bad in BAD_PATHS:
                if bad in line:
                    fail(path, f"line {lineno}: stale path '{bad}'")

        for host in URL.findall(text):
            if host.lower() not in ALLOWED_HOSTS:
                fail(path, f"link to non-allowlisted host '{host}'")

    if problems:
        print("Skill checks failed:\n" + "\n".join("  " + p for p in problems))
        return 1

    print(f"OK: {len(documents())} documents pass frontmatter, price, path and host checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

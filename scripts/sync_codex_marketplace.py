#!/usr/bin/env python3
"""Regenerate the nested Codex plugin package.

Codex marketplace entries must point at a nested plugin directory, while the
repository root stays the Claude-facing layout. This copies the Codex manifest
and the shipped content into `.codex-marketplace/publora-skills/`.

Do not edit anything under `.codex-marketplace/` by hand: it is generated, and
the next run of this script will overwrite it.

Usage: python3 scripts/sync_codex_marketplace.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / ".codex-marketplace" / "publora-skills"

PATHS_TO_COPY = [
    ".codex-plugin/plugin.json",
    "skills",
    "assets",
    "README.md",
    "LICENSE",
    "SECURITY.md",
]

# Repo plumbing has no business inside an installed plugin.
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def copy(rel: str) -> None:
    src, dest = ROOT / rel, DEST / rel
    if not src.exists():
        print(f"  skip {rel} (missing)")
        return
    if src.is_dir():
        shutil.copytree(src, dest, ignore=IGNORE)
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    print(f"  copied {rel}")


def main() -> int:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)
    print(f"Syncing -> {DEST.relative_to(ROOT)}")
    for rel in PATHS_TO_COPY:
        copy(rel)

    skills = sorted((DEST / "skills").glob("*/SKILL.md"))
    print(f"OK: {len(skills)} skills in the Codex package")
    return 0


if __name__ == "__main__":
    sys.exit(main())

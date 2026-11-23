#!/usr/bin/env python3
"""Regenerate the nested Claude and Codex plugin packages.

Both marketplaces point at a nested plugin directory that holds only what an
installed plugin ships: manifest, skills, assets and the top-level docs. Repo
plumbing (`scripts/`, `.github/`, `requirements-dev.txt`) stays out. The Claude
directory accepts scripts and package lists only from verified organizations,
so `.claude-marketplace/publora-skills/` is also the folder submitted there.

The repository root stays the source of truth. Do not edit anything under
`.claude-marketplace/` or `.codex-marketplace/` by hand: both are generated,
and the next run of this script will overwrite them.

Usage: python3 scripts/sync_plugin_packages.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHARED = ["skills", "assets", "README.md", "LICENSE", "SECURITY.md"]

PACKAGES = {
    "Claude": (
        ROOT / ".claude-marketplace" / "publora-skills",
        # Not the whole .claude-plugin/: marketplace.json describes the repo
        # and would point the package back at itself.
        [".claude-plugin/plugin.json", ".claude-plugin/icon.png", ".mcp.json", *SHARED],
    ),
    "Codex": (
        ROOT / ".codex-marketplace" / "publora-skills",
        [".codex-plugin/plugin.json", *SHARED],
    ),
}

IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def copy(rel: str, dest_root: Path) -> None:
    src, dest = ROOT / rel, dest_root / rel
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
    for name, (dest, paths) in PACKAGES.items():
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
        print(f"Syncing {name} -> {dest.relative_to(ROOT)}")
        for rel in paths:
            copy(rel, dest)
        skills = sorted((dest / "skills").glob("*/SKILL.md"))
        print(f"OK: {len(skills)} skills in the {name} package")
    return 0


if __name__ == "__main__":
    sys.exit(main())

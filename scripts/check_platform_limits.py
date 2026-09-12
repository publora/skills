#!/usr/bin/env python3
"""Compare the platform limits the skills state against the live API.

Six limits in this repo were wrong at once in September 2026: TikTok was called
video-only when it takes 35-image carousels, Instagram was called JPEG-only,
YouTube and Facebook video ceilings were off by three orders of magnitude, and
LinkedIn's image gate was wrong. Every one was a number copied by hand and never
checked again.

`GET /api/v1/platform-limits` is the generated source of truth. This compares the
few facts that can be extracted from the skills unambiguously, and deliberately
stays quiet about the rest: a check that cries wolf on prose is a check people
learn to skip.

Needs PUBLORA_LIMITS_KEY or PUBLORA_DRIFT_KEY (any valid key; the endpoint is
account-independent).

Usage: python3 scripts/check_platform_limits.py [--require-key]
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
ENDPOINT = "https://api.publora.com/api/v1/platform-limits"
# Cloudflare rejects urllib's default agent with a 1010. Do not remove.
USER_AGENT = "publora-skills-limit-check/1 (+https://github.com/publora/skills)"

# Which platform each skill speaks for. social-post covers three at once, so its
# numbers cannot be attributed to one platform and it is left out.
SKILL_PLATFORM = {
    "linkedin-post": "linkedin",
    "linkedin-analytics": "linkedin",
    "x-post": "twitter",
    "threads-post": "threads",
    "instagram-post": "instagram",
    "tiktok-post": "tiktok",
    "telegram-post": "telegram",
    "bluesky-post": "bluesky",
}

# "| Characters | 300 |" and "| Characters per post | 500 |"
CHARS_ROW = re.compile(r"^\|\s*(?:\*\*)?Characters?[^|]*\|\s*(?:\*\*)?([\d,]+)", re.M | re.I)
# "| Images | Up to 4 per post |", "| Images per carousel | 2-20 |"
IMAGES_ROW = re.compile(r"^\|\s*(?:\*\*)?Images?(?: per [a-z]+)?\s*(?:\*\*)?\s*\|[^|]*?(\d+)\s*(?:per post)?\s*\|", re.M | re.I)


def fetch_limits(key: str) -> dict:
    req = urllib.request.Request(
        ENDPOINT, headers={"x-publora-key": key, "User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["platforms"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-key", action="store_true",
                        help="fail instead of skipping when no key is set (use in CI)")
    args = parser.parse_args()

    key = os.environ.get("PUBLORA_LIMITS_KEY") or os.environ.get("PUBLORA_DRIFT_KEY")
    if not key:
        if args.require_key:
            print("No API key set. The limit check cannot run, and a check that "
                  "cannot run must not report success.", file=sys.stderr)
            return 2
        print("No API key set; skipping the platform-limit check.", file=sys.stderr)
        return 0

    limits = fetch_limits(key)
    problems: list[str] = []
    checked = 0

    for skill, platform in sorted(SKILL_PLATFORM.items()):
        path = SKILLS / skill / "SKILL.md"
        if not path.is_file() or platform not in limits:
            continue
        text = path.read_text(encoding="utf-8")
        live = limits[platform]

        real_chars = (live.get("characters") or {}).get("standard")
        found = CHARS_ROW.search(text)
        if real_chars and found:
            checked += 1
            stated = int(found.group(1).replace(",", ""))
            if stated != real_chars:
                problems.append(
                    f"  {skill}: character limit stated as {stated:,}, "
                    f"API says {real_chars:,}")

        images = live.get("images") or {}
        real_max = images.get("maxCount")
        row = IMAGES_ROW.search(text)
        if real_max and row:
            checked += 1
            stated = int(row.group(1))
            # a row may state the lower bound of a carousel range; only the
            # ceiling is comparable, so accept anything at or below it
            if stated > real_max:
                problems.append(
                    f"  {skill}: image count stated as {stated}, "
                    f"API allows {real_max}")

        if images.get("supported") and re.search(r"video[- ]only", text, re.I):
            checked += 1
            problems.append(
                f"  {skill}: calls {platform} video-only, but the API reports "
                f"image support ({real_max} max)")

    if problems:
        print("Limits that disagree with the API:\n" + "\n".join(problems))
        return 1

    print(f"OK: {checked} stated limits across {len(SKILL_PLATFORM)} skills match "
          f"the live platform-limits endpoint.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

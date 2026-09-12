# Changelog

All notable changes to the Publora skills. This project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html), read as described in
[CONTRIBUTING.md](CONTRIBUTING.md): MAJOR when an agent built on the previous
version would now do the wrong thing, MINOR for a new skill or tool, PATCH for a
corrected fact.

## [Unreleased]

## [1.0.3] - 2026-09-12

### Fixed

- **`bluesky-post` documented `altTexts` on `create_post`.** No such parameter
  exists. The platform doc is explicit that the value is not processed and that
  the media model never persists an `alt` property, and `platformSettings`
  rejects Bluesky with `400 PLATFORM_SETTING_UNKNOWN`, so alt text cannot be set
  through the API at all. It was promised in the description, the parameter
  list, an example and a best practice. Found by the parameter check below on
  its first run.

### Added

- **`check_mcp_drift.py` now verifies parameters, not just tool names.** Every
  fix in 1.0.2 passed the old check clean: it asked whether a tool exists and
  never whether its documented parameters do. It now compares each against the
  tool's `inputSchema` and reports required parameters a skill never mentions.
- **`check_platform_limits.py`** compares stated character limits, image counts
  and video-only claims against `GET /api/v1/platform-limits`, which is
  generated rather than hand-written. It checks only what parses unambiguously:
  a check that cries wolf on prose is one people learn to skip.
- **`post_stats` and `profile_stats`** documented in `bluesky-post`. Both are
  live tools that no skill mentioned, returning engagement counters and follower
  counts for Bluesky and Mastodon.

## [1.0.2] - 2026-09-12

### Fixed

Eight factual claims that contradicted the API, each verified against the live
`tools/list` schema or `publora-api-docs` rather than against prose.

- **`linkedin_create_reshare` named the wrong required parameter.** The skill
  said `postedId`; the tool requires `parent`. Every reshare an agent attempted
  from these instructions failed validation. Optional `visibility` added.
- **`linkedin_list_mentionables` named parameters it does not have.** It takes
  `q` and `limit` and requires neither; there is no `platformId`.
- **`platformSettings` is available through MCP.** Five skills said it was REST
  only, so agents abandoned MCP for no reason.
- **TikTok is not video-only.** It takes image carousels of up to 35 JPEG, PNG
  or WebP images at 20 MB each. Agents were refusing valid carousel requests.
- **Instagram is not JPEG-only.** JPEG, PNG and WebP all work, WebP converted
  before publishing. Animated GIF, BMP and TIFF are what get rejected.
- **Video ceilings.** YouTube 256 GB and Facebook 2 GB, not 512 MB. That figure
  belongs to the dashboard's `/media/process-video` multipart endpoint and has
  nothing to do with presigned API or MCP uploads.
- **LinkedIn images** are gated at 36,152,320 pixels with a 50 MB ceiling, not
  5 MB.
- **`showCaptionAboveMedia` is rejected.** Sending it returns
  `400 PLATFORM_SETTING_UNKNOWN`; removed, with a note saying why.

### Known gap

`check_mcp_drift.py` verifies that documented tools exist. It passes clean on
every item above: a correctly named tool with invented parameters, a capability
denied, a limit off by three orders of magnitude. Extending it to compare
parameter names against each tool's `inputSchema` would catch the first two
mechanically; the rest want `GET /api/v1/platform-limits` as a source of truth.

## [1.0.0] - 2026-09-08

First tagged release. The skills had been shipping without versions since March,
so users had no way to tell what they were running or what had changed.

### Fixed

- **Pricing removed from every skill.** The repo quoted Pro at $2.99 and a
  Premium plan that no longer exists. Prices now live only on
  [publora.com/pricing](https://publora.com/pricing), linked rather than copied.
- **Four MCP tools that did not exist.** `linkedin_post_stats`,
  `linkedin_account_stats`, `linkedin_followers` and `linkedin_profile_summary`
  were documented in `linkedin-analytics` but absent from the server. LinkedIn
  analytics is now documented as REST only.
- **Claude Desktop config path.** Every skill pointed at
  `~/.claude/claude_desktop_config.json`, which is not where the config lives.
- **`scheduledTime` documented as required.** It is optional; omitting it creates
  a draft.
- **Threads contradicted itself**, describing auto-threading in detail and then
  stating that multi-part threads are disabled. They are disabled.
- **Platform limit drift**: X video 2:00 to 2:20 (140s), Bluesky image ~1 MB to
  exactly 2,000,000 bytes, Threads video 500 MB to 1 GB, Threads carousel 2-10 to
  2-20 images.

### Added

- **`mediaUrls`** documented in every posting skill: up to 10 public https URLs
  attached before validation, so media and scheduling take one call.
- **`complete_media`** and **`list_connections`** added to every tool list.
- **`linkedin_create_reshare`** and **`linkedin_list_mentionables`**, two real
  tools no skill had ever mentioned.
- **CI**: `verify.yml` checks frontmatter, price literals, stale paths and link
  hosts on every pull request; `drift.yml` compares documented tools against the
  live `tools/list` every Monday.
- **Install paths**: Claude Code and Codex plugin manifests, alongside the
  existing `npx skills add`.
- README rewritten around when to use each skill, the 16 MCP tools, and a FAQ.
- `CONTRIBUTING.md` with the rules that keep facts from drifting again.

### Changed

- All nine `description` fields rewritten as triggers (150-300 characters,
  platform named, "Not for X" sentinel). This is the field agents and directories
  match on; they were 75-113 characters of prose.

[Unreleased]: https://github.com/publora/skills/compare/v1.0.3...HEAD
[1.0.3]: https://github.com/publora/skills/releases/tag/v1.0.3
[1.0.2]: https://github.com/publora/skills/releases/tag/v1.0.2
[1.0.0]: https://github.com/publora/skills/releases/tag/v1.0.0

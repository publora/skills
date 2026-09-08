# Changelog

All notable changes to the Publora skills. This project follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html), read as described in
[CONTRIBUTING.md](CONTRIBUTING.md): MAJOR when an agent built on the previous
version would now do the wrong thing, MINOR for a new skill or tool, PATCH for a
corrected fact.

## [Unreleased]

## [1.0.0] - 2026-09-07

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

[Unreleased]: https://github.com/publora/skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/publora/skills/releases/tag/v1.0.0

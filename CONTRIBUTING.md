# Contributing

These skills are read by AI agents that act on what they say. A wrong number here
becomes a wrong API call, a failed post, or a user quoting a price that does not
exist. That shapes every rule below.

## The one rule

**A skill must not restate a fact that lives in the API.**

Between March and September 2026 this repo shipped Pro at $2.99 and a Premium
plan that had been retired, four MCP tools that never existed, and a Claude
Desktop config path that was never correct. None of it was carelessness. It was
copied by hand once and then had no way to notice it had gone stale.

So the skills link facts instead of copying them:

| Fact | Source of truth | In a skill |
|---|---|---|
| Prices, plan limits | [publora.com/pricing.md](https://publora.com/pricing.md) | a link, never a number |
| MCP tools and signatures | live `tools/list`, [tools-reference](https://docs.publora.com/mcp/tools-reference) | only tools that exist today |
| Platform limits | `GET /api/v1/platform-limits` | numbers checked against the endpoint |
| Client config paths | [mcp/client-setup](https://docs.publora.com/mcp/client-setup) | a link, not a copied path |
| REST contract | [publora-api-docs](https://github.com/publora/publora-api-docs) | follow its changelog |

CI enforces the first, third and fourth mechanically. Any `$` followed by a digit
fails the build.

## Workflow

- Work on a branch, open a pull request. `main` is protected.
- Content changes need one approval. Changes to `.github/` or `scripts/` need two,
  because those are what stop the next round of drift.
- External pull requests are read in full before merge. CI checks that every link
  points at a host we control; a human confirms the change is what it claims.
- An entry in the [API changelog](https://docs.publora.com/changelog) becomes an
  issue here within seven days.
- Once a quarter, run five real scenarios through an agent with these skills
  loaded and attach the transcript to a pull request. Static checks cannot tell
  you that a skill is confusing, only that it is not provably wrong.

## Versioning and releases

Semantic versioning, read for a documentation repo:

- **MAJOR** a skill is renamed or removed, or a tool changes meaning. An agent
  built on the old version now does the wrong thing.
- **MINOR** a new skill, tool or platform.
- **PATCH** a corrected fact, link or limit.

The version lives in `CHANGELOG.md` and the git tag. It is deliberately not
repeated in nine files.

Every merge that touches `skills/` gets a tag **and** a GitHub Release. A tag on
its own is invisible: the release badge and the Releases page both read the
Releases API, and release notes are what search engines index.

Release notes are three lines: what changed for the agent, what changed in the
API with a link to its changelog, and how to update
(`npx skills add publora/skills`).

## Checks you can run locally

```bash
python3 scripts/check_skills.py                          # frontmatter, prices, paths, hosts
python3 scripts/check_links.py                           # every documentation link resolves
PUBLORA_DRIFT_KEY=sk_... python3 scripts/check_mcp_drift.py   # documented tools still exist
python3 scripts/sync_codex_marketplace.py                # regenerate the Codex package
```

The drift key must be a Starter-plan key with **no connected accounts**. The check
only calls `initialize` and `tools/list`, so it never needs the ability to publish.

## Writing a skill

The `description` in the frontmatter is the field agents and directories match
on. It decides whether a skill is ever loaded, so it is the most valuable line in
the file. Aim for 150 to 300 characters, and:

- start with the trigger: "Use when the user wants to ..."
- name the platform and Publora
- end with a "Not for X (use Y)" sentinel so sibling skills do not compete

Then say what the skill will never do. "TikTok unaudited apps can only publish
private videos" saves an agent from promising something the platform will refuse.

## What changes for an agent

<!-- One or two sentences. What will an agent do differently after this merge? -->

## Facts touched

<!-- Delete rows that do not apply. Link the source you verified against. -->

| Fact | Verified against |
|---|---|
| MCP tool names or signatures | live `tools/list` / docs.publora.com/mcp/tools-reference |
| Platform limits | `GET /api/v1/platform-limits` |
| REST contract | docs.publora.com/changelog |
| Client config | docs.publora.com/mcp/client-setup |

## Checklist

- [ ] No prices in the diff. Pricing links to publora.com/pricing.
- [ ] Every tool named here exists in the live `tools/list`.
- [ ] `python3 scripts/check_skills.py` passes.
- [ ] `python3 scripts/check_links.py` passes.
- [ ] `CHANGELOG.md` updated under Unreleased.
- [ ] If `skills/` changed, this needs a tag and a Release after merge.

---
name: linkedin-analytics
description: Analyze LinkedIn performance and manage engagement through Publora. Use when the user asks how a LinkedIn post or account performed (impressions, reach, reactions, comments, reshares, follower growth) or wants to react, comment, reshare or resolve an @mention. Statistics run over the REST API, engagement over MCP tools. Not for creating posts (use linkedin-post).
---

# LinkedIn Analytics

Track impressions, engagement and follower growth for your LinkedIn posts and profile, and interact with posts through reactions, comments and reshares. Statistics come from the REST API; reactions, comments, reshares and mention lookups are MCP tools.

## Prerequisites

**Plans:** Works on the free Starter plan. Current limits and pricing: [publora.com/pricing](https://publora.com/pricing).

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register) (free)
2. **Connect LinkedIn** via OAuth in [Publora Dashboard](https://app.publora.com/dashboard)
3. **Get API key** at [app.publora.com/dashboard/api](https://app.publora.com/dashboard/api)
4. **Connect your agent** to the MCP server at `https://mcp.publora.com`, authenticating with `Authorization: Bearer sk_YOUR_API_KEY`. In Claude Code:

```bash
claude mcp add publora --transport http https://mcp.publora.com \
  --header "Authorization: Bearer sk_YOUR_API_KEY"
```

   Claude Desktop, Cursor, Codex, OpenClaw and the claude.ai connector each need a different config file or flow: see [client setup](https://docs.publora.com/mcp/client-setup) for the exact path and snippet.

### REST API Fallback

If the MCP server is unavailable or returns errors, use the REST API directly:

**Base URL:** `https://api.publora.com/api/v1`

**Authentication:** Use `x-publora-key` header (NOT `Authorization: Bearer`):

```bash
# Get your connected platforms
curl -X GET "https://api.publora.com/api/v1/platform-connections" \
  -H "x-publora-key: sk_your_api_key"

# Get post statistics
curl -X POST "https://api.publora.com/api/v1/linkedin-post-statistics" \
  -H "x-publora-key: sk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "platformId": "linkedin-abc123",
    "postedId": "urn:li:share:7123456789012345678",
    "queryTypes": "ALL"
  }'

# Get account statistics
curl -X POST "https://api.publora.com/api/v1/linkedin-account-statistics" \
  -H "x-publora-key: sk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "platformId": "linkedin-abc123",
    "queryTypes": "ALL"
  }'
```

**Platform ID Format:** `linkedin-{id}` where `{id}` is from `/platform-connections` response.

Example IDs: `linkedin-Tz9W5i6ZYG`, `linkedin-abc123xyz`

📖 **Full API documentation:** [docs.publora.com](https://docs.publora.com)

## Analytics Tools (REST only)

LinkedIn analytics are **not exposed as MCP tools**. The MCP server carries posting, media and LinkedIn engagement tools; statistics live only on the REST API, so call these endpoints directly with the `x-publora-key` header. Asking an agent for an `linkedin_post_stats` MCP tool will fail: there is no such tool.

### POST /linkedin-post-statistics
Engagement metrics for one post.

**Body:**
- `platformId`: platform connection ID (e.g. `linkedin-abc123`), from `list_connections`
- `postedId`: post URN (`urn:li:share:...` or `urn:li:ugcPost:...`)
- `queryTypes` (optional): `IMPRESSION`, `MEMBERS_REACHED`, `RESHARE`, `REACTION`, `COMMENT`, or `ALL`

**Returns:** impressions, unique impressions (members reached), reactions, comments, reshares, and a `cached` flag telling you whether the numbers came from cache.

### POST /linkedin-account-statistics
Aggregated statistics for the account.

**Body:** `platformId`, optional `queryTypes`, optional `aggregation` (`DAILY` or `TOTAL`, default `TOTAL`).

### POST /linkedin-followers
Follower count or growth over time.

**Body:** `platformId`, optional `period` (`lifetime` or `daily`), optional `dateRange` (`{start: {year, month, day}, end: {year, month, day}}`).

### POST /linkedin-profile-summary
Combined profile overview: followers plus statistics.

**Body:** `platformId`, optional `dateRange`.

```bash
curl -X POST "https://api.publora.com/api/v1/linkedin-post-statistics" \
  -H "x-publora-key: sk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"platformId": "linkedin-abc123", "postedId": "urn:li:share:7123456789012345678", "queryTypes": "ALL"}'
```

## Engagement Tools

### linkedin_create_reaction
React to a LinkedIn post.

**Parameters:**
- `postedId`: LinkedIn post URN
- `platformId`: Platform connection ID
- `reactionType`: One of the following:

| Type | Description |
|------|-------------|
| `LIKE` | Standard thumbs up |
| `PRAISE` | Clapping hands / applause |
| `EMPATHY` | Heart / love |
| `INTEREST` | Lightbulb / insightful |
| `APPRECIATION` | Supportive |
| `ENTERTAINMENT` | Funny / laughing |

### linkedin_delete_reaction
Remove your reaction from a post.

**Parameters:**
- `postedId`: LinkedIn post URN
- `platformId`: Platform connection ID

### linkedin_create_comment
Post a comment on a LinkedIn post (max 1,250 characters).

**Parameters:**
- `postedId`: LinkedIn post URN
- `platformId`: Platform connection ID
- `message`: Comment text (max 1,250 characters)
- `parentComment` (optional): Comment URN for nested replies

### linkedin_create_reshare
Reshare an existing post, with optional commentary.

**Parameters:**
- `postedId`: the original post's **share URN** (`urn:li:share:...` or `urn:li:ugcPost:...`)
- `platformId`: platform connection ID
- `commentary` (optional): your text above the reshare

Note: a LinkedIn feed URL carries an `activity` id, which is not always the same as the share id. Use the `postedId` returned by `get_post`, not a hand-converted activity id.

### linkedin_list_mentionables
Resolve names to the URNs that @mentions need, so you never hand-write a member id.

**Parameters:**
- `platformId`: platform connection ID
- `query`: the name to search for

### linkedin_delete_comment
Remove a comment you made.

**Parameters:**
- `postedId`: LinkedIn post URN
- `commentId`: Comment URN or numeric ID
- `platformId`: Platform connection ID

## Example Prompts

### Weekly Performance Review
```
Analyze my LinkedIn performance for the last 7 days.
Show me:
1. Which posts performed best
2. My engagement rate trends
3. Follower growth
4. Recommendations for improvement
```

### Post Analysis
```
Get detailed stats for my last 5 LinkedIn posts and identify patterns in what content resonates with my audience.
```

### Engagement Campaign
```
React with PRAISE to my colleague's post about their promotion (urn:li:share:123456) and add a congratulatory comment.
```

### Follower Tracking
```
Show my LinkedIn follower growth for the last 30 days. How many new followers did I gain each week?
```

## Metrics Reference

| Metric | Description |
|--------|-------------|
| `IMPRESSION` | Total times content appeared in feeds |
| `MEMBERS_REACHED` | Unique LinkedIn members who saw the post |
| `RESHARE` | Number of reposts/shares |
| `REACTION` | Total reactions (all types combined) |
| `COMMENT` | Number of comments |

## Engagement Rate Benchmarks

**Average LinkedIn engagement rates by follower count:**

| Followers | Good Engagement Rate |
|-----------|---------------------|
| < 5K | 3-5% |
| 5K-50K | 2-3% |
| 50K+ | 1-2% |

**Good performing posts typically have:**
- 2x your average impressions
- Comment-to-reaction ratio above 10%
- Engagement rate above your baseline

## Important Notes

1. **Analytics delay**: LinkedIn analytics may take up to 24 hours to fully populate. Querying immediately after posting returns partial data.

2. **URN formats**: LinkedIn URLs use `urn:li:activity:xxx` but the API requires `urn:li:share:xxx` or `urn:li:ugcPost:xxx`. Use the `postedId` from Publora's `get_post` response for accurate URNs.

3. **Caching**: Analytics responses may be cached. The response includes a `cached` field indicating if data came from cache.

4. **Rate limits**: LinkedIn has approximately 200+ API calls per hour. Implement backoff on 429 errors.

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Platform ID not found" | Invalid connection ID | Run `list_connections` to get valid IDs |
| "Post not found" | Wrong URN format | Use `urn:li:share:` or `urn:li:ugcPost:` format |
| 429 Too Many Requests | Rate limited | Wait and retry with exponential backoff |
| "message cannot exceed 1250 characters" | Comment too long | Shorten comment to under 1,250 chars |

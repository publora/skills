---
name: linkedin-analytics
description: Analyze LinkedIn performance, track engagement metrics, and manage reactions/comments via Publora MCP
---

# LinkedIn Analytics

Get detailed analytics for your LinkedIn posts and profile using the Publora MCP server. Track impressions, engagement, follower growth, and interact with posts through reactions and comments.

## Prerequisites

**Plans:** Starter (free), Pro, Premium - LinkedIn is available on all plans including free.

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register) (free)
2. **Connect LinkedIn** via OAuth in [Publora Dashboard](https://publora.com/dashboard)
3. **Get API key** at [publora.com/settings/api](https://publora.com/settings/api)
4. **Configure MCP** in Claude Desktop (`~/.claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "publora": {
      "type": "http",
      "url": "https://mcp.publora.com",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### REST API Fallback

If the MCP server is unavailable or returns errors, use the REST API directly:

**Base URL:** `https://api.publora.com/api/v1`

**Authentication:** Use `x-publora-key` header (NOT `Authorization: Bearer`):

```bash
# Get your connected platforms
curl -X GET "https://api.publora.com/api/v1/platform-connections" \
  -H "x-publora-key: sk_your_api_key"

# Get post stats (via REST endpoint)
curl -X GET "https://api.publora.com/api/v1/linkedin/post-stats?postedId=urn:li:share:123456&platformId=linkedin-abc123" \
  -H "x-publora-key: sk_your_api_key"
```

**Platform ID Format:** `linkedin-{id}` where `{id}` is from `/platform-connections` response.

Example IDs: `linkedin-Tz9W5i6ZYG`, `linkedin-abc123xyz`

📖 **Full API documentation:** [docs.publora.com](https://docs.publora.com)

## Analytics Tools

### linkedin_post_stats
Get engagement metrics for a specific LinkedIn post.

**Parameters:**
- `postedId`: LinkedIn post URN (e.g., `urn:li:share:123456` or `urn:li:ugcPost:123456`)
- `platformId`: Platform connection ID (e.g., `linkedin-abc123`)
- `queryTypes` (optional): Metrics to fetch: `IMPRESSION`, `MEMBERS_REACHED`, `RESHARE`, `REACTION`, `COMMENT`

**Response includes:**
- Impressions (total views)
- Unique impressions (members reached)
- Reactions count
- Comments count
- Shares/reposts
- Engagement rate

### linkedin_account_stats
Get aggregated statistics for your LinkedIn account.

**Parameters:**
- `platformId`: Platform connection ID
- `queryTypes` (optional): Metrics to fetch
- `aggregation` (optional): `DAILY` or `TOTAL` (default: TOTAL)

### linkedin_followers
Get follower count or growth over time.

**Parameters:**
- `platformId`: Platform connection ID
- `period` (optional): `lifetime` or `daily`
- `dateRange` (optional): For daily period: `{start: {year, month, day}, end: {year, month, day}}`

### linkedin_profile_summary
Get a combined profile overview with followers and stats.

**Parameters:**
- `platformId`: Platform connection ID
- `dateRange` (optional): Date range for stats

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

---
name: linkedin-analytics
description: Analyze LinkedIn performance, track post engagement, and monitor follower growth via Publora MCP
---

# LinkedIn Analytics

Get detailed analytics for your LinkedIn posts and profile using the Publora MCP server. Track engagement, monitor follower growth, and optimize your content strategy.

## Prerequisites

Connect Publora MCP server in your Claude Desktop config:

```json
{
  "mcpServers": {
    "publora": {
      "url": "https://mcp.publora.com/sse",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Get your API key at [publora.com/settings/api](https://publora.com/settings/api)

## Available Tools

### linkedin_post_stats
Get detailed analytics for a specific LinkedIn post.

**Parameters:**
- `post_id`: The ID of the post to analyze

**Returns:**
- Impressions (total views)
- Unique impressions
- Engagement rate
- Reactions breakdown (likes, celebrates, supports, loves, insightful, funny)
- Comments count
- Shares/reposts
- Click-through rate

### linkedin_account_stats
Get overall account performance metrics.

**Parameters:**
- `period` (optional): Time range - "7d", "30d", "90d" (default: "30d")

**Returns:**
- Total impressions over period
- Total engagements
- Average engagement rate
- Top performing posts
- Posting frequency analysis

### linkedin_followers
Get follower analytics and growth trends.

**Parameters:**
- `period` (optional): Time range for growth analysis

**Returns:**
- Current follower count
- Follower growth (net new followers)
- Follower demographics (when available)
- Growth rate percentage

### linkedin_profile_summary
Get a summary of your LinkedIn profile performance.

**Returns:**
- Profile views
- Search appearances
- Post impressions summary
- Connection/follower count

## Engagement Tools

### linkedin_create_reaction
Add a reaction to a post.

**Parameters:**
- `post_id`: Target post ID
- `reaction_type`: "LIKE", "CELEBRATE", "SUPPORT", "LOVE", "INSIGHTFUL", "FUNNY"

### linkedin_delete_reaction
Remove your reaction from a post.

### linkedin_create_comment
Add a comment to a post.

**Parameters:**
- `post_id`: Target post ID
- `text`: Comment content

### linkedin_delete_comment
Remove a comment you made.

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

### Post-by-Post Analysis
```
Get detailed stats for my last 5 LinkedIn posts and identify
patterns in what content resonates with my audience.
```

### Content Strategy Insights
```
Based on my LinkedIn analytics, what topics and posting times
generate the highest engagement? Give me data-driven recommendations.
```

### Engagement Analysis
```
Analyze the comments and reactions on my recent posts.
What sentiment trends do you see? Who are my most engaged followers?
```

## Metrics Explained

| Metric | What It Measures | Why It Matters |
|--------|------------------|----------------|
| Impressions | Total times your content appeared in feeds | Reach and visibility |
| Engagement Rate | (Reactions + Comments + Shares) / Impressions | Content quality signal |
| Click-through Rate | Clicks on links or "see more" / Impressions | Call-to-action effectiveness |
| Follower Growth | Net new followers over time | Audience building momentum |

## Benchmarks

**Average LinkedIn engagement rates by follower count:**
- < 5K followers: 3-5% is good
- 5K-50K followers: 2-3% is good
- 50K+ followers: 1-2% is good

**Good performing posts typically have:**
- 2x your average impressions
- Engagement rate above your baseline
- Comment-to-reaction ratio above 10%

## Tips for Better Analytics

1. **Track consistently**: Review analytics weekly to spot trends
2. **Compare similar content**: Group posts by topic/format for meaningful comparisons
3. **Note external factors**: Events, holidays, and news can affect performance
4. **Focus on engagement rate**: Raw numbers vary; rate shows quality
5. **Watch for patterns**: Best days, times, topics, and formats for your audience

---
name: threads-post
description: Create and schedule Threads posts with image carousels and reply control via Publora MCP. Use when the user wants to post to Meta's Threads. Multi-part threading is currently disabled by the platform, so long content stays a single post. Not for Instagram (use instagram-post) or X threads (use x-post).
---

# Threads Post

Create and schedule posts on Meta's Threads using the Publora MCP server. Supports single posts, image carousels (2-20 images) and reply control. Multi-part threading is disabled by the platform connection right now.

## Prerequisites

**Plans:** Works on the free Starter plan. Current limits and pricing: [publora.com/pricing](https://publora.com/pricing).

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register) (free)
2. **Connect Threads** via Instagram OAuth in [Publora Dashboard](https://app.publora.com/dashboard)
3. **Get API key** at [app.publora.com/dashboard/api](https://app.publora.com/dashboard/api)
4. **Connect your agent** to the MCP server at `https://mcp.publora.com`, authenticating with `Authorization: Bearer sk_YOUR_API_KEY`. In Claude Code:

```bash
claude mcp add publora --transport http https://mcp.publora.com \
  --header "Authorization: Bearer sk_YOUR_API_KEY"
```

   Claude Desktop, Cursor, Codex, OpenClaw and the claude.ai connector each need a different config file or flow: see [client setup](https://docs.publora.com/mcp/client-setup) for the exact path and snippet.

### REST API Fallback

If MCP is unavailable, use the REST API directly:

**Base URL:** `https://api.publora.com/api/v1`

**Authentication:** `x-publora-key` header

```bash
# Get connected platforms
curl -X GET "https://api.publora.com/api/v1/platform-connections" \
  -H "x-publora-key: sk_your_api_key"

# Create a post
curl -X POST "https://api.publora.com/api/v1/create-post" \
  -H "x-publora-key: sk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["threads-12345"],
    "content": "Your post content",
    "scheduledTime": "2026-03-25T10:00:00Z"
  }'
```

**Platform ID Format:** `threads-{id}` (from `/platform-connections`)

📖 **Docs:** [docs.publora.com](https://docs.publora.com)

## Platform Limits

| Feature | Limit |
|---------|-------|
| Characters per post | 500 |
| Hashtags | 1 per post maximum |
| Links | 5 per post maximum |
| Images per carousel | 2-20 |
| Image size | 8 MB |
| Image formats | JPEG, PNG (WebP auto-converted) |
| Video duration | 5 minutes |
| Video size | 1 GB |
| Video formats | MP4, MOV |
| Posts per day | 250 |
| Replies per day | 1,000 |

## Available Tools

### create_post
Create a new Threads post or thread.

**Parameters:**
- `platforms`: Array with your Threads connection ID (e.g., `["threads-12345"]`)
- `content`: Post text (auto-threads if over 500 chars)
- `scheduledTime`: ISO 8601 UTC datetime. **Optional**: omit it and the post is created as a draft. Send a future time to schedule. A time five or more minutes in the past is rejected with `SCHEDULED_TIME_IN_PAST`, so for immediate posting use the current time plus a minute.
- `mediaUrls`: up to 10 public **https** image or video URLs. Publora downloads them server-side and attaches them *before* validation, so media and scheduling happen in one call. This is the one-shot alternative to the draft then `get_upload_url` then `complete_media` flow. Ingestion is rate-limited to 60 URLs per hour.

### get_upload_url
Get a presigned URL to upload images.

### complete_media
Finalize a file uploaded through `get_upload_url`, after the presigned `PUT` succeeds. Optional, because scheduling also finalizes pending media, but calling it early surfaces format and probe errors before publish. Not needed for media attached with `mediaUrls`.

**Parameters:**
- `mediaId`: the id returned by `get_upload_url`

### list_connections
List your connected accounts with their platform IDs. Call this first and copy the IDs verbatim; they are never guessable.

### list_posts / get_post / update_post / delete_post
Manage scheduled and draft posts. `update_post` also patches `content` and `platforms` on a draft or scheduled post, so fixing a typo or retargeting no longer means delete and recreate. `delete_media` and `prune_media_reference` clean up uploaded files.

## Long Content

Threads posts are capped at 500 characters and **Publora's multi-part threading is currently disabled** while the Threads app connection is being restored. Content over the limit is not split automatically, so:

- Keep the post inside 500 characters, or
- Publish the parts yourself as separate posts, or
- Move the long-form version to a platform that threads today (X) and link to it.

Manual `---` separators and `[1/3]` markers are preserved as written but do **not** create a connected reply chain right now. Contact support@publora.com for the restore timeline.

## Reply Control

Control who can reply to your posts via REST API `platformSettings`:

| Value | Description |
|-------|-------------|
| `""` (empty) | Default platform behavior (anyone can reply) |
| `"everyone"` | Explicitly allow anyone to reply |
| `"accounts_you_follow"` | Only accounts you follow can reply |
| `"mentioned_only"` | Only mentioned accounts can reply |

Note: `platformSettings` is not available via MCP - use REST API for reply control.

## Important Restrictions

1. **Single hashtag limit**: Threads allows maximum 1 hashtag per post. Additional hashtags are ignored by the platform.

2. **No post editing**: Once posted, Threads posts cannot be edited via API. Delete and repost if needed.

3. **Video carousels not supported**: Publora's carousel implementation supports images only. Standalone video posts work normally.

4. **Multi-threaded posts temporarily unavailable**: Content splitting into multiple connected replies is temporarily disabled. Single posts and carousels continue to work.

## Examples

### Simple Text Post
```
Post this to Threads:
"Just discovered an amazing productivity hack that saved me 2 hours today. The key is batching similar tasks together."
```

### Image Carousel
```
Create a Threads carousel with these 5 product evolution screenshots.
Caption: "From concept to launch - our 6-month journey. #buildinpublic"
```
Note: Requires 2-20 images. Videos in carousels are not supported.

### Long Content (published as separate posts)

Threading is disabled, so ask for the parts explicitly:

```
Post this to Threads as separate posts:
"Thread: 7 mistakes I made as a first-time founder

---

1. Hiring too fast. We went from 2 to 15 in 3 months. The culture suffered.

---

2. Ignoring unit economics. Revenue felt great until we calculated CAC..."
```

### Scheduled Post
```
Schedule this for tomorrow at 10 AM:
"Monday motivation: The best time to start was yesterday. The second best time is now."
```

## Best Practices

1. **Hook first**: First 2 lines determine engagement - make them count
2. **Optimal length**: 100-250 characters for single posts perform well
3. **Native content**: Original, conversational posts are rewarded
4. **Single hashtag**: Use one highly relevant hashtag (platform limit)
5. **No edit option**: Double-check content before posting

### Timing
- **Best times**: 7-9 AM, 12-1 PM, 7-9 PM in target timezone
- **Frequency**: 1-3 posts per day for growth
- **Consistency**: Regular posting signals active account

### Engagement
- Reply to comments within first hour
- Cross-reference your Instagram (accounts are linked)
- Use relevant topics/keywords for discovery

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Account not connected" | Threads/Instagram OAuth expired | Reconnect via Publora dashboard |
| "Content too long" | Post exceeds 500 chars and threading failed | Manually add `---` breaks |
| "Media upload failed" | Wrong format or size | Check: images < 8 MB, JPEG/PNG only |
| "Carousel requires 2-20 items" | Wrong number of images | Ensure 2-20 images for carousel |
| 250 posts/day exceeded | Rate limit reached | Wait 24 hours |

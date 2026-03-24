---
name: threads-post
description: Create and schedule Threads posts with auto-threading, image carousels, and reply control via Publora MCP
---

# Threads Post

Create and schedule posts on Meta's Threads using the Publora MCP server. Supports auto-threading for long content, image carousels (2-10 images), and reply control settings.

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

## Platform Limits

| Feature | Limit |
|---------|-------|
| Characters per post | 500 |
| Hashtags | 1 per post maximum |
| Links | 5 per post maximum |
| Images per carousel | 2-10 |
| Image size | 8 MB |
| Image formats | JPEG, PNG (WebP auto-converted) |
| Video duration | 5 minutes |
| Video size | 500 MB |
| Video formats | MP4, MOV |
| Posts per day | 250 |
| Replies per day | 1,000 |

## Available Tools

### create_post
Create a new Threads post or thread.

**Parameters:**
- `platforms`: Array with your Threads connection ID (e.g., `["threads-12345"]`)
- `content`: Post text (auto-threads if over 500 chars)
- `scheduledTime`: ISO 8601 datetime

### get_upload_url
Get a presigned URL to upload images.

### list_posts / update_post / delete_post
Manage your scheduled and draft posts.

## Auto-Threading

When content exceeds 500 characters, Publora automatically creates a connected thread:

1. **Smart splitting**: Content is split at paragraph breaks (`\n\n`), then sentence boundaries (`. `, `! `, `? `), then word boundaries
2. **Auto-numbering**: Each part gets `(1/N)`, `(2/N)`, etc. at the end
3. **Reply chain**: Posts are connected using Threads' `reply_to_id` parameter

### Manual Thread Breaks

Use `---` on its own line to force a thread break:

```
This is my first post in the thread.

---

This is my second post in the thread.

---

And this is my third post!
```

Or use explicit markers `[1/3]`, `[2/3]`, `[3/3]` (square brackets are preserved as written).

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
Note: Requires 2-10 images. Videos in carousels are not supported.

### Long-Form Thread
```
Create a Threads thread from this content:
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
| "Carousel requires 2-10 items" | Wrong number of images | Ensure 2-10 images for carousel |
| 250 posts/day exceeded | Rate limit reached | Wait 24 hours |

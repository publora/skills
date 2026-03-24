---
name: threads-post
description: Create and schedule Threads posts with auto-threading, carousels, and reply chains via Publora MCP
---

# Threads Post

Create and schedule posts on Meta's Threads using the Publora MCP server. Supports auto-threading for long content, image carousels, and reply chains.

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
| Images per carousel | 10 |
| Video length | 5 minutes |
| Video size | 1 GB |

## Available Tools

### create_post
Create a new Threads post or thread.

**Parameters:**
- `platform`: "threads"
- `content`: Post text (auto-threads if over 500 chars)
- `scheduled_at` (optional): ISO 8601 datetime
- `media_ids` (optional): Array for carousels

### get_upload_url
Get a presigned URL to upload images or videos.

### list_posts
List your scheduled and published Threads posts.

### update_post / delete_post
Manage posts before they're published.

## Auto-Threading

Publora automatically handles long content:

1. **Smart splitting**: Content over 500 characters is split at natural paragraph or sentence boundaries
2. **Thread markers**: Each part gets numbered `(1/N)`, `(2/N)`, etc.
3. **Reply chain**: Posts are published as a connected thread

### Manual Thread Breaks

Use `---` on its own line to force a thread break:

```
This is the first post in my thread.

---

This will be the second post.

---

And this is the third.
```

## Examples

### Simple Text Post
```
Post this to Threads:
"Just discovered an amazing productivity hack that saved me 2 hours today..."
```

### Long-Form Thread
```
Create a Threads thread from this article summary:
[Paste your long content here - Publora will auto-thread it]
```

### Image Carousel
```
Create a Threads carousel with these 5 images showing our product evolution.
Add this caption: "From concept to launch - our 6-month journey."
```

### Scheduled Thread
```
Schedule this thread for tomorrow at 10 AM:
"Thread: 7 mistakes I made as a first-time founder 🧵

---

1. Hiring too fast. We went from 2 to 15 in 3 months...

---

2. Ignoring unit economics. Revenue felt great until...
"
```

## Best Practices

### Content Strategy
1. **Hook first**: First 2 lines determine if people engage
2. **Native content**: Threads rewards original, conversational posts
3. **Optimal length**: 100-250 characters for single posts perform well
4. **Threads (multi-post)**: Save for valuable, structured content

### Timing
- **Best times**: 7-9 AM, 12-1 PM, 7-9 PM in target timezone
- **Frequency**: 1-3 posts per day for growth
- **Consistency**: Regular posting signals active account

### Engagement
- Reply to comments within first hour
- Cross-reference your Instagram (they're linked)
- Use relevant topics/keywords (Threads has topic discovery)

## Supported Media

| Type | Formats | Notes |
|------|---------|-------|
| Images | JPG, PNG | Up to 10 per carousel |
| Video | MP4, MOV | Max 5 min, 1 GB |
| GIF | GIF | Treated as image |

## Troubleshooting

- **"Account not connected"**: Connect your Threads (Instagram) account in Publora dashboard
- **"Content too long"**: If auto-threading fails, manually add `---` breaks
- **"Media upload failed"**: Check file format and size limits
- **"Thread out of order"**: Publora maintains thread order; if issues persist, contact support

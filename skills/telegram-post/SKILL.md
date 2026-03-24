---
name: telegram-post
description: Post to Telegram channels and groups with markdown formatting, media support, and message options via Publora MCP
---

# Telegram Post

Create and schedule posts to Telegram channels and groups using the Publora MCP server. Supports rich markdown formatting, photos, videos, and message delivery options.

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

**Additional setup:**
1. Create a bot with [@BotFather](https://t.me/BotFather) on Telegram
2. Add the bot as **administrator** to your channel/group with `can_post_messages` permission
3. Connect in Publora dashboard with bot token and channel name

## Platform Limits (Bot API)

| Feature | Limit |
|---------|-------|
| Text message | 4,096 characters |
| **Media caption** | **1,024 characters** (critical limit!) |
| Images | 10 MB max, 10 per media group |
| Image formats | JPEG, PNG, GIF, BMP, WebP |
| **Video size** | **50 MB max** (not 4 GB - that's for users!) |
| Video formats | MP4, MOV, AVI, MKV, WebM |
| Rate limit | 30 msg/sec global, 20 msg/min per group |

**Critical:** Bot API has much lower limits than regular Telegram users. Videos over 50 MB and captions over 1,024 characters will fail.

## Markdown Formatting

Telegram uses its own markdown flavor with **single asterisks** for bold:

| Syntax | Result |
|--------|--------|
| `*bold*` | **bold** |
| `_italic_` | *italic* |
| `` `code` `` | `inline code` |
| ``` ```code``` ``` | Code block |
| `[text](url)` | [hyperlink](url) |
| `> text` | Blockquote |

**Note:** This differs from standard Markdown where `**double asterisks**` make bold.

## Available Tools

### create_post
Create a new Telegram post.

**Parameters:**
- `platforms`: Array with your Telegram connection ID (e.g., `["telegram-1001234567890"]`)
- `content`: Message text (supports markdown)
- `scheduledTime`: ISO 8601 datetime

### get_upload_url
Get presigned URL for media uploads.

### list_posts / update_post / delete_post
Manage scheduled and draft posts.

## Post Options (via REST API)

Telegram-specific options available via REST API `platformSettings.telegram`:

| Option | Description |
|--------|-------------|
| `disableNotification` | Send silently (no sound) |
| `disableWebPagePreview` | No link preview cards |
| `showCaptionAboveMedia` | Caption above image/video |
| `protectContent` | Prevent forwarding/saving |

Note: `platformSettings` is not available via MCP - use REST API for these options.

## Examples

### Simple Channel Post
```
Post this to my Telegram channel:
"*Product Update v2.5*

We have shipped the following improvements:
- _Faster API response times_ (avg 45ms)
- New `batch` endpoint for bulk operations

[Read the changelog](https://example.com/changelog)"
```

### Formatted Announcement
```
Create a Telegram post with this formatting:
"*Important Update*

We're launching our new feature tomorrow at 10 AM UTC.

_What's new:_
- Feature A improvements
- Feature B release

[Read the full announcement](https://example.com/update)"
```

### Post with Image
```
Post this image to my Telegram channel with caption:
"*New Dashboard Preview*

Here's a sneak peek at our redesigned analytics dashboard."
```
**Important:** Caption must be under 1,024 characters when posting with media.

### Scheduled Post
```
Schedule this for tomorrow at 8 AM Moscow time:
"*Good morning!* Here's your daily market summary..."
```

## Important Restrictions

1. **Caption limit is 1,024 chars**: When posting with media (images/videos), text is sent as a caption limited to 1,024 characters. Text-only messages allow 4,096 characters.

2. **Video max 50 MB**: Bot API limits videos to 50 MB (not 4 GB like regular users). Large videos will fail.

3. **Bot must be admin**: Your bot needs administrator role with `can_post_messages` permission. This is verified at connection time.

4. **No mixed media**: A single post cannot contain both images and videos.

5. **Caption overflow**: If caption exceeds 1,024 chars on a media post, it's sent as a separate reply message instead of being truncated.

## Best Practices

### Content
1. **Use formatting**: Bold headlines, italic emphasis improves readability
2. **Link previews**: Great for articles; disable for cleaner announcements
3. **Emoji usage**: Common and expected on Telegram
4. **Post length**: No penalty for longer posts on text-only messages

### Timing
- **Global audience**: Telegram users are worldwide; consider timezone posts
- **Best times**: 8-10 AM, 12-2 PM, 7-9 PM in target regions
- **Frequency**: Channels can post more frequently (5-10/day)

### Engagement
- Enable comments in channel settings for discussions
- Use polls for engagement
- Pin important announcements

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Bot not admin" | Bot missing admin permissions | Add bot as admin with `can_post_messages` |
| "Channel not found" | Wrong channel name/ID | Verify `@channelname` or numeric chat ID |
| `MEDIA_CAPTION_TOO_LONG` | Caption > 1,024 chars | Shorten caption or use text-only post |
| "Bad Request: file is too big" | File > 50 MB | Compress video/image to under 50 MB |
| "Mixed media not supported" | Images + video in same post | Use one media type per post |

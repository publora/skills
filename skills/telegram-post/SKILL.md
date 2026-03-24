---
name: telegram-post
description: Post to Telegram channels and groups with markdown formatting and media via Publora MCP
---

# Telegram Post

Create and schedule posts to Telegram channels and groups using the Publora MCP server. Supports rich markdown formatting, photos, videos, documents, and silent posting.

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
| Text message | 4,096 characters |
| Media caption | 1,024 characters |
| Photos | JPG, PNG, GIF (up to 10 MB) |
| Videos | MP4, up to 2 GB, 50 MB for streaming |
| Documents | Any format, up to 2 GB |

## Available Tools

### create_post
Create a new Telegram post.

**Parameters:**
- `platform`: "telegram"
- `content`: Message text (supports markdown)
- `scheduled_at` (optional): ISO 8601 datetime
- `media_ids` (optional): Uploaded media IDs
- `platform_settings` (optional): Telegram-specific options

### Platform Settings

```json
{
  "disableNotification": true,    // Silent message
  "disableWebPagePreview": true,  // No link preview
  "protectContent": true          // Disable forwarding/saving
}
```

### get_upload_url
Get presigned URL for media uploads.

### list_posts
List scheduled and published Telegram posts.

## Markdown Formatting

Telegram uses its own markdown flavor:

| Format | Syntax | Result |
|--------|--------|--------|
| Bold | `*bold*` | **bold** |
| Italic | `_italic_` | *italic* |
| Code | `` `code` `` | `code` |
| Link | `[text](url)` | [text](url) |
| Code block | ``` ```code``` ``` | Code block |

**Note**: Telegram markdown differs from standard markdown. Use single asterisks for bold, underscores for italic.

## Examples

### Simple Channel Post
```
Post this to my Telegram channel:
"New blog post published: How to Build a Personal Brand in 2024"
```

### Formatted Announcement
```
Create a Telegram post with this formatting:
*Important Update*

We're launching our new feature tomorrow at 10 AM UTC.

_What's new:_
- Feature A
- Feature B

[Read the full announcement](https://example.com/update)
```

### Silent Post (No Notification)
```
Post this to Telegram silently (no notification to subscribers):
"Daily digest: Today's top 5 articles..."
```

### Post with Image
```
Post this image to my Telegram channel with caption:
"Our team at the conference! Great discussions on AI in healthcare."
```

### Scheduled Post
```
Schedule this for tomorrow at 8 AM Moscow time:
"Good morning! Here's your daily market summary..."
```

### Protected Content
```
Post this as protected content (no forwarding/saving):
"Exclusive content for channel members only..."
```

## Bot vs MTProto

Publora supports both connection types:

| Feature | Bot API | MTProto |
|---------|---------|---------|
| Setup | Easy (BotFather token) | Advanced (app credentials) |
| Post as | Bot name | Your personal name |
| Channels | Bot must be admin | Direct access |
| Rate limits | Moderate | Higher |

Most users use Bot API. Connect via Publora dashboard.

## Best Practices

### Content
1. **Use formatting**: Bold headlines, italic emphasis improves readability
2. **Link previews**: Great for articles; disable for cleaner announcements
3. **Emoji usage**: Common and expected on Telegram
4. **Post length**: No penalty for longer posts; be comprehensive

### Timing
- **Global audience**: Telegram users are worldwide; consider multiple timezone posts
- **Best times**: 8-10 AM, 12-2 PM, 7-9 PM in target regions
- **Frequency**: Channels can post more frequently than other platforms (5-10/day)

### Engagement
- Enable comments in channel settings for discussions
- Use polls for engagement
- Pin important announcements

## Troubleshooting

- **"Bot not admin"**: Ensure your bot is added as admin to the channel/group
- **"Channel not found"**: Verify channel username or ID in Publora settings
- **"Message too long"**: Text posts max 4,096 chars; captions max 1,024
- **"Media not supported"**: Check format and size against limits

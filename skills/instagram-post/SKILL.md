---
name: instagram-post
description: Post to Instagram with images, carousels, Reels, and Stories via Publora MCP (Business account required)
---

# Instagram Post

Create and schedule Instagram posts using the Publora MCP server. Supports image posts, carousels (2-10 images), Reels, and Stories. Requires an Instagram Business account.

## Prerequisites

**Plans:** Free Starter (15 posts/month), Pro, Premium

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register) (free)
2. **Convert to Business account** in Instagram settings (Personal and Creator accounts are NOT supported by the API)
3. **Connect Instagram** via OAuth in [Publora Dashboard](https://publora.com/dashboard)
4. **Get API key** at [publora.com/settings/api](https://publora.com/settings/api)
5. **Configure MCP** in Claude Desktop (`~/.claude/claude_desktop_config.json`):

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

# Create a post
curl -X POST "https://api.publora.com/api/v1/create-post" \
  -H "x-publora-key: sk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["instagram-11223344"],
    "content": "Your caption here #hashtag",
    "scheduledTime": "2026-03-25T10:00:00Z"
  }'
```

**Platform ID Format:** `instagram-{id}` where `{id}` is from `/platform-connections` response.

Example IDs: `instagram-11223344`, `instagram-55667788`

📖 **Full API documentation:** [docs.publora.com](https://docs.publora.com)

### Plan Limits

| Plan | Posts/month | Price |
|------|-------------|-------|
| Starter | 15 | Free |
| Pro | 100/account | $2.99/account/month |
| Premium | 500/account | $9.99/account/month |

## Platform Limits (API vs Native App)

These limits are specific to the Instagram Graph API and differ from native app limits:

### Images

| Feature | API Limit |
|---------|-----------|
| **Formats** | **JPEG only** (PNG is NOT supported and will fail!) |
| Max file size | 8 MB |
| Carousel images | 2-10 (native app allows 20) |
| Aspect ratios | 4:5 (portrait) to 1.91:1 (landscape) |

### Videos

| Feature | Reels | Stories | Carousel Videos |
|---------|-------|---------|-----------------|
| Max duration | **15 minutes** (only 5-90s eligible for Reels tab) | 60 seconds | 60 seconds |
| Min duration | 3 seconds | 3 seconds | 3 seconds |
| Max file size | 300 MB | 100 MB | 300 MB |
| Formats | MP4, MOV | MP4, MOV | MP4, MOV |

### Captions

| Feature | Limit |
|---------|-------|
| Caption length | 2,200 characters |
| Visible before "more" | First 125 characters |
| Hashtags | 30 per post (included in caption) |

### Rate Limits

- **50 posts per 24 hours** (some accounts report 25)

## Available Tools

### create_post
Create a new Instagram post.

**Parameters:**
- `platforms`: Array with your Instagram connection ID (e.g., `["instagram-11223344"]`)
- `content`: Caption text (up to 2,200 characters)
- `scheduledTime`: ISO 8601 datetime (**required** - for immediate posting, use current time + 1 minute)

### get_upload_url
Get presigned URL for media uploads.

**Parameters:**
- `postGroupId`: Post ID to attach media to
- `fileName`: File name (e.g., "photo.jpg")
- `contentType`: Must be `image/jpeg` for images, `video/mp4` for video
- `type`: `"image"` or `"video"`

### list_posts / update_post / delete_post
Manage scheduled and draft posts.

## Video Type Settings (via REST API)

Control how videos are published via `platformSettings`:

```json
{
  "platformSettings": {
    "instagram": {
      "videoType": "REELS"
    }
  }
}
```

| Setting | Values | Default | Description |
|---------|--------|---------|-------------|
| `videoType` | `"REELS"`, `"STORIES"` | `"REELS"` | Determines how videos are published |

Note: `platformSettings` is not available via MCP - use REST API for video type control.

## Examples

### Single Image Post
```
Post this to Instagram:
"Morning coffee and code. Best way to start the day. #devlife #coding"

[Attach JPEG image]
```
**Important:** Image must be JPEG format. PNG will be rejected.

### Carousel Post
```
Create an Instagram carousel with these 5 product screenshots.
Caption: "Our app evolution over 6 months. Swipe to see the journey! #buildinpublic"
```
Note: Requires 2-10 JPEG images. Cannot mix images and videos in carousels.

### Reel
```
Post this video as a Reel:
"60-second tutorial on our new feature. #tutorial #app"
```
Videos default to Reels. Set `videoType: "STORIES"` via REST API for Stories.

### Story
```
Post this 30-second clip as a Story (will disappear after 24 hours).
```
Requires `platformSettings.instagram.videoType: "STORIES"` via REST API.

### Scheduled Post
```
Schedule this for tomorrow at 10 AM:
"New feature announcement coming soon! Stay tuned."
[Attach JPEG image]
```

## Important Restrictions

1. **JPEG only for images**: PNG, GIF, WebP are NOT supported by the Instagram API. Convert to JPEG before uploading.

2. **Business account required**: Personal and Creator accounts cannot post via API. Only Business accounts work.

3. **Media required on every post**: Instagram does not support text-only posts. Every post needs at least one image or video.

4. **No mixed media in carousels**: A carousel must be either all images OR all videos (via separate posts), not both.

5. **Stories disappear**: Stories are ephemeral and disappear after 24 hours.

6. **Reel is the default**: Videos are published as Reels by default. To post a Story, use the REST API with `videoType: "STORIES"`.

## Best Practices

### Content
1. **First 125 chars matter**: This is what users see before tapping "more"
2. **Hashtag strategy**: Use 5-15 relevant hashtags (max 30)
3. **Image quality**: Use high-quality JPEG images for best results
4. **Carousel engagement**: Carousels get higher engagement than single images

### Timing
- **Best times**: 11 AM - 1 PM, 7 PM - 9 PM in target timezone
- **Frequency**: 1-2 posts per day for growth
- **Reels boost**: Reels get algorithmic preference over static images

### Engagement
- Reply to comments within the first hour
- Use location tags when relevant
- Cross-promote from Stories to Feed

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Business account required" | Using Personal/Creator account | Convert to Business account in Instagram settings |
| "Invalid image format" | PNG or other non-JPEG format | Convert image to JPEG before uploading |
| "Media upload failed" | File too large or wrong format | Check: images < 8 MB JPEG, videos < 300 MB MP4 |
| "Carousel requires 2-10 items" | Wrong number of images | Ensure 2-10 images for carousel |
| "Account not connected" | OAuth expired | Reconnect via Publora dashboard |
| Rate limit (429) | Exceeded 50 posts/day | Wait 24 hours |

---
name: bluesky-post
description: Post to Bluesky with rich text facets, images, videos, and alt text support via Publora MCP
---

# Bluesky Post

Create and schedule posts to Bluesky using the Publora MCP server. Supports text posts with auto-detected hashtags and URLs, images with alt text, and videos.

## Prerequisites

**Plans:** Free Starter (15 posts/month), Pro, Premium

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register) (free)
2. **Generate app password** in Bluesky Settings > App Passwords (NOT your main password)
3. **Connect Bluesky** in [Publora Dashboard](https://publora.com/dashboard) using your handle + app password
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
    "platforms": ["bluesky-did:plc:abc123xyz"],
    "content": "Your post content here",
    "scheduledTime": "2026-03-25T10:00:00Z"
  }'
```

**Platform ID Format:** `bluesky-{did}` where `{did}` is from `/platform-connections` response.

Example IDs: `bluesky-did:plc:abc123xyz`, `bluesky-did:plc:def456uvw`

📖 **Full API documentation:** [docs.publora.com](https://docs.publora.com)

### Plan Limits

| Plan | Posts/month | Price |
|------|-------------|-------|
| Starter | 15 | Free |
| Pro | 100/account | $2.99/account/month |
| Premium | 500/account | $9.99/account/month |

## Platform Limits

| Feature | Limit |
|---------|-------|
| Characters | 300 |
| Images | Up to 4 per post |
| Image size | ~1 MB (976.56 KB) |
| Video duration | 3 minutes |
| Video size | 50-100 MB (based on duration) |
| Videos per day | 25 |
| Alt text | 2,000 characters per image |

### Video Size Tiers

| Duration | Max Size |
|----------|----------|
| Under 60s | 50 MB |
| 60s - 3min | 100 MB |

## Rich Text Facets

Bluesky uses a unique rich text system. Publora handles the complexity automatically:

- **Hashtags**: `#hashtag` auto-detected and made clickable
- **URLs**: Any URL auto-detected and made clickable
- **Byte offsets**: Calculated correctly for multi-byte characters (emojis, CJK)

No special formatting needed - just write naturally.

## Available Tools

### create_post
Create a new Bluesky post.

**Parameters:**
- `platforms`: Array with your Bluesky connection ID (e.g., `["bluesky-did:plc:abc123xyz"]`)
- `content`: Post text (up to 300 characters)
- `scheduledTime`: ISO 8601 datetime (**required** - for immediate posting, use current time + 1 minute)
- `altTexts`: Array of alt text for images (optional)

### get_upload_url
Get presigned URL for media uploads.

**Parameters:**
- `postGroupId`: Post ID to attach media to
- `fileName`: File name (e.g., "photo.jpg")
- `contentType`: `image/jpeg`, `image/png`, `video/mp4`
- `type`: `"image"` or `"video"`

### list_posts / update_post / delete_post
Manage scheduled and draft posts.

## Examples

### Simple Post with Hashtags
```
Post this to Bluesky:
"Just launched our new API documentation! Check it out at https://docs.example.com #devtools #api"
```
Hashtags and URLs are automatically made clickable.

### Post with Image and Alt Text
```
Post this to Bluesky with a dashboard screenshot:
"Our new analytics view is live! #buildinpublic"

Alt text: "Screenshot of analytics dashboard showing user growth charts"
```

### Multiple Images
```
Create a Bluesky post with before/after comparison images:
"Office renovation complete! What a transformation."
```
Note: Up to 4 images allowed per post.

### Video Post
```
Post this 60-second demo video to Bluesky:
"Quick tour of our new mobile app features"
```

### Scheduled Post
```
Schedule this for tomorrow at 10 AM:
"Good morning! Here's your daily productivity tip..."
```

## Important Restrictions

1. **App password required**: You must use a Bluesky app password, NOT your main account password. Generate one at Settings > App Passwords.

2. **All images converted to JPEG**: Regardless of input format (PNG, WebP, GIF), all images are converted to JPEG before upload.

3. **~1 MB image limit**: The AT Protocol enforces a strict ~1 MB limit. Compress images to 80-85% JPEG quality.

4. **DID-based platform ID**: Unlike other platforms using numeric IDs, Bluesky uses `did:plc:xxx` format.

5. **Email verification for video**: You must verify your email in Bluesky before uploading videos.

6. **25 video daily limit**: Maximum 25 videos OR 10 GB per day.

## Best Practices

### Content
1. **Concise posts**: 300 chars is shorter than Twitter - be punchy
2. **Natural hashtags**: 1-2 relevant hashtags work well
3. **Alt text**: Always add alt text for accessibility
4. **URLs work**: Links are clickable (unlike some platforms)

### Timing
- **Growing platform**: Less crowded than X, easier to get noticed
- **Tech-savvy audience**: Developer and early-adopter heavy
- **Frequency**: 1-3 posts per day

### Engagement
- Bluesky favors authentic conversation
- Reply to comments to build community
- Follow relevant users to grow network

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid credentials" | Wrong password type | Use app password, not main password |
| "Image too large" | Over ~1 MB | Compress to 80-85% JPEG quality |
| "Content too long" | Over 300 chars | Shorten content (no auto-threading) |
| "Video daily limit" | 25 videos reached | Wait 24 hours |
| "Email not verified" | Trying to upload video | Verify email in Bluesky settings |

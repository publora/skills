---
name: tiktok-post
description: Upload videos to TikTok with privacy controls and interaction settings via Publora MCP
---

# TikTok Post

Upload and schedule videos to TikTok using the Publora MCP server. Supports privacy controls, interaction settings (comments, duet, stitch), and commercial content disclosure.

## Prerequisites

**Plans:** Free Starter (15 posts/month), Pro, Premium

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register) (free)
2. **Connect TikTok** via OAuth in [Publora Dashboard](https://publora.com/dashboard)
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

# Create a post
curl -X POST "https://api.publora.com/api/v1/create-post" \
  -H "x-publora-key: sk_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "platforms": ["tiktok-99887766"],
    "content": "Video caption here #hashtag",
    "scheduledTime": "2026-03-25T10:00:00Z",
    "platformSettings": {
      "tiktok": {
        "viewerSetting": "PUBLIC_TO_EVERYONE",
        "allowComments": true
      }
    }
  }'
```

**Platform ID Format:** `tiktok-{id}` where `{id}` is from `/platform-connections` response.

Example IDs: `tiktok-99887766`, `tiktok-123456789`

📖 **Full API documentation:** [docs.publora.com](https://docs.publora.com)

### Plan Limits

| Plan | Posts/month | Price |
|------|-------------|-------|
| Starter | 15 | Free |
| Pro | 100/account | $2.99/account/month |
| Premium | 500/account | $9.99/account/month |

## Platform Limits (API vs Native App)

**Critical API limits that differ from native TikTok app:**

### Video Requirements

| Specification | API Limit | Native App |
|---------------|-----------|------------|
| **Max duration** | **10 minutes** | 60 minutes |
| Min duration | 3 seconds | 3 seconds |
| Max file size | 4 GB | 4 GB |
| Min frame rate | **23 FPS** | 23 FPS |
| Formats | MP4, MOV, WebM | MP4, MOV, WebM |

### Caption Limits

| Element | API Limit | Native App |
|---------|-----------|------------|
| Caption length | **2,200 characters** | 4,000 characters |
| Hashtags | Included in caption count | Included in caption count |

### Rate Limits

| Limit | Value |
|-------|-------|
| Posts per day | 15-20 |
| Videos per minute | Max 2 |

## Available Tools

### create_post
Create a new TikTok post.

**Parameters:**
- `platforms`: Array with your TikTok connection ID (e.g., `["tiktok-99887766"]`)
- `content`: Video caption (up to 2,200 characters)
- `scheduledTime`: ISO 8601 datetime

### get_upload_url
Get presigned URL for video upload.

**Parameters:**
- `postGroupId`: Post ID to attach video to
- `fileName`: Video file name (e.g., "video.mp4")
- `contentType`: `video/mp4`, `video/quicktime`, or `video/webm`
- `type`: `"video"`

### list_posts / update_post / delete_post
Manage scheduled and draft posts.

## Platform Settings (via REST API)

TikTok has 7 platform-specific settings controlled via `platformSettings`:

```json
{
  "platformSettings": {
    "tiktok": {
      "viewerSetting": "PUBLIC_TO_EVERYONE",
      "allowComments": true,
      "allowDuet": false,
      "allowStitch": false,
      "commercialContent": false,
      "brandOrganic": false,
      "brandedContent": false
    }
  }
}
```

### Viewer Settings (Required)

| Value | Description |
|-------|-------------|
| `PUBLIC_TO_EVERYONE` | Anyone can view (default) |
| `MUTUAL_FOLLOW_FRIENDS` | Only mutual followers |
| `FOLLOWER_OF_CREATOR` | Only your followers |
| `SELF_ONLY` | Only you (draft-like) |

### Interaction Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `allowComments` | `true` | Whether viewers can comment |
| `allowDuet` | `false` | Whether viewers can create Duets |
| `allowStitch` | `false` | Whether viewers can Stitch |

### Commercial Content Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `commercialContent` | `false` | Is this commercial content? |
| `brandOrganic` | `false` | Organic brand promotion |
| `brandedContent` | `false` | Paid partnership/sponsored |

**Note:** If `commercialContent` is `true`, at least one of `brandOrganic` or `brandedContent` must also be `true`.

Note: `platformSettings` is not available via MCP - use REST API for these settings.

## Critical Restrictions

### 1. Unaudited Apps = PRIVATE Only

**CRITICAL:** If your TikTok app hasn't passed TikTok's review process, you can **ONLY post PRIVATE videos** (`SELF_ONLY`). All other `viewerSetting` values will be overridden to `SELF_ONLY`.

To post public videos, your app must be audited by TikTok.

### 2. Video Only Platform

TikTok does NOT support:
- Text-only posts
- Image posts
- Photo carousels

Every post must include a video.

### 3. Minimum 23 FPS

Videos below 23 frames per second will be rejected by TikTok.

## Examples

### Basic Video Post
```
Post this video to TikTok:
"How we built our startup in 60 seconds #startup #tech #coding"
```

### Private Draft (Testing)
```
Upload this video as a private draft to TikTok (only I can see it):
"Testing new content format"
```
Use `viewerSetting: "SELF_ONLY"` for testing before making public.

### Branded Content
```
Post this sponsored video to TikTok with proper disclosure:
"Loving this new product from @brand! #ad #sponsored"
```
Set `commercialContent: true` and `brandedContent: true` for paid partnerships.

### Scheduled Post
```
Schedule this TikTok video for tomorrow at 6 PM:
"Weekend vibes incoming! #weekend #fun"
```

## Supported Video Formats

| Format | Recommended | Notes |
|--------|-------------|-------|
| MP4 | Yes | Most reliable |
| MOV | Yes | Apple format |
| WebM | Yes | Web format |
| AVI | Accepted by Publora | May be rejected by TikTok |
| MKV | Accepted by Publora | May be rejected by TikTok |

**Recommendation:** Use MP4 for best compatibility.

## Best Practices

### Content
1. **Hook in first 3 seconds**: Grab attention immediately
2. **Optimal length**: 15-60 seconds for best engagement
3. **Trending sounds**: Use trending audio when possible
4. **Hashtag strategy**: 3-5 relevant hashtags

### Technical
1. **Vertical video**: 9:16 aspect ratio performs best
2. **High quality**: At least 720p resolution
3. **23+ FPS**: Ensure smooth playback
4. **MP4 format**: Most reliable format

### Timing
- **Best times**: 7-9 AM, 12-3 PM, 7-11 PM in target timezone
- **Frequency**: 1-3 posts per day for growth
- **Consistency**: Regular posting schedule helps algorithm

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `unaudited_client_can_only_post_to_private_accounts` | App not approved | Submit app for TikTok review or use `SELF_ONLY` |
| `spam_risk_too_many_posts` | Daily limit reached | Wait 24 hours |
| `duration_check_failed` | Video too long/short | Ensure 3 seconds to 10 minutes |
| `file_format_check_failed` | Wrong video format | Use MP4, MOV, or WebM |
| "23 FPS required" | Low frame rate | Re-encode video at 23+ FPS |
| "TikTok requires selecting who can view" | Missing viewerSetting | Always include `viewerSetting` in platformSettings |

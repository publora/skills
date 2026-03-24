---
name: social-post
description: Post to YouTube, Facebook Pages, and Mastodon via Publora MCP - unified skill for video and fediverse platforms
---

# Social Post (YouTube, Facebook, Mastodon)

Create and schedule posts to YouTube, Facebook Pages, and Mastodon using the Publora MCP server. This skill covers platforms that work through standard posting without platform-specific complexity.

## Prerequisites

**Plans:** Free Starter (15 posts/month), Pro, Premium

### Getting Started

1. **Create account** at [publora.com/register](https://publora.com/register) (free)
2. **Connect platforms** via OAuth in [Publora Dashboard](https://publora.com/dashboard):
   - **YouTube**: Google OAuth (requires YouTube channel)
   - **Facebook**: Facebook OAuth (Pages only, not personal profiles)
   - **Mastodon**: OAuth (mastodon.social instance)
3. **Get API key** at [publora.com/settings/api](https://publora.com/settings/api)
4. **Configure MCP** in Claude Desktop (`~/.claude/claude_desktop_config.json`):

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

### Plan Limits

| Plan | Posts/month | Price |
|------|-------------|-------|
| Starter | 15 | Free |
| Pro | 100/account | $2.99/account/month |
| Premium | 500/account | $9.99/account/month |

---

## YouTube

**Video-only platform** - every post requires a video file.

### Platform Limits

| Feature | Limit |
|---------|-------|
| Video title | 100 characters |
| Video description | 5,000 characters |
| Video duration | 12 hours |
| Video size | 512 MB (Publora limit) |
| Video formats | MP4, MOV, AVI, MKV, WebM |

### Platform Settings (via REST API)

```json
{
  "platformSettings": {
    "youtube": {
      "privacy": "public",
      "title": "My Video Title"
    }
  }
}
```

| Setting | Values | Default |
|---------|--------|---------|
| `privacy` | `"public"`, `"unlisted"`, `"private"` | `"public"` |
| `title` | string | Derived from first 70 chars of content |

Note: `platformSettings` is not available via MCP - use REST API for these settings.

### YouTube Examples

```
Upload this tutorial video to YouTube:
"How to Build a REST API in 10 Minutes - Complete guide for beginners"
```

```
Upload this as an unlisted video (for internal sharing):
"Internal demo - Q1 dashboard features"
```

### YouTube Restrictions

1. **Video required**: YouTube does not support text-only or image posts
2. **Single video only**: One video per post
3. **Processing time**: Videos take seconds to minutes to process after upload
4. **Token refresh**: YouTube tokens expire after ~6 months, reconnect if needed

---

## Facebook

**Pages only** - posts go to Facebook Pages, not personal profiles.

### Platform Limits

| Feature | Limit |
|---------|-------|
| Post text | 2,200 characters (frontend) / 63,206 (API) |
| Images | Up to 10 per post |
| Image size | 10 MB |
| Video duration | 45 minutes |
| Video size | 512 MB (Publora limit) |

### Multi-Page Support

If you manage multiple Facebook Pages, each gets its own platform ID:
- `facebook-112233445566` (Page 1)
- `facebook-778899001122` (Page 2)

You can post to multiple pages in a single request.

### Facebook Examples

```
Post this announcement to my Facebook Page:
"We're thrilled to announce our new product launch! Visit our website to learn more."
```

```
Post this to both my Facebook Pages:
"Holiday notice: Our offices will be closed on Monday."
```

```
Share these event photos on Facebook:
"Highlights from our company retreat! Great team, great memories."
```

### Facebook Restrictions

1. **Pages only**: Cannot post to personal profiles via API
2. **WebP auto-converted**: WebP images become JPEG automatically
3. **59-day token**: Tokens auto-refresh, but may need reconnection if it fails
4. **No mixed media**: A post can have images OR video, not both

---

## Mastodon

**Fediverse platform** - posts federate across the decentralized network.

### Platform Limits

| Feature | Limit |
|---------|-------|
| Post text | 500 characters |
| Images | Up to 4 per post |
| Image size | 16 MB |
| Video size | ~99 MB |
| Image formats | JPEG, PNG, GIF, WebP |
| Video formats | MP4, WebM, MOV |

### Mastodon Examples

```
Post this to Mastodon:
"Hello fediverse! We just shipped a major update to our open-source project. #opensource"
```

```
Share this screenshot on Mastodon:
"New feature: dark mode is here! #ui #darkmode"
```

### Mastodon Restrictions

1. **mastodon.social only**: Currently connects only to mastodon.social instance
2. **Public visibility**: All posts are public by default
3. **No auto-threading**: Unlike X/Twitter, Mastodon doesn't split long content
4. **500-char strict**: Content over 500 characters will be rejected

---

## Available Tools (All Platforms)

### create_post
Create a new post on any platform.

**Parameters:**
- `platforms`: Array of platform IDs (e.g., `["youtube-UCxxx", "facebook-123", "mastodon-456"]`)
- `content`: Post text
- `scheduledTime`: ISO 8601 datetime

### get_upload_url
Get presigned URL for media uploads.

**Parameters:**
- `postGroupId`: Post ID to attach media to
- `fileName`: File name
- `contentType`: MIME type
- `type`: `"image"` or `"video"`

### list_posts / update_post / delete_post
Manage scheduled and draft posts.

---

## Cross-Platform Posting

Post to multiple platforms at once:

```
Post this video to YouTube and this text to Facebook and Mastodon:
"Announcing our new feature - watch the demo!"
```

Publora handles platform-specific requirements automatically:
- YouTube gets the video with title/description
- Facebook gets the text + video
- Mastodon gets the text (500 char limit applies)

---

## Troubleshooting

| Platform | Error | Solution |
|----------|-------|----------|
| YouTube | "Video required" | Attach a video file |
| YouTube | "Account disconnected" | Reconnect via dashboard |
| Facebook | "Page not found" | Verify page connection |
| Facebook | "Token expired" | Reconnect page in dashboard |
| Mastodon | "Content too long" | Shorten to under 500 chars |
| Mastodon | "Too many images" | Reduce to 4 or fewer |
| All | Rate limit errors | Wait and retry |

---
name: linkedin-post
description: Create, schedule, and manage LinkedIn posts with AI assistance via Publora MCP
---

# LinkedIn Post

Create and schedule LinkedIn posts using the Publora MCP server. Supports text posts, images, videos, documents, and carousels.

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

### create_post
Create a new post for LinkedIn (or schedule for later).

**Parameters:**
- `platform`: "linkedin"
- `content`: Post text (up to 3,000 characters for LinkedIn)
- `scheduled_at` (optional): ISO 8601 datetime for scheduling
- `media_ids` (optional): Array of uploaded media IDs

### get_upload_url
Get a presigned URL to upload media (images, videos, documents).

**Parameters:**
- `filename`: Name of the file (e.g., "chart.png")
- `content_type`: MIME type (e.g., "image/png", "video/mp4", "application/pdf")

### list_posts
List your scheduled and published posts.

**Parameters:**
- `platform` (optional): Filter by "linkedin"
- `status` (optional): "scheduled", "published", "draft"

### update_post
Update a scheduled post before it's published.

### delete_post
Delete a scheduled or draft post.

## Examples

### Simple Text Post
```
Create a LinkedIn post announcing our new product launch:
"We're thrilled to announce the release of our AI writing assistant..."
```

### Post with Image
```
1. First, upload the image using get_upload_url
2. Then create the post with the media_id
```

### Schedule a Post
```
Schedule this LinkedIn post for tomorrow at 9 AM EST:
"5 lessons learned from scaling our startup to 100 employees..."
```

### Carousel Post
Upload multiple images and include all media_ids in the create_post call.

## Best Practices

1. **Optimal posting times**: Tuesday-Thursday, 8-10 AM or 12 PM in your audience's timezone
2. **Character limits**: LinkedIn allows up to 3,000 characters, but posts under 1,300 perform better
3. **Hashtags**: Use 3-5 relevant hashtags at the end of your post
4. **First line hook**: Make the first 2 lines compelling - they appear before "see more"
5. **Call to action**: End with a question or clear CTA to boost engagement

## Supported Media Types

| Type | Formats | Max Size |
|------|---------|----------|
| Image | JPG, PNG, GIF | 8 MB |
| Video | MP4 | 200 MB, 10 min |
| Document | PDF | 100 MB |

## Troubleshooting

- **"Account not connected"**: Ensure your LinkedIn account is connected in Publora dashboard
- **"Rate limited"**: LinkedIn limits posting frequency; wait before retrying
- **"Media upload failed"**: Check file size and format against supported types

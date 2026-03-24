# Publora Skills for Agent Systems

Official agent skills for [Publora](https://publora.com) - the AI-powered social media management platform.

## Installation

```bash
# Install all skills
npx skills add publora/skills

# Install specific skill
npx skills add publora/skills --skill linkedin-post
npx skills add publora/skills --skill linkedin-analytics
npx skills add publora/skills --skill threads-post
npx skills add publora/skills --skill telegram-post
npx skills add publora/skills --skill instagram-post
npx skills add publora/skills --skill tiktok-post
```

## Available Skills

### [linkedin-post](./skills/linkedin-post/SKILL.md)
Create, schedule, and manage LinkedIn posts. Supports text, images, videos, documents, and carousels.

### [linkedin-analytics](./skills/linkedin-analytics/SKILL.md)
Analyze LinkedIn performance - track post engagement, follower growth, and get content strategy insights. Includes engagement tools (reactions, comments).

### [threads-post](./skills/threads-post/SKILL.md)
Post to Meta's Threads with auto-threading for long content, carousels, and scheduled posting.

### [telegram-post](./skills/telegram-post/SKILL.md)
Post to Telegram channels and groups with markdown formatting, media support, and silent posting options.

### [instagram-post](./skills/instagram-post/SKILL.md)
Post to Instagram with images, carousels, Reels, and Stories. Business account required. JPEG images only (PNG not supported by API).

### [tiktok-post](./skills/tiktok-post/SKILL.md)
Upload videos to TikTok with privacy controls and interaction settings. Video-only platform with extensive platformSettings.

## Prerequisites

All skills require the Publora MCP server. Add to your Claude Desktop config:

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

## Supported Platforms

Publora supports 10 social platforms:
- LinkedIn (posting + analytics + engagement)
- X/Twitter
- Instagram
- Threads
- TikTok
- YouTube
- Facebook
- Bluesky
- Mastodon
- Telegram

## Links

- [Publora Website](https://publora.com)
- [Documentation](https://docs.publora.com)
- [MCP Tools Reference](https://docs.publora.com/mcp/tools-reference)
- [API Documentation](https://docs.publora.com/api)

## License

MIT

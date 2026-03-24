# Publora Skills for Agent Systems

Official agent skills for [Publora](https://publora.com) - the AI-powered social media management platform.

## Quick Start

### Step 1: Create Publora Account

Sign up for free at [publora.com/register](https://publora.com/register)

### Step 2: Choose Your Plan

| Plan | Price | Posts | Platforms |
|------|-------|-------|-----------|
| **Starter** | Free forever | 15/month | All platforms except X/Twitter |
| **Pro** | $2.99/account/month | 100/account | All 10 platforms |
| **Premium** | $9.99/account/month | 500/account | All 10 platforms |

**Note:** X/Twitter requires Pro or Premium plan. All other platforms work on free Starter.

### Step 3: Connect Your Social Accounts

1. Go to [Publora Dashboard](https://publora.com/dashboard)
2. Click "Connect Account" for each platform
3. Complete OAuth authorization (or bot setup for Telegram)

### Step 4: Get Your API Key

1. Go to [publora.com/settings/api](https://publora.com/settings/api)
2. Click "Create API Key"
3. Copy the key (you'll need it for MCP config)

### Step 5: Configure MCP Server

Add to your Claude Desktop config (`~/.claude/claude_desktop_config.json`):

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

### Step 6: Install Skills

```bash
# Install all skills
npx skills add publora/skills

# Or install specific skill
npx skills add publora/skills --skill linkedin-post
```

## Available Skills

### Posting Skills

#### [linkedin-post](./skills/linkedin-post/SKILL.md)
Create and schedule LinkedIn posts. Supports text, images, videos, documents.
**Plans:** Starter (free), Pro, Premium

#### [threads-post](./skills/threads-post/SKILL.md)
Post to Meta's Threads with auto-threading and carousels.
**Plans:** Starter (free), Pro, Premium

#### [telegram-post](./skills/telegram-post/SKILL.md)
Post to Telegram channels with markdown and media support.
**Plans:** Starter (free), Pro, Premium

#### [instagram-post](./skills/instagram-post/SKILL.md)
Post to Instagram with images, carousels, Reels, Stories. Business account required.
**Plans:** Starter (free), Pro, Premium

#### [tiktok-post](./skills/tiktok-post/SKILL.md)
Upload videos to TikTok with privacy and interaction controls.
**Plans:** Starter (free), Pro, Premium

#### [bluesky-post](./skills/bluesky-post/SKILL.md)
Post to Bluesky with rich text facets, images, videos, and alt text.
**Plans:** Starter (free), Pro, Premium

#### [x-post](./skills/x-post/SKILL.md)
Post to X (Twitter) with auto-threading, images, and videos.
**Plans:** Pro, Premium only (not available on Starter)

#### [social-post](./skills/social-post/SKILL.md)
Post to YouTube, Facebook Pages, and Mastodon - unified skill for video and fediverse platforms.
**Plans:** Starter (free), Pro, Premium

### Analytics Skills

#### [linkedin-analytics](./skills/linkedin-analytics/SKILL.md)
Analyze LinkedIn performance - engagement, followers, reactions, comments.
**Plans:** Starter (free), Pro, Premium

## Platform Support by Plan

| Platform | Starter (Free) | Pro | Premium |
|----------|----------------|-----|---------|
| LinkedIn | Yes | Yes | Yes |
| Bluesky | Yes | Yes | Yes |
| Threads | Yes | Yes | Yes |
| Instagram | Yes | Yes | Yes |
| TikTok | Yes | Yes | Yes |
| Telegram | Yes | Yes | Yes |
| YouTube | Yes | Yes | Yes |
| Facebook | Yes | Yes | Yes |
| Mastodon | Yes | Yes | Yes |
| **X/Twitter** | **No** | Yes | Yes |

Free Starter plan: 15 posts/month across all platforms (except X/Twitter which requires Pro).

## Skill Coverage

| Skill | Platforms | Special Features |
|-------|-----------|------------------|
| linkedin-post | LinkedIn | Documents, articles, scheduling |
| linkedin-analytics | LinkedIn | Engagement metrics, follower analytics |
| threads-post | Threads | Auto-threading, carousels |
| telegram-post | Telegram | Markdown, bot posting |
| instagram-post | Instagram | Reels, Stories, carousels (JPEG only) |
| tiktok-post | TikTok | Privacy controls, commercial disclosure |
| bluesky-post | Bluesky | Rich text facets, alt text |
| x-post | X/Twitter | Auto-threading, 280 chars, emoji counting |
| social-post | YouTube, Facebook, Mastodon | Video uploads, Pages, fediverse |

## Pricing FAQ

**Can I try for free?**
Yes! Starter plan is free forever with 15 posts/month on all platforms except X/Twitter.

**What about X/Twitter?**
X/Twitter requires Pro plan ($2.99/account/month) due to Twitter API costs.

**What happens when I exceed my post limit?**
You'll see a message that you've reached your monthly limit. Upgrade to Pro or wait for the next billing cycle.

**Can I upgrade anytime?**
Yes. Upgrade or downgrade from Settings. Changes take effect immediately.

## Links

- [Publora Website](https://publora.com)
- [Pricing](https://publora.com/pricing)
- [Documentation](https://docs.publora.com)
- [MCP Tools Reference](https://docs.publora.com/mcp/tools-reference)
- [API Documentation](https://docs.publora.com/api)

## License

MIT

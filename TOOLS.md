# TOOLS.md - Local Notes

## Model Architecture (Token Optimization)

| Model | Use For | How |
|-------|---------|-----|
| **Claude Opus** | Brain - orchestration, decisions, talking to Marko | Main session |
| **ChatGPT** | Planning, task breakdown | API/spawn |
| **Codex CLI** | Coding (high reasoning) | `codex --model o4-mini --reasoning-effort high` |
| **Grok** | X/Twitter search, social media | API |
| **Gemini** | Internet research, bulk processing | API (key in .env.local) |
| **Nano Banana** | Image generation | API |

**Flow:** Marko → Opus (brain) → spawns muscles → Opus reviews → delivers

## Coding Preference
**Use Codex CLI with extra high thinking for all coding tasks.**
- Command: `codex --model o4-mini --reasoning-effort high "task"`
- Or spawn with thinking: `sessions_spawn` with `thinking: "high"`

## IMPORTANT: Credentials Locations
- **Notion API Key:** `~/.config/notion/` (just cat the file)
- **Google Calendar:** `~/.config/gcal-pro/token.json`
- **Google Drive:** Use OAuth token from gcal-pro (has drive scope). Refresh via `/oauth2.googleapis.com/token`, then hit Drive API directly.

## Google Drive Folders
- **Kurios Automated Business:** `1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ`
- **MVA Carlos & Mark Partnership:** `1qshu4wTkayK-3C_h8nPEy_YWtWoaPAUX`

## Google Calendar
- **Authenticated as:** sierra@kuriosbrand.com
- **Marko's calendar ID:** mark@kuriosbrand.com (use this, not 'primary')
- **Access:** Read/write via gcal-pro skill
- **Token location:** ~/.config/gcal-pro/token.json

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## Notion - Sierra Workspace
- **Sierra Workspace Page ID:** `2f79371d-3030-8083-8ac8-c16af6cb0f07`
- **Sierra Documents Database ID:** `2f89371d-3030-8185-adbd-e6e4febece73`
- **Purpose:** Central knowledge base - reports, SOPs, resources, training, videos, tools
- **Use PATCH method** for adding blocks: `curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children"`

### Database Properties:
| Property | Type | Options |
|----------|------|---------|
| Name | title | (document title) |
| Type | select | Report, Analysis, Playbook, SOP, Resource, Training, Video, Tool, Template, Research, Strategy |
| Project | select | MVA Lead Gen, Concrete Rank & Rent, SEO, Paid Ads, Automation, General |
| Status | select | Draft, Final, Archived |
| Source | select | Jacky Chou, Internal, Partner, Course, External |
| Priority | select | High, Medium, Low |
| URL | url | (link to external resource) |
| Tags | multi_select | (flexible tagging) |
| Created | date | (creation date) |

### When to Use Each Type:
- **Report** - Analysis with findings (Mom Test, audits)
- **Playbook** - Actionable strategy guides
- **SOP** - Step-by-step procedures
- **Resource** - External links, tools, references
- **Training** - Courses, tutorials, learning materials
- **Video** - Video content links (YouTube, courses)
- **Tool** - Software, services, platforms
- **Template** - Reusable frameworks, scripts
- **Research** - Data, studies, market research
- **Strategy** - High-level plans and approaches

### Versioning Workflow:
When updating a document that already exists:
1. **Archive old version** - Set Status → "Archived"
2. **Create new version** - New page with updated content
3. **Set Version number** - Increment (1 → 2 → 3)
4. **Link via Replaces** - Point to the archived version for history
5. **Keep same Name** - So it's clear it's an update

This keeps history while surfacing only current/relevant docs.

## X/Twitter API (@markkodg)
- Credentials: `~/.config/x-api/credentials.json`
- User ID: 1198729883867848706
- OAuth 1.0a: Working (for posting)
- Script: `/home/ec2-user/clawd/scripts/x_tools.py`
- **READ:** Scrape (save API credits)
- **WRITE:** Use API (posting, replies, likes)

## DataForSEO API
- Login: mark@kuriosbrand.com
- Base64 auth: `bWFya0BrdXJpb3NicmFuZC5jb206YjI5MmI0YTVlNjg2YmM3NQ==`
- Usage: `curl -H "Authorization: Basic $BASE64" https://api.dataforseo.com/v3/...`
- Endpoints: SERP, Keywords, Backlinks, On-Page, Domain Analytics

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

---

Add whatever helps you do your job. This is your cheat sheet.

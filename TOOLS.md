# TOOLS.md - Local Notes

## Model Architecture (Token Optimization)

**Full routing config:** `/home/ec2-user/clawd/data/model-routing-config.json`

| Task | Model | Cost Tier | Command/How |
|------|-------|-----------|-------------|
| **Orchestration** | Claude Opus 4.5 | $$$$ | Main session - brain |
| **Coding** | Codex CLI (o4-mini) | $$ | `codex --model o4-mini --reasoning-effort high` |
| **Research** | Gemini 3 Flash | $ | spawn with model=gemini-3-flash |
| **X/Social** | Grok 4 Fast | $ | Native X access |
| **Bulk/Budget** | DeepSeek Chat | ¢ | spawn with model=deepseek-chat |
| **Fast/Simple** | Groq Llama 3.1 8B | ¢ | 840 TPS, instant |
| **Long Context** | Gemini 3 Pro | $$ | 2M context window |
| **Conversation** | Claude Sonnet 4.5 | $$ | Day-to-day execution |

**Task Keywords → Route:**
- `code|build|fix|debug` → Codex CLI
- `research|search|analyze` → Gemini Flash
- `tweet|twitter|social` → Grok
- `cheap|bulk|batch` → DeepSeek
- `quick|fast|simple` → Groq
- `plan|strategy|complex` → Opus (stay in main)
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

## Notion - Sierra Workspace (SOPs ONLY)
- **Sierra Workspace Page ID:** `2f79371d-3030-8083-8ac8-c16af6cb0f07`
- **Sierra Documents Database ID:** `2f89371d-3030-8185-adbd-e6e4febece73`
- **Purpose:** SOPs ONLY — Standard Operating Procedures for tasks Sierra does
- **NOT for:** Research, reports, memory, notes → Use Supermemory for that
- **Use PATCH method** for adding blocks: `curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children"`

### When to use Notion vs Supermemory:
| Content Type | Where |
|--------------|-------|
| SOPs / How-to procedures | Notion |
| Research / Analysis | Supermemory |
| Memory / Context | Supermemory |
| Reports | Supermemory |
| Meeting notes | Supermemory |

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

## Webshare Rotating Residential Proxies
- **Proxy list:** `~/.config/webshare/proxies.txt`
- **Format:** `host:port:username:password`
- **Host:** p.webshare.io:80
- **Username pattern:** dtwmetwu-[1-215084]
- **Password:** ww846x37mmd9
- **Usage:** `curl --proxy "http://dtwmetwu-1:ww846x37mmd9@p.webshare.io:80" [url]`
- **Python:** `proxies = {"http": "http://user:pass@p.webshare.io:80", "https": "..."}`

## Neon Postgres Database
- **Project:** texas-mva-site (`odd-math-10907968`)
- **Region:** aws-us-east-1
- **Database:** neondb
- **Credentials:** `~/.config/neon/credentials.json`
- **Connection:** `postgresql://neondb_owner:***@ep-summer-silence-ahgxcxho-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require`
- **Use for:** Dashboard backend, lead tracking, structured data

## Discord Channels
- **#general (agent squad):** `1467415347723501580`

## Go High Level (GHL)
- **Location ID:** OsNgWuy8oZzLbp5BXbnD (Kurios subaccount - both Mark & Carlos)
- **API Key:** pit-9c041df9-b51b-4c7b-9329-241b528dc726
- **API Base:** https://services.leadconnectorhq.com
- **Credentials file:** ~/.config/ghl/credentials.json
- **Use for:** Sales appointments (source of truth over Google Calendar)

### GHL Custom Fields Reference:
- `1ImINic5Ef3ntrFFkQgG` = Website
- `NXbhfJYvzPwItFz45HJ2` = Role/Title
- `PMLr40tWCz8J9NvA4sx8` = Intake Setup
- `QtNRYpA6MqH8HPcncxs2` = Firm Size
- `g5kONh6i8fwXT84iRNnx` = Target Cost Per Case

## RB2B (Website Visitor Identification)
- **Dashboard:** https://app.rb2b.com
- **Pixel:** Install on MVA landing pages
- **Webhook URL:** `https://webhook.kuriosbrand.com/rb2b/webhook`
- **Slack Channel:** #rb2b-notifications (C0A7RNYC6CF)
- **Match Rate:** 15-20% (free), 35-45% (Pro+)
- **Use for:** Identifying anonymous website visitors → enrich → outreach
- **Flow:** RB2B → Webhook → Qualify → BetterContact enrich → Slack → Lemlist/GHL
- **Note:** Replaces Leadpipe (2026-02-06) — Leadpipe had broken webhooks and no support

## BetterContact (Waterfall Lead Enrichment)
- **API Key:** `~/.config/bettercontact/credentials.json`
- **API Base:** https://app.bettercontact.rocks/api
- **Integrated with:** Lemlist (via BetterContact dashboard)
- **Use for:** Waterfall enrichment across 20+ providers for verified emails/phones
- **Added:** 2026-02-04

## Apollo.io (Sales Intelligence)
- **API Key:** t_j7hexbGUqksRuWZWi9hw
- **Use for:** Finding contacts, company info, lead enrichment
- **API Docs:** https://apolloio.github.io/apollo-api-docs/

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

## Lemlist (Email Outreach)
- **API Key:** `~/.config/lemlist/credentials.json`
- **API Base:** https://api.lemlist.com/api
- **Auth:** Basic auth with empty username, API key as password
- **Campaigns:** MVA Outreach Sequence, LinkedIn Messages, Mark's campaign
- **Limitations:** Leads endpoint returns 403 (may need plan upgrade or API permission)
- **Use for:** Campaign management, activity tracking, LinkedIn connection tracking

## Stripe API (KuriosBrand LLC)
- **Account ID:** acct_1MYcAaCzRJgQ28gJ
- **API Key:** ~/.config/stripe/credentials.json
- **Key type:** Restricted (read-only: balance, charges, customers, payouts, invoices, subscriptions)
- **Use for:** Revenue tracking, invoice history, loan repayment monitoring
- **Added:** 2026-02-04

### Stripe Capital Loan
- **Disbursed:** $4,200 on 01/23/2026
- **Total to repay:** $5,035 ($4,200 + $835 fee, 19.9% effective rate)
- **Remaining:** $4,705
- **Repayment:** 20% of every Stripe deposit (automatic, only affects deposits AFTER 01/23)

# Buyer Profile Scraper Agent

24/7 agent that scrapes Reddit, social media, and the web to continuously build and update buyer profiles for PI attorneys.

## Purpose
Based on the Mitch Wiggins framework, this agent finds:
- Pain points
- Complaints about vendors
- Decision-making patterns
- Pricing discussions
- What makes attorneys buy/not buy

## Data Sources

### Reddit Subreddits
- r/LawFirm - Main attorney community
- r/lawyers - General lawyer discussion
- r/personalinjury - PI specific
- r/lawschool - Future attorneys
- r/marketing - Legal marketing discussions
- r/SEO - Law firm SEO discussions

### Search Queries
- "personal injury lead generation"
- "law firm marketing vendor"
- "legal leads scam"
- "attorney intake"
- "PI lawyer marketing"
- "cases on demand" / "legal leads" (competitor mentions)

### Social Platforms
- X/Twitter - @mentions of lead gen companies
- LinkedIn - PI attorney discussions
- Facebook Groups - Law firm marketing groups

## Output
All findings get added to Notion Sierra Documents database:
- Type: Research
- Project: Sales
- Tags: Reddit, Pain Point, Buyer Profile, etc.

## Schedule
- Runs **every 2 hours** via cron (12x/day)
- **10-15 searches per run** = ~120-180 searches/day
- Cron ID: `buyer-profile-scraper`

## Requirements
⚠️ **Needs API Access:**
- Brave Search API key (for web search) - run `clawdbot configure --section web`
- OR Reddit API credentials (for direct scraping)

## Files
- `README.md` - This file
- `TASK.md` - Task instructions for the agent
- `queries.json` - Search queries and subreddits

## Status
✅ Cron job created (every 6 hours)
⏳ Needs Brave API key for web search functionality

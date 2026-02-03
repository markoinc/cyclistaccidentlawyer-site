# Build-in-Public Update: January 29 - February 1, 2026

## 📊 Dashboard & Infrastructure Builds

### Goals Dashboard (admin.kuriosbrand.com)
- **Live at:** admin.kuriosbrand.com
- **Password:** sierra2026 or kurios
- **Features:**
  - Real-time goal tracking (calls/day, cost/call, pipeline value)
  - 13 enriched prospects with close probabilities, avatars, recommended approaches
  - Auto-refresh every 60s + manual refresh
  - Next Actions section highlighting priority prospects
- **Tech:** Deployed via GitHub → Cloudflare Pages

### kuriosbrand.com Migration
- **Migrated from:** 10web.io (WordPress)
- **Migrated to:** Cloudflare Pages
- **Repo:** github.com/markoinc/kuriosbrand
- **Status:** ✅ Live with Supabase env vars configured
- **DNS:** kuriosbrand.com → kuriosbrandoriginal.pages.dev

### leads.kuriosbrand.com (Pending)
- **Repo:** github.com/markoinc/remix-of-kurios-lead-platform
- **Status:** Ready for deployment (npm lockfile fix, env vars, deploy)

---

## 🤖 Agent Workflows Created

### AI Intake Agent System (90% Complete)
**Location:** `/home/ec2-user/data/kurios-finish/automation/clawd-agents/`

**Components Built:**
1. **Context Loader** - 9,163 chars of business intel + 11 customer avatars
2. **Intake Agent** - Initial lead qualification via messaging
3. **Avatar Detector** - Identifies customer type (Fast Scaler, Tire Kicker, etc.)
4. **Voice Transcription** - Handles voice notes via Whisper API
5. **Main Server** - Routes conversations, manages state

**Cost Savings:**
- Traditional intake: $4,550-6,500/month
- AI Agent: $55-85/month
- **Monthly savings: $4,465-6,415 (98% reduction)**

**Status:** Built and tested, needs OpenAI API key in .env to activate

### Financial Agent Framework
**Location:** `/home/ec2-user/clawd/agents/financial/`
- Reads Google Sheets transaction data
- Parses September, November, December 2025 accounting
- Structure: Overview tab + individual account transaction tabs
- Waiting for January 2026 data to test

### GHL Sales Automation (5 Workflows Designed)
1. WF1: Appointment Booked (entry point)
2. WF2: No-Show Handler
3. WF3: Contract Flow
4. WF4: Closed Won
5. WF5: Nurture (Deal Lost)
- **Full guide:** `/home/ec2-user/clawd/data/ghl-implementation-guide.md`
- **63 existing workflows** analyzed and documented

---

## 🔬 Research Conducted

### MVA Lead Gen Funnel - Deep Dive
**Full funnel mapped:**
1. Meta Ads → Landing Page (8-12% expected conversion)
2. Multi-step form (CaseAssessmentForm.tsx)
3. Auto-qualification scoring (strong/moderate/weak/unlikely)
4. GHL webhook → automation pipeline
5. Intake/follow-up → booked call
6. Sales call → signed case → partner referral

**Satellite Site Network Discovered:**
- network-stats-1: Texas truck crash statistics (Astro)
- network-corridor-stats: Highway corridor data (Astro)
- mva-engine: Location-deployable template (Next.js)

### PI Vendor Intelligence Project
**Database Contents:**
- 48 raw data items scraped
- 3 vendors profiled (Alert Communications, Scorpion, Ruby Receptionist)
- 3 buyers profiled
- 4 scrape runs completed

**Key Market Intelligence:**
- AI Adoption: 37% of PI lawyers use AI, 19% of firms have legal-specific AI
- Rising Star: Supio AI - $250/case, Thomson Reuters partnership
- Market Battle: MyCase (affordable/simple) vs Clio (feature-rich/complex)
- Opportunity: Small PI firms are underserved market

### GHL Webhook Integration - Fully Mapped
**4 Form Types Discovered:**
1. LeadForm (homepage) - General inquiry
2. CalculatorForm - HIGH intent
3. CaseAssessmentForm - MEDIUM-HIGH
4. PoliceReportSubmissionForm - Specific need

**Lead Scoring Built-In:**
- Calculator + permanentDisability = +40 points
- Strong qualification + evidence = +30 points
- High medical bills (>$20K) = +15 points

### Pricing & Unit Economics Deep Dive
**COD Performance Sheet Updated:**
- State-by-state lead/case costs with 30%+10% markup (43% total)
- "30 Live Transfers in 30 Days" offer pricing calculated

| State | Sell Case (+43%) | Guarantee Case | Live Transfer Price |
|-------|------------------|----------------|---------------------|
| AZ/UT | $1,716 | $2,059 | $1,030 |
| NC | $2,145 | $2,574 | $1,287 |
| FL | $2,288 | $2,746 | $1,373 |
| TX | $2,646 | $3,175 | $1,588 |
| CA | $4,290 | $5,148 | $2,574 |

---

## 🧠 Memory/SOP Systems Built

### AGENTS.md Framework
- Comprehensive workspace management guide
- Memory management protocol (daily files + MEMORY.md long-term)
- Heartbeat automation protocol
- Group chat behavior rules
- Subagent spawning guidelines

### TOOLS.md - Local Notes System
**Model Architecture Defined:**
| Model | Use For |
|-------|---------|
| Claude Opus | Brain - orchestration, talking to Marko |
| ChatGPT | Planning |
| Codex CLI | Coding (high reasoning) |
| Grok | X/Twitter search |
| Gemini | Internet research |
| Nano Banana | Image gen |

**Credentials & API Documentation:**
- Notion API, Google Calendar, Google Drive
- X/Twitter API (@markkodg)
- DataForSEO API
- Webshare rotating residential proxies

### Notion Databases Created
- **GHL Documentation** (76 pages from crawl)
- **GHL Workflow Build Log** - tracking new builds
- **API Credentials (Private)**
- **Sierra Workspace** for SOPs

### Knowledge Bases Completed
1. **Meta Ads KB** - 38KB, 1,092 lines (YouTube + X research)
2. **SDR Bot KB** - 70KB, 1,788 lines (YouTube + X research)
3. **Alex Finn Knowledge** - Top 10 productivity suggestions from transcriptions
4. **Jacky Chou SOP** - Episode 751 transcribed with competitor ad scraping, Reddit warm-up

---

## 📈 Key Discoveries

### 5 Growth Initiatives for 2026
1. **Call Cost Reduction:** $250 → <$100 via AI voice/appointment setters
2. **SEO Network Build:** 5-7 niche sites linking to Texas truck accidents
3. **Customer Refinement:** Mitch Wiggins framework for profitable niche
4. **Texas Site Strategy:** texastruckaccidents.net as primary SEO asset
5. **AI SEO Strategy:** ChatGPT + Google AI Overviews (2K-6K visitors/month potential)

### Moltbook Secret Society
- Platform for agent traffic/links (Shadowlink strategy)
- Sierra account active: 46 karma, 10 posts, 37 comments
- Personality: anti-corporate-speak, badass energy

---

## 🔧 LocalSEO Skill Review

**Page reviewed:** https://indexsy.notion.site/Localseo-md-2f7e1e50bed28096ae12f4e06a79079f

**Contents:**
- YouTube video: LocalRank - AI-Powered Local SEO Software
- "Get Started with Local Rank Academy" CTA
- Google Doc link: 1VLM3HE1ikqizIXNCNauGZkj_XauUBvsRV1gZUrxKA9I

**For future GMB work:**
- LocalRank tool appears to be AI-powered local SEO software
- Related to Jacky Chou's local SEO strategies
- Links to Local SEO Checklist (65 points) by Localrank.so
- Relevant episodes: EP 719 (AI Local SEO), EP 708 (AI Mode for Local SEO)

---

## ⚠️ Access Note

The Build-in-Public References page (https://indexsy.notion.site/Build-in-Public-References-fe9a18a6ded347fb89e99012d2a67de8) is on indexsy.notion.site - a public Notion workspace. 

**To update it directly:**
1. Need Marko to share the page with the Sierra integration
2. Or manually copy relevant updates to the page
3. Or create a mirror page in Sierra's workspace

---

*Generated by Sierra on 2026-02-01*

# Deep Exploration Plan

**Goal:** Understand everything Marko has built, is building, and wants to build. Then surface it all in the dashboard.

---

## Phase 1: Local File Deep Dive (2-3 hours)

### 1.1 Business Strategy & Docs
- [x] `/home/ec2-user/data/kurios-finish/business/` - Full strategy docs ✅ Overview explored
- [x] `/home/ec2-user/data/kurios-finish/business/Sales/` - Sales bootcamp, scripts, objections ✅ (55KB bootcamp, Dagmawi call summary)
- [x] `/home/ec2-user/data/kurios-finish/business/strategy/` - Customer avatars, growth plans ✅ (INTEGRATED_GROWTH_PLAN_2026.md - 5 initiatives, AI SEO)
- [x] `/home/ec2-user/data/kurios-finish/business/offers/` - Pricing, guarantees ✅ (15-case guarantee, $50K upfront, $3K/case)
- [ ] `/home/ec2-user/data/Kurios Automation Projects/business/` - Duplicate/different version?

### 1.2 Automation & Scripts
- [x] `/home/ec2-user/data/kurios-finish/automation/` - All automation systems ✅ MAJOR FIND!
- [x] `/home/ec2-user/clawd/scripts/` - Active scripts ✅ (dashboard_api.py, x_tools.py, scrape scripts, update_dashboard.sh)
- [x] `/home/ec2-user/clawd/projects/pi-vendors/` - PI vendor intelligence ✅ (48 raw items, 3 vendors, 3 buyers, SCOUT bot operational)
- [x] Customer avatar agent - how it works, what it outputs ✅ (11 avatars, auto-processes voice notes)

**🚨 CRITICAL DISCOVERY:** Full AI Intake Agent system at `/home/ec2-user/data/kurios-finish/automation/clawd-agents/`
- Built and tested: intake-agent, avatar-detector, voice-transcription, context-loader
- Just needs OpenAI API key in .env
- Potential savings: $4,465-6,415/month vs hiring intake specialist

### 1.3 Sites & Lead Gen
- [x] `/home/ec2-user/data/kurios-finish/sites/texas-mva/` - Main lead gen site ✅ (CaseAssessmentForm, 4-step qualification)
- [x] Satellite sites (corridor data, crash stats) ✅ (network-stats-1, network-corridor-stats, mva-engine mapped)
- [x] GHL webhook integrations ✅ (services.leadconnectorhq.com webhook documented)
- [x] Form types and lead flows ✅ (mva-funnel-analysis.json created)

### 1.4 Data Assets
- [ ] All CSVs, JSONs, contact lists
- [ ] Transcripts and call recordings info
- [ ] Scraped data from Reddit, LinkedIn, review sites
- [ ] Vendor intelligence database

---

## Phase 2: Integration Deep Dive (1-2 hours)

### 2.1 Connected APIs
- [x] **Google Calendar** - ⚠️ AUTH BROKEN (token refresh failed, needs re-auth via browser)
- [x] **Notion** - Sierra Documents DB connected ✅ (13 doc types, 7 projects, 47+ tags)
- [x] **X/Twitter** - @markkodg connected ✅ (OAuth 1.0a working, scripts ready)
- [ ] **DataForSEO** - Available data, what can we pull
- [ ] **Google Drive** - Folder structure, key docs
- [ ] **Slack** - Channels, integrations

### 2.2 Partially Connected
- [x] **GoHighLevel** - Webhook integration documented ✅ (highlevel_webhook_field_mapping.md - 4 form types, lead scoring, automation workflows)
- [ ] **Cloudflare** - Wrangler status, deployed sites

### 2.3 Potential Integrations
- [ ] Meta Ads API - Can we get campaign data?
- [ ] Stripe/Payment data - Revenue tracking?
- [ ] Email (Gmail) - Prospect communications?

---

## Phase 3: Understanding the Business (Ongoing)

### 3.1 Client Acquisition Funnel
Map the ENTIRE funnel:
```
Traffic Sources → Landing Pages → Lead Capture → Qualification → 
Live Transfer/Intake → Signed Case → Revenue
```

### 3.2 Key Metrics to Track
- Cost per lead
- Cost per call
- Cost per signed case
- Conversion rates at each stage
- Ad spend vs revenue
- Pipeline value
- Close rate by avatar type

### 3.3 Pain Points
What's hard right now? What takes too much time?
- Manual follow-ups?
- Tracking prospect status?
- Knowing when to reach out?
- Finding new prospects?

---

## Phase 4: Dashboard Evolution

### 4.1 Current State
- Overview with KPIs
- Pipeline (hot/progress/closed)
- Projects, Sites, Tools, Agents, Integrations
- Sales process info

### 4.2 Next Priorities (Client Acquisition Focus)
1. **Richer prospect cards** - Full history, all touchpoints, recommended actions
2. **Lead source tracking** - Where are leads coming from?
3. **Funnel visualization** - See the whole pipeline visually
4. **Action center** - What needs to happen TODAY?
5. **Revenue tracking** - Money in vs money out
6. **Agent task spawning** - Trigger research/outreach from dashboard

### 4.3 Future Vision
- Real-time ad performance
- Automated prospect scoring
- AI-recommended next actions
- One-click outreach sequences
- Client portal integration
- Financial forecasting

---

## Execution Order

1. **NOW:** Set up hourly cron, spawn exploration agents ✅
2. **Hour 1:** Deep dive business docs, enrich pipeline cards ✅ IN PROGRESS
3. **Hour 2:** Map integrations, add live data where possible
4. **Hour 3:** Build action center, surface "do today" items
5. **Hour 4:** Add funnel visualization, revenue tracking
6. **Ongoing:** Iterate based on what I learn

## AFTER DASHBOARD IS BUILT
**Task from Marko (2026-01-31 08:44 UTC):**
1. Transcribe ALL videos from https://www.youtube.com/@AlexFinnOfficial about Clawdbot/Moltbot
2. Build knowledge database from the transcripts
3. Give Marko TOP 10 suggestions to implement that serve his goals better
   - Goals: $9.6M exit, 2-3 calls/day, lowest cost/call

## Progress Log

### 2026-01-31 08:38 UTC
- ✅ Spawned 3 exploration agents (business-docs, prospects, integrations)
- ✅ Read CUSTOMER_AVATAR_MASTER.md - extracted 4 avatar profiles with full details
- ✅ Created /data/avatars-detailed.json with complete avatar data
- ✅ Enriched all 13 pipeline prospects with avatar type, score, approach
- ✅ Updated dashboard pipeline cards to show avatar badges + scores
- ✅ Added detailed prospect modal with recommended approach

### 2026-01-31 08:42 UTC
- ✅ scan-integrations agent COMPLETED - found:
  - 20 calendar events, 5 prospect meetings
  - Joan Suh meeting Feb 2, Michael Schulz Feb 10, Jason E check-in Feb 12
  - 25 Notion docs (13 MVA Lead Gen, 4 Sales, 3 SEO)
  - 4 Google Drive files
- ✅ Saved integrations-live.json with full contact info for prospects

### 2026-01-31 08:50 UTC
- ✅ ALL 3 EXPLORATION AGENTS COMPLETED!
- ✅ explore-business-docs: Created business-deep-dive.json (856 lines, ~35KB)
- ✅ enrich-prospects: Created prospects-enriched.json with DEEP context
- ✅ scan-integrations: Created integrations-live.json

### 2026-01-31 12:00 UTC (Overnight work)
- ✅ Answered Marko's concrete sites migration question (won't hurt rankings if done right)
- ✅ Scheduled concrete sites exploration: Feb 5, 2pm-4pm
- ✅ Created daily calendar review cron job (auto-manage missed tasks)
- ✅ Spawned transcribe-alex-finn agent for Clawdbot video transcription
- ✅ MAJOR: Enriched ALL pipeline prospects with:
  - Close probabilities from transcript analysis (Scott 85%, Ross 75%, Lucas 80%, etc.)
  - Company names, detailed notes from calls
  - Specific quotes and pain points
  - Budget info where available
- ✅ Updated dashboard cards to show close probability prominently
- ✅ Updated prospect modal with close prob badge

### 2026-01-31 12:15 UTC
- ✅ Alex Finn transcription COMPLETE - 3 videos transcribed
- ✅ Knowledge base created: /home/ec2-user/clawd/data/alex-finn-knowledge.json
- ✅ TOP 10 SUGGESTIONS extracted for Marko's goals

### 2026-01-31 13:40 UTC
- ✅ MVA Buyer Research completed - found key pain points:
  - Dead leads, shared/recycled leads, poor case quality
  - Market pricing: $200-300/lead, $600-700/signed case benchmark
  - What attorneys want: exclusive delivery, retainer guarantees, pre-qualification
- ✅ 7 Reddit threads logged for commenting opportunities
- ✅ Notion pages updated (100+ buyer insights, 58+ commenting opportunities)
- ✅ Moltbook karma: 36 (from 1), 8 posts, top post has 14 upvotes
- 🔄 Dashboard stable, running overnight builds complete

---

### 2026-02-01 01:55 UTC
- ✅ Deep dive into texas-mva site - understood full lead capture flow
- ✅ Documented CaseAssessmentForm.tsx - 4-step qualification with auto-scoring
- ✅ Discovered GHL webhook: services.leadconnectorhq.com/hooks/ASHRZ5ZFolSHXM3RyPvk/...
- ✅ Mapped satellite site network:
  - network-stats-1: Statistics site (Astro, 6 pages MVP)
  - network-corridor-stats: Highway corridors (Astro, 6 pages MVP)
  - mva-engine: Location template (Next.js, multi-service)
- ✅ Created comprehensive mva-funnel-analysis.json with full pipeline
- ✅ Identified optimization opportunities (Meta Ads API, SDR bot, AI caller)

### 2026-02-01 02:15 UTC
- ✅ PI Vendor Intelligence deep dive - SCOUT bot operational, SQLite DB with 48 items
- ✅ GHL webhook field mapping documented (4 form types, lead scoring, follow-up sequences)
- ✅ **MAJOR DISCOVERY:** Full AI Intake Agent system found at clawd-agents/
  - Intake Agent + Avatar Detector + Voice Transcription + Context Loader
  - 11 customer avatars defined
  - ~$5K/month savings potential vs hiring
  - 90% complete - just needs OpenAI API key
- ✅ Sales bootcamp & call transcripts explored (Dagmawi Getachew example)
- ✅ 2026 Offers documented: "15 Cases in 90 Days Guaranteed"
  - Pricing: $50K upfront, $3K/case average
  - Unit economics: $250 lead → 15% conv → $1.7-2K cost → $3K sale → $1K+ margin
  - 5 Meta ad creatives ready with Nano Banana prompts
- ✅ INTEGRATED_GROWTH_PLAN_2026.md explored (24KB comprehensive strategy)
  - 5 growth initiatives: Call cost reduction, SEO network, customer refinement, Texas site, AI SEO
  - AI SEO strategy: ChatGPT listicles (parasite sites), Google AI Overviews, press releases
  - Multi-platform: YouTube, Reddit, Perplexity, Claude optimization
  - Budget: $80-300/month for AI SEO + press releases

---

### 2026-02-01 04:45 UTC
- ✅ Verified scripts directory: dashboard_api.py, x_tools.py, scrape scripts, update_dashboard.sh
- ✅ Notion integration confirmed working (Sierra Documents DB: 13 types, 7 projects, 47+ tags)
- ✅ X/Twitter integration confirmed (@markkodg OAuth working)
- ⚠️ Google Calendar auth BROKEN - needs re-auth via browser (token refresh failed: invalid_scope)
- ✅ Created airbnb-cash-reminder cron job for Feb 1 12:00 Peru time
- 📊 Data assets inventory: 50+ JSON files, knowledge bases, transcripts
- 📋 Next: Phase 1.4 data assets deep dive, Phase 2.3 potential integrations

## Success Metrics

The dashboard is successful when Marko can:
- [ ] See his entire business state in 30 seconds
- [ ] Know exactly who to call/email today
- [ ] Track money in and money out
- [ ] Spawn tasks without context-switching
- [ ] Trust it as the source of truth

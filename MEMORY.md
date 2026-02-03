# MEMORY.md - Long-Term Memory

## Key Info

### Accounts & Access
- **sierra@kuriosbrand.com** — My Google Workspace account
- **Google OAuth** — Proper API access set up (no passwords stored)
  - ✅ Calendar API
  - ✅ Gmail API
  - ✅ Drive API
- Token location: `~/.config/gcal-pro/token.json`
- Can access mark@kuriosbrand.com calendar (shared)
- **Slack** — ✅ Configured (Socket Mode, DM pairing enabled)
- **Telegram** — configured and working

### Business
- **KuriosBrand LLC** — Marko's business
- **MVA Lead Gen** — Current focus: generating motor vehicle accident leads for lawyers
- Partners: Max & Jeremy @ Cases on Demand, Patrick @ Inquired Esquire (intake support)
- **Domains:**
  - kuriosbrand.com — main
  - lead.kuriosbrand.com — landing page for different offer

### Google Drive Shared Files
- **Kurios MVA Appointments** — Main CRM/pipeline tracker
  - ID: `1iu8lHRKAt_eDoHr6SreDktQhwT8l0R-VFpfvObKHtMQ`
  - Tracks: contacts, appointment dates, call outcomes, Patrick handoffs, deal status
- **November 2025 Accounting** — `1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0` (empty)
- **December 2025 Accounting** — `1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo` (empty)
- **MVA Carlos & Mark Partnership** folder — `1qshu4wTkayK-3C_h8nPEy_YWtWoaPAUX`
- **MVA Sales Process - COD** doc — `1pJ3l9grF0ed_y-eJ5Mt5-CnLfRbtt8Qas880_s3Wts0` (needs Docs API enabled)

### Terminology
- **OTP** = One Time Password (SMS verified leads) — NOT "On The Phone"
- **Form Fill Leads** = Raw leads from form submissions (basic tier)
- **Live Transfers** = Qualified prospects transferred to attorney's phone
- **Signed Cases** = Retainers delivered, ready to litigate

### MVA Sales Model (from pipeline data)
- **Lead pricing:** ~$250-350/lead depending on state
- **Conversion rates:** ~8-15% lead-to-signed (varies by state — contract states lower)
- **Case cost target:** ~$2,000-$2,100 per signed case
- **Minimum buy:** $15k media spend (some deals at $50k)
- **Patrick's intake options:** $100/qualified transfer OR $350/signed case
- **Key selling points:** branded ads, predictable volume, vetted leads, compliance

### Current Pipeline (as of 2026-01-29)
**Hot prospects (need Patrick call):**
- Rich Hyde (Trial Tribe) — wants reliable vendor replacement
- Dagmawi Getachew (DG Firm) — wants vetted leads, small test first
- Lucas Naccarati (Muniz Kim Law) — scalable paid acquisition
- Jalal Abdallah — $50k multi-state buy, verbally committed, call 01/21
- Omeed Hakimianpour (Injury Partners) — $50k CA campaign, call 01/21
- Scott Barney — VA Beach, burned $250k on bad marketing, HIGH PRIORITY
- Ross Robin — brand new PI firm from scratch, HIGH PRIORITY
- Michael Schulz (RMD Law) — follow-up 02/10

**Closed/Lost:**
- Jonathan Mahler — wanted full fee transparency, not a fit
- Jason E (GCE Law) — CLOSED
- Michael Goodrich — canceled

**In progress (need follow-up):**
- Josh Sweeney (Shane Smith Law) — interested in YouTube/TikTok
- Michael Shirts (BS Injury Law) — Las Vegas, needs firm branding
- Daniel Ramirez — Dallas→Houston expansion, Spanish leads, follow up in 1 week
- Joan Suh — call scheduled 01/29

### Projects in Progress
- **Kurios Automation Projects** — TWO SOURCES:
  - Partial upload (665M): `/home/ec2-user/data/Kurios Automation Projects/`
  - GitHub finish (9.6M, 304 files): `/home/ec2-user/data/kurios-finish/`
  - Contains: automation, business, data, docs, sites, states, root scripts
  - **RULES:**
    - DO NOT DELETE ANY FILES without explicit approval
    - Filter mentally — ignore node_modules/.git/build artifacts when learning
    - Focus on: .md files, transcripts, configs, actual source code
    - Over time: suggest consolidations/cuts, but ASK FIRST
    - Goal: Learn the important content, preserve all data
- **Texas MVA Site** — GitHub repo: https://github.com/markoinc/texas-mva-site

### Completed Tasks (2026-01-29)
- ✅ EC2 security (SSH IP restriction, auto-updates) — done by Marko
- ✅ Google Workspace 2FA on admin account — done by Marko

### Preferences
- Marko prefers voice messages over typing
- Wants bedtime reminders 9 hours before morning calendar events
- Direct communication style
- **Tasks → Calendar:** When Marko says "update my tasks" with action items, ADD THEM TO CALENDAR (not just memory)
- **NEVER move/reschedule booked appointments** (especially sales calls with law firms) unless explicitly asked
- **Sales calls = #1 priority** — never deprioritize for tasks
- **Simulate 1000 scenarios** — Before deploying anything, stress test with 1000 simulated users/conversations/scenarios. Report what breaks.
- **Simulation budget:** $200/day TOTAL for large-scale simulations (100K scenarios)

### Tools & Resources
- **crowdreply.io** — Reddit comments and upvotes
- **Jacky Chou SOPs** — Saved to `/home/ec2-user/clawd/data/jacky-chou-sops.md`
  - Reddit: EP 742 (10k comments), EP 650 (full course), EP 635 ($10k SOP)
  - Appointments: EP 653 (7-day sequence)
  - ClawdBot: EP 747 (phone farm/account farming)
  - Facebook Groups: EP 721

---

*Created: 2026-01-29*
*Last updated: 2026-01-29*

## 2026-02-01 Late Night Updates

### Site Migration
- **kuriosbrand.com** moved from Lovable → GitHub + Cloudflare Pages
- Repo: `markoinc/kuriosbrand`
- Cloudflare project: `kuriosbrandoriginal`
- Supabase env vars required for build

### Pricing Sheet
- **Kurios Performance Stats & Pricing** (current - recreated 2026-02-02)
- Sheet ID: `1Ka5HMSXoxsffYX3W-jlNURMkFiNuA7FcptM4tkx6h7c`
- Link: https://docs.google.com/spreadsheets/d/1Ka5HMSXoxsffYX3W-jlNURMkFiNuA7FcptM4tkx6h7c/edit
- OLD Sheet (deleted): `1aFiWHBiugUKLK-fkRru8HcbTVfP6NQHkXjvPhVnXasU`

### Knowledge Base Additions
- Kit's Clawdbot multi-persona setup (Greg Isenberg podcast)
- Jacky Chou's $254K/mo SOP - competitor ad scraping, Reddit warm-up

## Core Operating Principle (2026-02-02)
**BUILD SYSTEMS, NOT ONE-OFFS**

Marko's instruction: "Anytime I ask you to do something, instead of doing it yourself, build something that does it and save it to memory so you can use it in the future."

- Every task → becomes a reusable tool/script
- Save to ~/clawd/scripts/ + document in TOOLS.md
- Goal: Every repeated task becomes a one-liner

---

## 2026-02-03 Learnings & SOPs

### Email Preferences (IMPORTANT)
**Signature format — SIMPLE:**
```
Mark Gundrum
kuriosbrand.com
```
- ❌ NO business name (KuriosBrand LLC)
- ❌ NO phone number
- ❌ NO address

### MVA Sales Email Language
- **Timeline:** Signed cases delivered in **30-40 days** (NOT 60-90)
- **Terminology:** We deliver "signed cases" — not leads, not warm transfers
- **Differentiation:** "Real signed cases cost more, but they're already converted. That's what we deliver."
- **Closing:** "Looking forward to getting started." (confident, not passive)
- **Patrick mentions:** Don't include unless specifically instructed

### SOPs Created
All saved to `/home/ec2-user/clawd/memory/sops/`:
- `email-signature.md` — Standard signature format
- `prospect-follow-up-emails.md` — Full email drafting process
- `voice-message-workflow.md` — Transcription and response process
- `contact-enrichment.md` — Enriching contacts for agreements

### Email Addresses
- Joan Suh: joan0407@gmail.com
- Sierra: sierra@kuriosbrand.com
- Carlos: carlos@kuriosbrand.com

### Joan Suh Deal (sent 2026-02-03)
- Georgia PI lawyer, first-time ad buyer
- Option 1: $30k for 10 guaranteed signed cases (30-40 days)
- Option 2: $15k for ~5 signed cases (no guarantee)
- Follow-up call: **Feb 9, 2026 @ 4:00 PM EST**

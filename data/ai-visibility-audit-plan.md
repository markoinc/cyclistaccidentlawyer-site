# AI Visibility Audit Tool — Build Plan

**Purpose:** Free lead magnet that scores law firm websites on AI readiness
**Goal:** Capture emails, qualify leads, demonstrate expertise before the sales call

---

## WHAT IT DOES

User enters:
1. Website URL
2. City/Location
3. Practice area (PI, Criminal, etc.)
4. Email

Tool returns:
- **AI Visibility Score (0-100)**
- **Breakdown by category**
- **Competitor comparison** (3 local competitors)
- **Top 5 actionable fixes**
- **PDF report** (for email capture)

---

## SCORING CATEGORIES (100 points total)

### 1. Structured Data & Schema (25 points)
- [ ] LocalBusiness schema present (5 pts)
- [ ] Attorney/LegalService schema (5 pts)
- [ ] Review schema / aggregateRating (5 pts)
- [ ] FAQ schema on pages (5 pts)
- [ ] Breadcrumb schema (3 pts)
- [ ] Organization schema (2 pts)

**How to check:** Scrape page, parse for JSON-LD / microdata

### 2. Content Quality for AI (25 points)
- [ ] Clear practice area pages (5 pts)
- [ ] FAQ sections with Q&A format (5 pts)
- [ ] Location-specific content (5 pts)
- [ ] "About the attorney" with credentials (5 pts)
- [ ] Case results / settlements listed (5 pts)

**How to check:** Scrape page content, look for patterns/keywords

### 3. Technical SEO (20 points)
- [ ] Mobile-friendly (5 pts)
- [ ] Page speed <3s (5 pts)
- [ ] HTTPS (3 pts)
- [ ] No broken links (3 pts)
- [ ] Sitemap present (2 pts)
- [ ] Robots.txt configured (2 pts)

**How to check:** Lighthouse API, PageSpeed Insights API, simple HTTP checks

### 4. Local SEO Signals (15 points)
- [ ] Google Business Profile linked (5 pts)
- [ ] NAP consistency (name, address, phone) (5 pts)
- [ ] Service area pages (3 pts)
- [ ] Local citations referenced (2 pts)

**How to check:** Scrape for address patterns, check GBP API

### 5. AI Discoverability (15 points)
- [ ] Site appears in ChatGPT results for "[city] [practice] lawyer" (5 pts)
- [ ] Site appears in Perplexity results (5 pts)
- [ ] Site appears in Google AI Overview (5 pts)

**How to check:** API calls to AI tools (tricky, may need manual verification or proxy)

---

## COMPETITOR COMPARISON

For the given city + practice area:
1. Search Google for "[city] [practice] lawyer"
2. Pull top 3 organic results
3. Run same audit on each
4. Show side-by-side comparison

**Output example:**
| Metric | Your Site | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|-----------|--------------|--------------|--------------|
| AI Score | 34/100 | 67/100 | 52/100 | 45/100 |
| Schema | ❌ | ✅ | ✅ | ❌ |
| Speed | 4.2s | 1.8s | 2.4s | 3.1s |
| Mobile | ✅ | ✅ | ✅ | ✅ |

---

## TECHNICAL ARCHITECTURE

### Option A: Simple Script (MVP)
```
Input → Python script → PDF report → Email via SendGrid
```
- Fast to build (1-2 days)
- Manual trigger or webhook
- No fancy UI

### Option B: Web App (Better)
```
Landing Page → Form → API → Processing → Results Page + PDF
```
- Next.js or simple HTML/JS frontend
- Python/Node backend for analysis
- Better UX, can show results live

### Option C: Full Product (Best, but more work)
```
Branded tool on subdomain (audit.kuriosbrand.com)
→ Form
→ Real-time scoring with animations
→ Results dashboard
→ PDF download
→ Auto-email sequence
```

**Recommendation:** Start with Option B, upgrade to C if it converts.

---

## BUILD PHASES

### Phase 1: Core Analyzer (Day 1-2)
- [ ] Build Python script that takes URL input
- [ ] Implement schema detection (JSON-LD parser)
- [ ] Implement basic content analysis
- [ ] Implement technical checks (speed, mobile, SSL)
- [ ] Generate score calculation
- [ ] Output JSON results

**Tools needed:**
- `requests` + `BeautifulSoup` for scraping
- `extruct` for schema extraction
- Google PageSpeed Insights API (free)
- `jinja2` for report templating

### Phase 2: Competitor Analysis (Day 2-3)
- [ ] Add Google Search scraping (or DataForSEO API)
- [ ] Pull top 3 competitors for given city+practice
- [ ] Run analyzer on each competitor
- [ ] Generate comparison table

### Phase 3: Report Generation (Day 3)
- [ ] Design PDF report template
- [ ] Include score breakdown
- [ ] Include competitor comparison
- [ ] Include top 5 recommendations
- [ ] Add branding (Kurios logo, CTA)

**Tools:**
- `weasyprint` or `reportlab` for PDF generation
- Or use a service like DocRaptor

### Phase 4: Web Interface (Day 4-5)
- [ ] Build simple landing page (form)
- [ ] Connect to backend API
- [ ] Show loading state with progress
- [ ] Display results on page
- [ ] Trigger PDF generation + email

### Phase 5: Email Automation (Day 5)
- [ ] Set up SendGrid/Postmark
- [ ] Send PDF report via email
- [ ] Add to email nurture sequence
- [ ] Track opens/clicks

---

## API KEYS NEEDED

| Service | Purpose | Have It? |
|---------|---------|----------|
| Google PageSpeed Insights | Speed/mobile checks | Free, no key needed |
| DataForSEO | SERP data for competitors | ✅ Yes |
| OpenAI | Optional: AI analysis of content | ✅ Yes |
| SendGrid/Postmark | Email delivery | Need to set up |

---

## SAMPLE OUTPUT

```
===============================================
AI VISIBILITY AUDIT REPORT
===============================================
Website: smithinjurylaw.com
Location: Houston, TX
Practice: Personal Injury

OVERALL SCORE: 34/100 (Poor)
You're losing cases to competitors.

-----------------------------------------------
BREAKDOWN:
-----------------------------------------------
Structured Data:     8/25  ⚠️ Missing critical schema
Content Quality:    12/25  ⚠️ No FAQ sections
Technical SEO:      14/20  ✅ Mostly good
Local SEO:           0/15  ❌ No local optimization
AI Discoverability:  0/15  ❌ Invisible to AI

-----------------------------------------------
VS. YOUR COMPETITORS:
-----------------------------------------------
                    You    Morgan&Morgan   LocalFirm1   LocalFirm2
AI Score           34/100     78/100         61/100       52/100
Ranking            #4         #1             #2           #3

-----------------------------------------------
TOP 5 FIXES (in order of impact):
-----------------------------------------------
1. Add LocalBusiness + Attorney schema markup
2. Create FAQ sections on every practice page
3. Build location-specific landing pages
4. Add case results with $ amounts
5. Improve page speed (currently 4.2s, target <2s)

-----------------------------------------------
NEXT STEP:
-----------------------------------------------
Book a free 15-minute call to discuss your results:
[CALENDAR LINK]

Or reply to this email with questions.
===============================================
```

---

## MONETIZATION FLOW

```
Free Audit → Email Capture → Results → CTA for Call → Sales Call → $12,500 Website
```

**Expected conversion:**
- 100 audits/week
- 20% book a call (20 calls)
- 25% close rate (5 clients)
- 5 × $12,500 = $62,500/month potential

---

## TIMELINE

| Day | Task |
|-----|------|
| 1 | Core analyzer script (schema, content, technical) |
| 2 | Competitor analysis + scoring logic |
| 3 | PDF report generation |
| 4 | Web interface (form + results page) |
| 5 | Email integration + testing |
| 6 | QA + launch |

**Total: 6 days to MVP**

---

## QUESTIONS FOR MARKO

1. **Domain:** audit.kuriosbrand.com or kuriosbrand.com/audit?
2. **Branding:** Kurios or create a separate brand for the audit tool?
3. **Email sequence:** How many follow-up emails after the audit?
4. **Manual review:** Should every audit get a human review before sending, or fully automated?
5. **Competitor limit:** Show top 3 competitors, or let user choose which competitors to compare?

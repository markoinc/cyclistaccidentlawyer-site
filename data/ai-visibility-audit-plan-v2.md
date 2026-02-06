# AI Visibility Audit Tool — Build Plan v2

**Updated:** 2026-02-05
**Based on:** Princeton/Stanford GEO research, Frase.io, Conductor 2026 AEO/GEO Benchmarks
**Purpose:** Score law firm websites on AI citation likelihood

---

## RESEARCH-BACKED SCORING FACTORS

### Key Research Findings:
1. **40% visibility boost** from 3 tactics: citing authoritative sources, expert quotes, statistical data
2. **87% of ChatGPT citations** match Bing's top organic results — SEO still matters
3. **76.1% of AI Overview citations** also rank in Google's top 10
4. **ChatGPT cites Wikipedia 47.9%** of the time — authoritative sources win
5. **Perplexity cites Reddit 46.7%** — fresh, community-vetted content
6. **AI prefers 2,800+ word** comprehensive content with topical completeness

---

## SCORING CATEGORIES (100 points total)

### 1. Structured Data & Schema (20 points)
*AI engines use schema to understand page context*

| Factor | Points | How to Check |
|--------|--------|--------------|
| LocalBusiness schema | 4 | JSON-LD parser |
| Attorney/LegalService schema | 4 | JSON-LD parser |
| FAQ schema on pages | 4 | JSON-LD parser |
| Review/AggregateRating schema | 3 | JSON-LD parser |
| Breadcrumb schema | 3 | JSON-LD parser |
| Organization schema | 2 | JSON-LD parser |

### 2. Content Quality for AI Citation (30 points)
*Princeton study: These factors increase citation rate by 40%*

| Factor | Points | How to Check |
|--------|--------|--------------|
| **Authoritative outbound links** (.edu, .gov, research) | 8 | Count external links to credible domains |
| **Expert quotations** with attribution | 6 | Pattern match for quote marks + attribution |
| **Statistics/data points** with citations | 6 | Regex for numbers + source references |
| **FAQ sections** (Q&A format) | 4 | Look for question-answer patterns |
| **Comprehensive length** (2,000+ words on key pages) | 3 | Word count |
| **Third-person authoritative tone** | 3 | NLP analysis (avoid "we", "I") |

### 3. Technical SEO (15 points)
*87% of AI citations come from top-ranking pages*

| Factor | Points | How to Check |
|--------|--------|--------------|
| Mobile-friendly | 4 | PageSpeed Insights API |
| Page speed <3s | 4 | PageSpeed Insights API |
| HTTPS | 3 | Simple HTTP check |
| No critical errors | 2 | Lighthouse audit |
| Clean URL structure | 2 | URL pattern analysis |

### 4. E-E-A-T Signals (20 points)
*Experience, Expertise, Authoritativeness, Trustworthiness*

| Factor | Points | How to Check |
|--------|--------|--------------|
| **Attorney bio pages** with credentials | 5 | Check for /attorney/ or /about/ pages with JD, Bar # |
| **Case results/verdicts** with $ amounts | 5 | Pattern match for settlements, verdicts |
| **Practice area depth** (dedicated pages per specialty) | 4 | Count practice area pages |
| **Publication dates** on content | 3 | Check for datePublished metadata |
| **Author attribution** on articles | 3 | Check bylines |

### 5. AI Discoverability / Freshness (15 points)
*Perplexity favors content <90 days old*

| Factor | Points | How to Check |
|--------|--------|--------------|
| Content updated in last 90 days | 5 | Check dateModified or Last-Modified header |
| Blog/news section with regular updates | 4 | Check for /blog/ with recent posts |
| Location-specific pages | 3 | Check for city/county landing pages |
| Answer-ready content structure | 3 | Direct answers in first 100 words |

---

## BONUS: ACTUAL AI CITATION CHECK (+10 bonus points)

Run test queries against AI platforms:

| Query Template | Check |
|----------------|-------|
| "best [practice area] lawyer in [city]" | Does site appear in ChatGPT response? |
| "[city] [practice area] attorney reviews" | Does site appear in Perplexity? |
| "[practice area] lawyer near me" | Does site appear in Google AI Overview? |

**Note:** This is harder to automate but high-value. Could do manual spot-check or use API if available.

---

## COMPETITOR COMPARISON METHOD

1. Search Google: "[city] [practice area] lawyer"
2. Pull top 3 organic results (DataForSEO API)
3. Run same audit on each competitor
4. Calculate percentile ranking

**Output:**
```
Your Score: 47/100
Competitor 1 (Morgan & Morgan): 78/100
Competitor 2 (Local Firm A): 61/100
Competitor 3 (Local Firm B): 52/100

You're in the BOTTOM 25% of local competitors.
```

---

## WEIGHTING RATIONALE

| Category | Weight | Why |
|----------|--------|-----|
| Content Quality | 30% | Princeton study: biggest impact on citation rate |
| E-E-A-T | 20% | Google's core ranking factor, feeds into AI citations |
| Structured Data | 20% | AI engines parse schema for understanding |
| Technical | 15% | Foundation — can't cite broken sites |
| Freshness | 15% | Perplexity heavily favors recent content |

---

## ACTIONABLE RECOMMENDATIONS ENGINE

Based on score gaps, auto-generate top 5 fixes:

**If Schema score < 50%:**
→ "Add LocalBusiness + Attorney schema markup — this helps AI understand your business"

**If no expert quotes found:**
→ "Add direct quotes from attorneys on case result pages — AI engines cite quoted experts 40% more"

**If no statistics with citations:**
→ "Add specific settlement amounts and cite case outcomes — data-backed content gets prioritized"

**If content < 2000 words:**
→ "Expand key practice area pages to 2,000+ words — AI prefers comprehensive coverage"

**If no dateModified:**
→ "Add lastmod timestamps to pages — AI engines favor recently updated content"

**If no FAQ sections:**
→ "Add FAQ schema to practice area pages — direct Q&A format matches how users query AI"

---

## SAMPLE REPORT OUTPUT

```
═══════════════════════════════════════════════════════
        AI VISIBILITY AUDIT REPORT
═══════════════════════════════════════════════════════

Website: smithinjurylaw.com
Location: Houston, TX
Practice: Personal Injury

═══════════════════════════════════════════════════════
        OVERALL SCORE: 34/100 (POOR)
═══════════════════════════════════════════════════════

When someone asks ChatGPT "best personal injury lawyer in 
Houston," you're NOT being cited. Your competitors are.

───────────────────────────────────────────────────────
BREAKDOWN BY CATEGORY:
───────────────────────────────────────────────────────

Content Quality for AI:    9/30   ⚠️ CRITICAL
  ❌ No authoritative outbound links
  ❌ No expert quotations found
  ❌ No statistics with citations
  ✅ FAQ sections present (partial)

E-E-A-T Signals:          12/20   ⚠️ NEEDS WORK
  ✅ Attorney bio with credentials
  ❌ No case results with $ amounts
  ⚠️ Only 2 practice area pages
  ❌ No publication dates

Structured Data:           4/20   ❌ POOR
  ❌ No LocalBusiness schema
  ❌ No Attorney schema
  ❌ No FAQ schema
  ❌ No Review schema

Technical SEO:            9/15   ✅ OK
  ✅ Mobile-friendly
  ⚠️ Page speed 3.2s (target: <2s)
  ✅ HTTPS enabled

Freshness:                0/15   ❌ STALE
  ❌ No content updates in 180+ days
  ❌ No blog or news section
  ❌ No dateModified metadata

───────────────────────────────────────────────────────
VS. LOCAL COMPETITORS (Houston PI Lawyers):
───────────────────────────────────────────────────────

                        YOURS   #1      #2      #3
AI Visibility Score     34      78      61      52
Schema Markup          ❌      ✅      ✅      ⚠️
Expert Quotes          ❌      ✅      ✅      ❌
Case Results           ❌      ✅      ✅      ✅
Fresh Content          ❌      ✅      ⚠️      ❌

🏆 #1 Competitor: morgananmorgan.com (78/100)
   They're dominating AI citations in your market.

───────────────────────────────────────────────────────
TOP 5 FIXES (In Order of Impact):
───────────────────────────────────────────────────────

1️⃣ ADD SCHEMA MARKUP (+16 potential points)
   Add LocalBusiness + Attorney + FAQ schema to all pages.
   AI engines use schema to understand your business.

2️⃣ ADD CASE RESULTS WITH $ AMOUNTS (+5 points)
   "We recovered $2.3M for a truck accident victim"
   Statistics with context get cited 40% more often.

3️⃣ ADD EXPERT QUOTES (+6 points)
   Include direct quotes from your attorneys on outcomes.
   "According to Attorney Smith, 'Most victims don't 
    realize they have 2 years to file...'"

4️⃣ UPDATE CONTENT REGULARLY (+5 points)
   Add a blog or update practice pages monthly.
   AI engines deprioritize stale content.

5️⃣ LINK TO AUTHORITATIVE SOURCES (+8 points)
   Cite TX statutes, CDC data, NHTSA reports.
   Outbound links to .gov/.edu boost credibility.

───────────────────────────────────────────────────────
WHAT THIS MEANS:
───────────────────────────────────────────────────────

Every time someone in Houston asks AI:
  "Who's the best car accident lawyer?"
  "Should I hire a PI attorney?"
  "How much is my accident case worth?"

...your competitors are getting cited. You're not.

One signed PI case = $16,500+ in fees.
How many cases are you losing to AI-invisible status?

───────────────────────────────────────────────────────
NEXT STEP:
───────────────────────────────────────────────────────

📞 Book a free 15-minute call to discuss your results:
   [CALENDAR LINK]

We build AI-optimized websites specifically for PI lawyers.
$12,500 one-time. Live in 14 days. You own everything.

═══════════════════════════════════════════════════════
```

---

## BUILD PHASES (REVISED)

### Phase 1: Core Analyzer (Day 1-2)
- [ ] Schema detection (JSON-LD parser with `extruct`)
- [ ] Content quality analysis:
  - Outbound link credibility checker
  - Quote detection (regex for quotes + attribution)
  - Statistics/citation detection
  - Word count per page
- [ ] E-E-A-T signal detection:
  - Attorney bio page check
  - Case results pattern matching
  - Publication date extraction

### Phase 2: Technical + Freshness (Day 2)
- [ ] PageSpeed Insights API integration
- [ ] Mobile-friendly check
- [ ] HTTPS verification
- [ ] Last-Modified / dateModified extraction
- [ ] Content freshness scoring

### Phase 3: Competitor Analysis (Day 3)
- [ ] DataForSEO integration for SERP data
- [ ] Parallel audit of top 3 competitors
- [ ] Percentile ranking calculation

### Phase 4: Report Generation (Day 3-4)
- [ ] Design branded PDF template
- [ ] Recommendation engine logic
- [ ] Competitor comparison visuals

### Phase 5: Web Interface (Day 4-5)
- [ ] Landing page with form
- [ ] Loading/progress animation
- [ ] Results page display
- [ ] PDF download trigger

### Phase 6: Email + CRM (Day 5-6)
- [ ] SendGrid integration
- [ ] Auto-send PDF report
- [ ] Add to GHL pipeline
- [ ] Follow-up sequence trigger

---

## QUESTIONS FOR MARKO

1. **Tool name:** "AI Visibility Audit" or something catchier like "AI Citation Score" or "GEO Grader"?
2. **Lead follow-up:** Manual outreach after audit, or automated sequence first?
3. **Competitor data:** Show full competitor URLs or anonymize as "Competitor 1, 2, 3"?
4. **Pricing mention:** Include the $12,500 offer in the report, or just CTA for call?

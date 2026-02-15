# Meta Ads Master Reference Guide 2026

> **Compiled:** February 2026  
> **Sources:** Expert transcripts, X/Twitter insights, course materials (Evan Se), industry guides, competitor research, MVA campaign learnings  
> **Purpose:** Single source of truth for all Meta advertising knowledge

---

## Table of Contents

1. [2026 Algorithm Changes (Andromeda & Beyond)](#1-2026-algorithm-changes-andromeda--beyond)
2. [Campaign Structure Best Practices](#2-campaign-structure-best-practices)
3. [Creative Testing Methodology](#3-creative-testing-methodology)
4. [Bidding Strategies](#4-bidding-strategies)
5. [Audience Targeting Approaches](#5-audience-targeting-approaches)
6. [Placement Optimization](#6-placement-optimization)
7. [Key Metrics & Benchmarks](#7-key-metrics--benchmarks)
8. [Ad Copy & Creative Frameworks](#8-ad-copy--creative-frameworks)
9. [MVA-Specific Learnings](#9-mva-specific-learnings)
10. [Common Mistakes to Avoid](#10-common-mistakes-to-avoid)
11. [Tools & Resources](#11-tools--resources)
12. [Quick Reference Cheat Sheets](#12-quick-reference-cheat-sheets)

---

## 1. 2026 Algorithm Changes (Andromeda & Beyond)

### The Fundamental Shift

Meta officially announced that **by end of 2026, every ad across Meta's platforms will be fully generated and optimized by AI**. Tools like GEM, Lattice, and Andromeda now track signals across Feed, Reels, Stories, and your website in real time.

#### What Changed:
- **Old methods don't work anymore:** Interest stacking, running 15+ ad sets, micro-targeting
- **What works now:** Clean setup, high-quality creative inputs, fewer campaigns
- **Meta rewards brands** that give the algorithm clear signals
- **Creative quality matters more** than complex audience setups

### Andromeda Algorithm: Key Behaviors

#### Creative Similarity Detection
> "Meta now treats two ads as 'identical' if they share similar first 3 seconds... even if the rest is different."
> — @oliverwhudson

**Critical Insight:** The first 3 seconds must be UNIQUE. Same opening = same ad in Meta's eyes. Andromeda groups similar creatives together, causing internal competition.

#### Entity IDs & Creative Diversity
- When creatives are too similar, they "fight each other" in auctions
- You need different "entity IDs" — truly diverse ads, not minor variations
- **Diversity beats volume:** Different angles, formats, hooks > more of the same

#### Post-Andromeda Creative Strategy
**Before Andromeda:**
- Take an angle, create 3-5 ads, test in single ad set

**After Andromeda:**
- Give Meta 3 ad sets with 10-15 ads each
- All different formats, angles, messaging
- Fewer ad sets, more ads per set
- Maximize diversity within each ad set

### Meta's Internal Testing Results
| Improvement | Metric |
|-------------|--------|
| +22% | Higher ROAS with Advantage+ creative |
| +8% | Improvement in ad quality |
| +7% | Increase in conversions using AI-generated images |

### The New Targeting Paradigm
> "Facebook's new Andromeda algorithm for ads will flip everything. Old way: Pick interests → Hope it works. New way: Create diverse content → Let AI find your people."
> — @usamaejaz

**Key Shift:** Stop micromanaging audiences. Feed Andromeda diverse creative and let it find your buyers.

---

## 2. Campaign Structure Best Practices

### The 2-Campaign Structure (Recommended for 2026)

**This is the dominant winning structure:**

1. **Testing Campaign (10-20% of budget)**
   - Test new creatives
   - Multiple ad sets with diverse ads
   - CBO or ABO depending on control needs
   
2. **Scaling Campaign (80-90% of budget)**
   - Holds proven winners only
   - Broad targeting
   - Minimal audience layering
   - Let algorithm optimize

**Process Flow:**
1. Test hooks, formats, messaging in testing campaign
2. Focus on UGC ads for faster feedback
3. When creative hits metric targets, move to scaling
4. Keep scaling campaign broad with minimal audience layering

### Campaign Structure by Budget Level

| Daily Budget | Structure | Reasoning |
|--------------|-----------|-----------|
| <$1K/day | 1 CBO, 1-2 ad sets max | Not enough data for complexity |
| $1K-$5K/day | 2-campaign (Test + Scale) | Standard approach |
| $5K+/day | 2-campaign + possible Advantage+ | Can support more testing |

### The 3-2-2 Testing Structure
> "For testing, I recommend the 3-2-2 structure: 3 ad sets, 2 creatives per ad set, 2 different hooks or angles."

**Implementation:**
- Campaign 1: Testing (CBO, $50-100/day)
  - Ad Set 1: Broad targeting
  - Ad Set 2: Lookalike 1-3%
  - Ad Set 3: Interest stack
- Campaign 2: Scaling (CBO, scaled budget)
  - Winners only

### Evan Se's Structure (High-Volume Testing)

**For CBO (Lower Spend):**
- Campaign Budget Optimization
- 3 ad sets: Interest / Broad / Lookalike
- 7-15 ads per ad set
- **Toggle OFF dynamic creative**

**For ABO (Higher Spend/Control):**
- Ad Set Budget Optimization
- More control over which ads get spend
- Test 1 ad per ad set to isolate variables
- Scale winners into CBO using Post IDs

### Advantage+ Shopping Campaigns (ASC)

**Setup Guidelines:**
- Upload 10-20+ creative variations
- Use existing customer list for exclusions
- Set new customer budget cap at 70-80%
- Let it run 7+ days before judging

**New Features (2026):**
- ASC now supports Cost Caps and ROAS goals
- Can test Value-Based Optimization
- Automates audience selection, placements, creative optimization

---

## 3. Creative Testing Methodology

### The Creative Testing Process

#### Phase 1: Concept Testing
> "Test the message before the creative. What hook resonates? What offer works? What angle converts?"

- Test 5-10 different hooks/angles
- Use simple static images
- Budget: $10-20 per concept
- Winner criteria: CTR > 1%, positive engagement

#### Phase 2: Format Testing
Take winning concepts and create in multiple formats:
- Static images (1:1, 4:5, 9:16)
- Video (15s, 30s, 60s)
- Carousel
- Collection ads

#### Phase 3: Iteration
> "Once you find a winner, iterate on it 10 different ways. Change the hook, the CTA, the colors, the format."

### Weekly Testing Rhythm

| Day | Action |
|-----|--------|
| **Monday** | Launch 5-10 new creatives in testing campaign |
| **Midweek** | Review early signals (don't edit too soon) |
| **End of Week** | Move winners to scaling campaign |
| **Brief Next Round** | Use insights for next batch |

**What to Include Each Week:**
- Mix of fresh angles, creator styles, hooks, formats
- Include one variation of past top performer
- Track what made winners work (hook? tone? problem solved?)

### Batch Testing Strategy (2026)
> "How to test 100 ads and find winners fast:
> 1. Launch an ABO and split 100 ads into 4 ad sets of 25 ads each
> 2. Meta will choose 1-2 ads per ad set to spend on
> 3. Give it 3 days minimum to prove those ads out
> 4. If they don't work, kill them and test more"
> — @benradack

### Statistical Significance Requirements

- **Minimum test duration:** 7-14 days
- **Minimum conversions per variant:** 100
- Wait for at least 50 conversions OR 7 days before making decisions
- Use statistical significance calculators for reliable reads

### Budget Allocation for Testing

| Monthly Budget | Testing Allocation | Focus |
|---------------|-------------------|-------|
| $1K-$5K | 30% | 2-3 distinct approaches, major differences |
| $5K-$25K | 25% | Combine A/B + DCO, parallel segment testing |
| $25K+ | 20% | Comprehensive pipelines, weekly new variants |

### Creative Diversification Strategy

**Creative Mix:**
- 40% UGC (User Generated Content)
- 30% Testimonials/Social Proof
- 20% Product/Offer Focused
- 10% Brand/Lifestyle

> "Your content isn't diverse enough and it's hampering your ability to reach the scale you desire. Too many brands are stuck iterating on the same concepts over and over."
> — @herrmanndigital

---

## 4. Bidding Strategies

### Bid Strategy Options

| Strategy | When to Use | Notes |
|----------|-------------|-------|
| **Highest Volume** | Default starting point | Meta predicts spend + purchase count |
| **Cost Cap** | Control CPA | Set max acceptable CPA |
| **ROAS Goal** | E-commerce scaling | Factors in order value |
| **Bid Cap** | Advanced control | More aggressive than Cost Cap |

### Bid Cap Strategy for Lower CPA
> "I've been testing a new bid cap strategy to lower our client's CPA… and it's working:
> - Set the campaign budget to 3x your desired daily spend
> - Set a bid cap ~20% above your target CPA
> - Use ad set spend limits to cap real spend"
> — @benradack

### Target ROAS Nuance
> "Using highest volume asks Meta to predict just two variables: ad spend and # of purchases. Target ROAS introduces a third variable: order value. It forces Meta to factor in how much they are likely to spend with your brand."
> — @andrewjfaris

**Use Target ROAS** to optimize for higher AOV, not just conversion count.

### Budget Scaling Rules (Evan Se Framework)

| ROAS Level | Action |
|------------|--------|
| <1x | Pull back 20% |
| 1.5-2x | Increase 10% every 3-4 days |
| 2-3x | Increase 20% |
| >3x | Increase 30% |

### The 20% Rule for Scaling
> "Never increase budget by more than 20% in a single day. The algorithm freaks out."

**Safe Scaling Protocol:**
1. Identify winning ad sets (ROAS > target for 3+ days)
2. Increase budget by 15-20%
3. Wait 3 days for learning phase
4. Repeat if performance holds

### Horizontal vs Vertical Scaling

**Vertical Scaling (Same Campaign):**
- Increase budget incrementally
- Safer but slower
- Best for stable performers

**Horizontal Scaling (Duplicate & Expand):**
> "Duplicate your winning ad set, put it in a new campaign with a fresh budget. This resets the learning phase and can unlock new audiences."

- Duplicate winning ads to new campaigns
- Test new audiences with proven creatives
- Run multiple campaigns simultaneously

---

## 5. Audience Targeting Approaches

### The New Targeting Hierarchy (2026)

1. **Broad (No Targeting)** — Best for established accounts with pixel data
2. **Advantage+ Audience** — Meta's AI-powered targeting
3. **Lookalikes** — Still effective, start with 1-3%
4. **Interest Stacking** — Use as fallback, not primary

### Advantage+ Audience Setup
> "Give Meta audience suggestions, not restrictions. Add interests as suggestions, not requirements."

**Best Practices:**
- Add 5-10 interest suggestions
- Don't use exclusions unless necessary
- Let Meta expand beyond suggestions
- Trust the algorithm with data

**Key Insight:** These are SUGGESTIONS, not restrictions. Meta will branch out from your suggestions.

### Lookalike Audiences That Still Work

**High-Value Seed Audiences:**
1. Purchasers (Top 25% by value)
2. Repeat purchasers
3. High LTV customers
4. Email subscribers who purchased
5. Video viewers (75%+)

> "Your lookalike is only as good as your seed audience. Garbage in, garbage out."

**Lookalike Percentages:**
| Percentage | Quality | Reach | Use Case |
|------------|---------|-------|----------|
| 1% | Highest | Smallest | Best quality |
| 1-3% | High | Medium | Sweet spot |
| 3-5% | Medium | Large | Scaling |
| 5-10% | Lower | Very Large | Prospecting only |

**Requirements:**
- Minimum 100 users in a single country
- Recommended: 1,000-5,000 users
- Can use any custom audience type

### Retargeting in 2026
> "Retargeting isn't dead, but it's different. Focus on engagement retargeting over pixel retargeting due to iOS changes."

**Effective Retargeting Pools:**
- Video viewers (25%, 50%, 75%, 95%)
- Page/profile engagers (30, 60, 90 days)
- Website visitors with Conversions API
- Customer lists (uploaded)
- Lead form submitters

### First-Party Data Strategy
> "The advertisers winning in 2025-2026 have strong first-party data. Email lists, customer databases, CRM integrations - this is your competitive advantage."

**Actions:**
- Upload customer lists to show Meta who's a good customer
- Separate high-revenue from lower-revenue audiences
- Upload unsubscribers as exclusions
- Use all converted audiences as exclusions to avoid spending on pipeline

### Detailed Targeting Types Reference

#### Demographics
- Age, Gender (user-provided)
- Education level
- Parental status
- Work details
- Financial (income by ZIP - US only)

#### Interests
Target by topics users like based on content engagement:
- Events
- Pages they've liked
- Content they've engaged with

**Pro Tip:** Search for interests directly rather than browsing dropdowns — many topics don't appear in category lists.

#### Behaviors
- Past purchasing behaviors
- Device type
- Intent data signals
- Travel behaviors
- Facebook/Instagram shop preferences

---

## 6. Placement Optimization

### Placement Strategy by Role

| Placement | Role | Best For |
|-----------|------|----------|
| **Reels & Stories** | Grab attention, stop scroll | Cold traffic, awareness |
| **Feed** | Engagement, trust building | Mid-funnel |
| **Carousel** | Go deeper, retarget | Warm audiences, consideration |

### Best Placements for Lead Gen
- Instagram Stories + Facebook Feed perform best for leads
- Test 3+ placement combinations per campaign

### Placement Best Practices
- **Reels/Stories:** Vertical 9:16, quick hooks, first 3 seconds critical
- **Carousel:** Feature highlights, before/after, multiple products
- **Feed:** Human faces, social proof, clear CTAs

### Advantage+ Placements
- Let Meta automatically deliver across placements
- Reduces manual effort
- Often finds unexpected high-performers
- Use when scaling proven creatives

---

## 7. Key Metrics & Benchmarks

### Primary Metrics

| Metric | What It Measures | Target Range |
|--------|------------------|--------------|
| **CTR** | Click-Through Rate | 1-3% |
| **CPM** | Cost Per 1000 Impressions | $5-30 |
| **CPA** | Cost Per Acquisition | Industry dependent |
| **ROAS** | Return On Ad Spend | 3x+ (varies by margin) |
| **CVR** | Conversion Rate | 2-5% |
| **CAC** | Customer Acquisition Cost | Depends on LTV |

### Video-Specific Metrics

| Metric | Definition | Benchmark |
|--------|------------|-----------|
| **Hook Rate** | 3-sec views / impressions | Aim for 30%+ |
| **Hold Rate** | ThruPlay (15-sec) / impressions | Aim for 15%+ |
| **Hook Strength** | ThruPlay / 3-sec views | Shows story quality |

### Diagnostic Framework

> "If your hook rate is low → Your ad is dead.
> If your hold rate is bad → Your story is boring.
> If your CTR is weak → Your offer is unclear."
> — @sourfraser

### Leading Indicators to Watch

1. **Link CTR** — Should be >1% for cold traffic
2. **Hook Rate** — 3-second views / impressions (aim for 30%+)
3. **Hold Rate** — ThruPlay / 3-second views (aim for 15%+)
4. **Outbound CTR** — Clicks that leave Facebook
5. **CPM Trends** — Rising CPM = audience fatigue

### Secondary Metrics
- Frequency (keep under 3 for TOF)
- Reach (unique people reached)
- Video average watch time
- Post engagement rate
- Landing page views vs clicks

### Attribution Windows
- **Default:** 7-day click, 1-day view
- **Conservative:** 7-day click only
- **Testing:** 1-day click for quick reads

### Breakeven ROAS Calculator
```
Breakeven ROAS = 1 / (Profit Margin %)

Example:
- Product Price: $100
- Cost of Goods: $30
- Profit Margin: 70%
- Breakeven ROAS: 1 / 0.70 = 1.43x
```

### Custom Metrics to Build

**CVR (Conversion Rate):**
```
CVR = purchases / landing page views
```

**AOV (Average Order Value):**
```
AOV = purchase conversion value / purchases
```

**Actions/Reach:**
```
Actions / Reach = Shows which audience-ad combinations convert best
```

### Creative Fatigue Indicators
- CTR declining over 3+ days
- CPM increasing while CTR drops
- Frequency above 3
- Comment sentiment turning negative

**Action:** Refresh creatives every 2-4 weeks. Always have new creatives in testing.

---

## 8. Ad Copy & Creative Frameworks

### The Ad Framework (Evan Se)

**Structure:**
- **Hook:** 3-5 seconds (stop the scroll)
- **Body:** Why, solution, achieve, credibility
- **CTA:** 5-10 seconds
- **Total:** 60-90 seconds

### Hook Types That Work

1. **Direct:** "Hey, experiencing [problem]?"
2. **Case Study:** Real results from real people
3. **Expectations (Math Breakdown):** "100 leads → 85 unqualified → 15 worked → 5 signed"
4. **Stalker Hooks:** Feels personalized/targeted
5. **Problem-Agitate:** "Tired of [problem]?"
6. **Curiosity:** "I can't believe this actually worked..."
7. **Social Proof:** "100,000+ people are using this..."
8. **Contrarian:** "Stop doing [common advice]"
9. **Direct Benefit:** "Get [result] in [timeframe]"

### Copy Formulas

#### PAS (Problem-Agitate-Solution)
```
[Problem] - State the problem clearly
[Agitate] - Dig into the pain/frustration
[Solution] - Present your product as the answer
[CTA] - Clear call to action
```

#### AIDA (Attention-Interest-Desire-Action)
```
[Attention] - Hook that stops the scroll
[Interest] - Interesting fact or benefit
[Desire] - Paint the picture of results
[Action] - Tell them what to do next
```

#### Before-After-Bridge
```
Before: [Current painful situation]
After: [Desired outcome/transformation]
Bridge: [Your product/service]
```

#### Testimonial Formula
```
"[Specific result] in [timeframe]"

[2-3 sentence story of the journey]

[Product/service name] changed everything for me.

[Call to action]
```

### Short-Form Copy Guidelines
- Primary text under 125 characters for feed
- Headlines under 7 words for best CTR
- Use emojis strategically (capture attention, humanize brand)

**Winning Templates:**
- "Finally, a [product] that actually [benefit]"
- "[Number] [people] can't be wrong. Try [product] today."
- "What if you could [benefit] without [pain point]?"

### Headline Formulas
- "Get [Result] in [Timeframe]"
- "The [Adjective] Way to [Benefit]"
- "How [Audience] Are [Achieving Result]"
- "[Number]% Off [Product] - Today Only"

### Top 8 Ad Styles (Fraser Cottrell)

1. **Us vs Them** — No-brainer for brands with direct competitors
2. **Big Headline** — Got a bold claim? Base entire ad around it
3. **The Review** — Pair reviews with an image
4. **Handwritten** — Simple handwritten notes feel personal
5. **Callout** — A staple of static ads
6. **Product Grid** — Great CTRs, pattern interrupts
7. **Podcast-Style** — Can outperform traditional UGC at scale
8. **Before/After** — Show transformation visually

### UGC Best Practices

**Top of Funnel (Cold Traffic):**
- Testimonials
- Quick demos
- Daily routines

**Retargeting:**
- Objection handling
- Product in use
- Cart reminders
- Comparison clips
- Real customer reactions

**Goal:** Content that looks real, earns clicks, tells story fast

**Warning:** Overused UGC creators hurt credibility. Diversify your creator pool.

---

## 9. MVA-Specific Learnings

### MVA Lead Gen Campaign Structure

**Current Winning Setup:**
- Budget: $150/day → Scale path to $500/day
- 15 ads total: 5 "Nothing" + 10 Full Copy
- CBO campaign with broad targeting
- Geographic (state-specific) + Behavior (accident-related)

### MVA Offer Evolution

| Date | Offer Type | Conversion | Notes |
|------|------------|------------|-------|
| Jan 18 | Live Warm Transfers | 30-50% | PI-trained intake team |
| Jan 20 | Pre-Qualified Leads | 15% | Client handles intake |
| Feb 10+ | Signed Cases Only | N/A | ~$2,000 average cost |

### Winning MVA Ad Themes

1. **Quality Problems Hide as Volume**
   > "You don't have a lead volume problem. You have a quality problem disguised as volume."

2. **Your Intake Isn't the Problem**
   > "Stop blaming downstream for upstream problems. They were handed garbage."

3. **Top Firms Stay Quiet**
   > "The value is in exclusivity. The moment a source becomes known, it becomes crowded."

4. **Exclusivity/One-to-One**
   > "One campaign, one firm."

5. **Speed to Lead Myth**
   > "Speed only matters if the lead is worth calling."

6. **Vendor Dirty Secret**
   > "Most vendors don't generate leads — they aggregate them."

7. **The Math Exposé**
   > "100 leads → 85 unqualified → 15 worked → 5 signed. Your vendor won't show you this math."

### MVA "Nothing Ads" (Headlines Only)

These performed surprisingly well (low CPA):
- "Pre-Qualified MVA Leads"
- "Stop Competing for Same Leads"
- "We Limit Who We Work With"
- "Your Intake Deserves Better Leads"
- "Exclusive Means Exclusive"

### MVA Targeting Approach

- **Objective:** Lead Generation
- **Audience:** Geographic (state-specific) + Behavior (accident-related)
- **Creative:** UGC testimonials, problem-solution format
- **Form:** Keep short (name, phone, accident date, injury type)

### MVA Pricing/Economics

| Metric | Value |
|--------|-------|
| Average cost per signed case | ~$2,000 |
| Facebook leads typical cost | $200-300 per lead |
| Target CPA for booked calls | <$600 (1.5x+ ROAS) |
| Breakeven | 1x at $900 cost |

### MVA Pixel Conditioning (Critical)

> "Qualified leads fire standard event, disqualified leads do NOT — train pixel on good leads only."

This trains Meta's algorithm to find more qualified leads, not just any leads.

### MVA Creative Recommendations

**Best Performing Styles:**
- Industrial tech look with funnel diagrams (Ad #17b style)
- Landing page screenshots ("Nothing" ads)
- Infographic-style explaining the math

**Avoid:**
- Generic legal imagery
- Stock photos of handshakes
- Overly polished agency vibes

### Territory Exclusivity Angle

> "We only work with ONE PI firm per city. If you're seeing this, your area might still be open."

**Why This Works:**
- Creates urgency/scarcity
- Implies exclusivity
- Filters for serious buyers

### Law Firm Marketing Swipe File Patterns

**What's Working Across Legal Ads:**
1. Video ads dominate
2. Lead magnets (free guides) convert
3. Scarcity/Territory exclusivity
4. Anti-agency messaging ("Most agencies are all talk")
5. Risk reversal (performance-based, guarantees)
6. Trust stacks (checkmarks, reviews, years in business)
7. Identity framing ("You're a lawyer, not a marketer")
8. Specific results ("$2M revenue", "500K subscribers")

**Opportunities NOT Being Used:**
- "Burned by agencies" direct callout
- Ownership guarantee (anti-Scorpion positioning)
- AI-ready websites
- Speed guarantee (14-day delivery)
- One-time pricing transparency

---

## 10. Common Mistakes to Avoid

### Mistake #1: Not Enough Creative Volume
> "You're not spending too much money. You're testing too few creatives. The brands winning are producing 20-50 new creatives per week."

**Fix:** Implement a creative production system. Aim for 10+ new creatives per week minimum.

### Mistake #2: Killing Ads Too Early
> "I see people turn off ads after 2 days. The learning phase takes 50 conversions. Give your campaigns time."

**Fix:** Wait for at least 50 conversions OR 7 days before making decisions.

### Mistake #3: Over-Segmenting Audiences
> "Stop creating 50 different ad sets for 50 different interests. You're fragmenting your data and confusing the algorithm."

**Fix:** Consolidate ad sets. Use broad targeting or Advantage+ Audience.

### Mistake #4: Ignoring Creative Fatigue
**Signs of Fatigue:**
- CTR declining over 3+ days
- CPM increasing while CTR drops
- Frequency above 3
- Comment sentiment turning negative

**Fix:** Refresh creatives every 2-4 weeks. Always have new creatives in testing.

### Mistake #5: Wrong Conversion Event
> "If you're optimizing for purchases but only getting 10/week, you don't have enough data. Move up the funnel."

**Conversion Event Ladder:**
- 50+ conversions/week → Optimize for Purchase
- 25-50/week → Optimize for Add to Cart
- <25/week → Optimize for View Content or Leads

### Mistake #6: Poor Tracking Setup
**Required Setup:**
- Facebook Pixel (base code)
- Conversions API (server-side) — CRITICAL post-iOS 14
- Event Match Quality > 6.0
- Aggregated Event Measurement configured

### Mistake #7: Ignoring Landing Page Experience
> "Your ads can be perfect, but if your landing page sucks, you'll never convert."

**Landing Page Checklist:**
- [ ] Load time < 3 seconds
- [ ] Mobile optimized
- [ ] Message matches ad
- [ ] Clear CTA above fold
- [ ] Social proof visible

### Mistake #8: Ad-Landing Page Mismatch
> "Running clickbait UGC that gets high engagement but terrible conversion rates? Build landing pages that match what your ad promised."

**Fix:** Ensure congruence between ad promise and landing page delivery.

### Mistake #9: Not Using Proper UTM Tracking
**Template:**
```
?utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}
```

### Mistake #10: Blindly Trusting Meta
> "'Never turn off ads' is just bad advice. Some ads simply don't work—but due to high engagement (likes and comments) Meta keeps spending on that ad."

**Fix:** Turn off ads that get engagement but no conversions.

---

## 11. Tools & Resources

### AI Tools Tier List (2025-2026)

| Tool | Use Case | Tier |
|------|----------|------|
| **Claude** | All copywriting | S |
| **Nano Banana** | Image generation for ads | S |
| **DeepResearch** | Market/customer research | S |
| **Reddit Answers** | Customer language mining | S |
| **Arcads 2.0** | AI-generated UGC | A |
| **Motion** | Creative analytics | A |
| **Gemini 3 Pro** | Image composition | A |

### Competitive Research Tools
- Meta Ad Library (free)
- Custom scrapers for ad libraries
- AI agents for creative analysis

### Creative Production Systems
- Notion dashboards for managing 1,000+ ad concepts
- Creative brief templates for every ad type
- AI prompt libraries
- SOP libraries (90+ documented processes)

### Key Accounts to Follow on X

| Expert | Handle | Specialty |
|--------|--------|-----------|
| Charley T | @CTtheDisrupter | 3:2:2 Method |
| Fraser Cottrell | @sourfraser | Ad Creative |
| Nick Theriot | @nicktheriot_ | Psychology |
| Alex Cooper | @alexgoughcooper | AI in Advertising |
| Dara Denney | @DenneyDara | Creative Strategy |
| Ben Radack | @benradack | Media Buying |
| Andrew Faris | @andrewjfaris | Bidding Strategy |
| Olly Hudson | @oliverwhudson | Andromeda |

---

## 12. Quick Reference Cheat Sheets

### The Perfect Meta Ads Setup (2026)

```
Campaign: Advantage+ Shopping (or Sales objective)
├── Budget: CBO at $100-500/day
├── Attribution: 7-day click, 1-day view
│
├── Ad Set 1: Advantage+ Audience
│   ├── Ad 1: UGC Video (Problem-Solution)
│   ├── Ad 2: Static Image (Testimonial)
│   └── Ad 3: Carousel (Product Features)
│
├── Ad Set 2: 1-3% Lookalike (Purchasers)
│   ├── Ad 1: UGC Video (Before-After)
│   ├── Ad 2: Static Image (Offer-Focused)
│   └── Ad 3: Video (Founder Story)
│
└── Ad Set 3: Broad (Testing)
    ├── Ad 1: New Hook Test
    ├── Ad 2: New Angle Test
    └── Ad 3: New Format Test
```

### Budget Allocation by Funnel Stage

| Funnel Stage | Budget % | Objective |
|--------------|----------|-----------|
| TOF (Cold) | 60-70% | Traffic, Reach, Video Views |
| MOF (Warm) | 20-25% | Engagement, Leads |
| BOF (Hot) | 10-15% | Conversions, Sales |

### Daily Budget Minimums
> "Your daily budget should be at least 10x your target CPA. If your target CPA is $30, spend at least $300/day to exit learning phase quickly."

### Scaling Decision Tree

```
Is ROAS > target for 3+ days?
├── NO → Wait or test new creative
└── YES → Increase budget 15-20%
         Wait 3 days
         └── Performance holds?
             ├── YES → Repeat
             └── NO → Pull back to previous level
```

### Creative Testing Decision Tree

```
Minimum 1,000-2,000 impressions per creative?
├── NO → Wait
└── YES → Check CTR vs account median
         ├── ≥+20% → Scale winner
         ├── At median → Continue testing
         └── Materially below → Kill
```

### The 10 Commandments of Meta Ads (2026)

1. **Creative is the biggest lever** — Not targeting, not budget, not bid strategy
2. **Diversity beats volume** — Different angles, formats, hooks > more of the same
3. **First 3 seconds must be unique** — Andromeda groups similar openings together
4. **Research before creative** — Know your customer's language and pain points
5. **Simple account structure** — 1-2 CBO, minimal ad sets, let Meta optimize
6. **Test in ABO, scale in CBO** — Control testing, automate scaling
7. **Use AI tools** — Claude for copy, Nano Banana for images, automation for workflows
8. **Build systems, not just ads** — SOPs, templates, dashboards, swipe files
9. **Measure % of spend controlled** — Better than hit rate for evaluating creative sources
10. **Ad-landing page congruence** — If ROAS sucks with good engagement, fix the landing page

### Key Numbers to Remember

| Metric | Number | Context |
|--------|--------|---------|
| Creative impact | 56% | Of all campaign outcomes on Meta |
| Hook rate target | 30%+ | 3-sec views / impressions |
| Hold rate target | 15%+ | ThruPlay / impressions |
| CTR target | 1-3% | Higher for warm traffic |
| Frequency limit | <3 | For top of funnel |
| Learning phase | 50 conversions | Before algorithm stabilizes |
| Test duration | 7-14 days | Minimum for statistical significance |
| Budget scaling | 20% max | Per day increase |
| Creatives per week | 5-10 | Minimum for testing |

---

## Appendix: MVA Campaign Quick Reference

### Current Campaign Setup
- **Budget:** $150/day → Scale to $500/day
- **Structure:** 15 ads (5 Nothing + 10 Full Copy)
- **Optimization:** CBO, broad targeting with geo filters
- **Target CPA:** <$600 per booked call

### Winning Ad Angles (Copy)
1. Quality vs Volume
2. Intake Defense
3. Speed Myth
4. Vendor Secret
5. ROI Simple ($2K math)
6. Top Firms Quiet
7. Rage Bait (Vendor math)
8. FOMO (Competitors know)
9. Time Value
10. Comparison (TV vs Us)
11. Burnout

### Winning Headlines (Nothing Ads)
- Pre-Qualified MVA Leads
- Stop Competing for Same Leads
- We Limit Who We Work With
- Your Intake Deserves Better Leads
- Exclusive Means Exclusive

### Key Messaging Points
- ~$2,000 average cost per signed case
- No retainers, no setup fees
- We fund ad spend
- Pre-qualified leads (verified injury, checked liability, confirmed insurance)
- Each lead 100% exclusive (never shared)

---

*Last Updated: February 2026*
*Maintained by: Sierra (KuriosBrand AI Assistant)*

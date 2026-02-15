# Meta Ads Ultimate Resource — KuriosBrand 2026

> Compiled by Sierra's 12-agent swarm from Supermemory, Notion, local files, and web research
> Created: 2026-02-12

---

## TABLE OF CONTENTS

1. [2026 Algorithm Changes (Andromeda)](#1-2026-algorithm-changes-andromeda)
2. [Campaign Structure](#2-campaign-structure)
3. [Creative Strategy](#3-creative-strategy)
4. [Audience Targeting](#4-audience-targeting)
5. [Budget & Scaling](#5-budget--scaling)
6. [Metrics & Benchmarks](#6-metrics--benchmarks)
7. [Testing Methodology](#7-testing-methodology)
8. [Legal/PI Specific Insights](#8-legalpi-specific-insights)
9. [MVA Campaign Assets](#9-mva-campaign-assets)
10. [Implementation Checklist](#10-implementation-checklist)

---

## 1. 2026 ALGORITHM CHANGES (ANDROMEDA)

### What Changed
Meta's **Andromeda** update fundamentally shifted how ads are selected and delivered:

| Old System | New System (Andromeda) |
|------------|------------------------|
| Audience-first → then creative | **Creative-first → then audience** |
| Manual targeting rules | AI-driven creative matching |
| Every ad competes in auction | Ads filtered BEFORE entering auction |
| Pixel did heavy lifting | System analyzes visuals, copy, audio, behavioral signals |

### Key Technical Details
- Powered by **NVIDIA GH200 superchips** — processes **10,000x more ad variants**
- **100x faster** at matching users to ads
- Works with **GEM (Generative Ads Recommendation Model)** — 4x more efficient than previous ranking
- **Entity IDs** track creative themes — high similarity = CPM penalties

### What Stopped Working ❌
1. **Hyper-segmented campaign structures** — complex trees choke performance
2. **Manual interest targeting** — interests/lookalikes weakened significantly
3. **AI-generated creative spam** — algorithm detects semantic similarity
4. **Minor hook variations** — same concept + different hook ≠ diversity
5. **Frequent edits** — changes reset learning, need 14-21 day no-touch windows
6. **Low budget campaigns** — minimum $50-75/day for testing
7. **"Increase 10% daily" scaling** — outdated; use weekly 20-30% increases

### What Works Now ✅
- **Creative diversity** — radically different angles, tones, formats
- **Broad targeting** — let Andromeda find your buyers
- **Simplified structure** — fewer campaigns, better creative
- **CPMr monitoring** — early warning for creative fatigue
- **7-21 day patience** — no-touch windows for learning

### The Golden Rule
> "Meta Ads is now a creative discovery engine, not a media-buying platform."

---

## 2. CAMPAIGN STRUCTURE

### The 2-Campaign Model (2026 Standard)

```
📁 TESTING CAMPAIGN (CBO) — 10-20% of budget
├── Purpose: Test new creatives, find winners
├── Budget: $50-100/day
├── Ad Sets: 2-4 (by angle or audience)
└── Ads: 3-5 per ad set

📁 SCALING CAMPAIGN (CBO) — 80-90% of budget
├── Purpose: Scale proven winners
├── Budget: $200-500+/day
├── Ad Sets: Winners only
└── Targeting: Broad or winning audiences
```

### Ad Set Configuration

| Setting | Testing | Scaling |
|---------|---------|---------|
| Budget Type | ABO or CBO | CBO |
| Daily Budget | $25-50/ad set | Let CBO distribute |
| Targeting | Test multiple | Broad with winners |
| Placements | Advantage+ | Advantage+ |
| Optimization | Leads | Leads |

### The 3-2-2 Structure (For Testing)
> "3 ad sets, 2 creatives per ad set, 2 different hooks or angles."

- Ad Set 1: Broad targeting
- Ad Set 2: 1-3% Lookalike
- Ad Set 3: Interest stack

### For MVA Lead Gen Specifically

```
📁 [TEST] MVA Lead Gen
├── 📂 Ad Set 1: Full Copy Ads ($25/day)
│   └── Ads 1-7: Long-form problem/solution
├── 📂 Ad Set 2: Nothing Ads ($25/day)
│   └── Ads 12-14: Minimal headline + URL

📁 [SCALE] MVA Winners
├── 📂 Broad Winners
├── 📂 Lookalike Winners (1% of leads)
└── 📂 State Expansion (TX, FL, CA, GA)

📁 [RETARGET] MVA Warm (ABO)
├── 📂 Video Viewers 50%+ (3 days)
├── 📂 Page Engagers (7 days)
└── 📂 Website Visitors (14 days)
```

---

## 3. CREATIVE STRATEGY

### The New Creative Requirement
- **25-40+ diverse ads** minimum (Andromeda requirement)
- Each ad = **one specific reason to buy**
- **NO similar first 3 seconds** — Meta groups them as same ad

### Creative Mix (Recommended)
| Type | % | Purpose |
|------|---|---------|
| UGC | 40% | Authenticity, trust |
| Testimonials | 30% | Social proof |
| Product/Offer | 20% | Direct response |
| Brand/Lifestyle | 10% | Awareness |

### Ad Structure (60-90 seconds)
| Section | Duration | Content |
|---------|----------|---------|
| **Hook** | 3-5 sec | Stop the scroll |
| **Body** | 45-70 sec | Why, solution, credibility |
| **CTA** | 5-10 sec | Clear next step |

### Hook Types That Work
1. **Direct** — "Hey, experiencing [problem]?"
2. **Case Study** — Success story lead
3. **Expectations** — Math breakdown
4. **Contrarian** — "Stop doing [common advice]"
5. **Social Proof** — "100,000+ people use this..."
6. **FOMO** — "Your competitors already know..."

### Format Performance (2026)
- **Static images** still drive 60-70% of conversions
- **90% of Meta inventory is vertical** (9×16 required)
- **Video < 15 seconds** performs best
- **UGC-style** beats polished brand content

### Creative Fatigue Signals
| Signal | Threshold | Action |
|--------|-----------|--------|
| CTR drop | >30% from peak | New creative |
| Frequency spike | >2.5 suddenly | Rotate |
| CPA increase | >25% over 5 days | Test new hooks |
| CPM rising | Without CPA improvement | Refresh creative |

---

## 4. AUDIENCE TARGETING

### The New Targeting Hierarchy (2026)
1. **Broad (No Targeting)** — Best for established accounts
2. **Advantage+ Audience** — AI-powered, use suggestions
3. **Lookalikes 1-3%** — Still effective
4. **Interest Stacking** — Fallback only

### When to Use Each

| Account Stage | Best Targeting |
|---------------|----------------|
| New (0-500 conversions) | Interests + 1-3% Lookalikes |
| Established (500+ conversions) | Broad + Advantage+ |
| High-spend ($10K+/day) | Full broad |

### Lookalike Best Practices
- **1%** — Highest quality, smallest reach
- **1-3%** — Sweet spot for most
- **3-5%** — Good for scaling
- **5-10%** — Very broad, prospecting only

### High-Value Seed Audiences
1. Purchasers (Top 25% by value)
2. Repeat customers
3. High LTV customers
4. Email subscribers who converted
5. Video viewers 75%+

### Retargeting in 2026 (Post-iOS)
Focus on **engagement retargeting** over pixel:
- Video viewers (25%, 50%, 75%, 95%)
- Page/profile engagers (30, 60, 90 days)
- Website visitors with CAPI
- Customer lists (uploaded)

### Exclusions (Important)
- Existing leads/customers
- Attorneys (prevent competitor visibility)
- Insurance agents
- Known converters

---

## 5. BUDGET & SCALING

### Starting Budget Framework

| Stage | Daily Budget | Purpose |
|-------|--------------|---------|
| Testing | $50-100 | Data collection |
| Early Scaling | $200-300 | Validate winners |
| Full Scale | $500+ | Maximum volume |

### The Golden Rules
- **Daily budget = 10x target CPA** minimum
- **50 conversions/week** per ad set to optimize
- **20% max increase** per day when scaling
- **3-day wait** between budget changes
- **70/30 split** — 70% winners, 30% testing

### Scaling Triggers

| Condition | Action |
|-----------|--------|
| CPA 20%+ below target for 3 days | Increase 20% |
| CPA 40%+ below target | Increase 30-50% or duplicate |
| CPA at target, frequency <2.0 | Increase 20% cautiously |
| CPA 30%+ above target for 48hrs | Cut 30% or pause |
| Frequency >3.0 | Expand audience or pause |

### Scaling Methods

**Vertical (Same Campaign):**
- Increase budget incrementally
- Safer but slower

**Horizontal (Duplicate):**
- Duplicate winning ad set to new campaign
- Resets learning, unlocks new audiences
- Fastest scaling method

**The Duplicate Method:**
```
Original: $100/day ──────────────►
Duplicate 1: $100/day ─────────► (Day 3)
Duplicate 2: $100/day ─────────► (Day 6)
= $300/day total without shocking algorithm
```

### Bid Strategies

| Strategy | Use When |
|----------|----------|
| Lowest Cost | Testing, volume priority |
| Cost Cap | Know target CPA, want volume |
| Bid Cap | Strict cost requirements |
| ROAS Target | E-commerce with revenue tracking |

---

## 6. METRICS & BENCHMARKS

### Primary Metrics

| Metric | B2B Lead Gen Target | Kill Threshold |
|--------|---------------------|----------------|
| **CTR** | >1.0% | <0.5% |
| **CPM** | $15-35 | >$60 |
| **CPA** | $30-75 | >$150 |
| **Hook Rate** | >30% | <20% |
| **Hold Rate** | >15% | <10% |
| **Frequency** | 1-2.5 | >3.0 |

### Legal/PI Specific Benchmarks

| Metric | PI/MVA Benchmark |
|--------|------------------|
| Cost Per Lead | $100-300 |
| Lead-to-Client | 25-30% |
| Cost Per Signed | $1,200-3,000 |
| CTR | 0.99% (below average) |

### Diagnostic Framework

```
Low CTR + High CPM → Creative problem (weak hook)
High CTR + Low Conversions → Landing page problem
High CTR + High CPA → Audience mismatch
Good metrics + Bad ROAS → Offer/pricing problem
```

### Attribution Settings
- **Default:** 7-day click, 1-day view
- **Conservative:** 7-day click only
- **Quick reads:** 1-day click

---

## 7. TESTING METHODOLOGY

### Creative Testing Process

**Phase 1: Concept Testing**
- Test 5-10 different hooks/angles
- Use simple static images
- Budget: $10-20 per concept
- Winner criteria: CTR >1%

**Phase 2: Format Testing**
- Take winning concepts
- Create in multiple formats (static, video, carousel)
- Test placements

**Phase 3: Iteration**
- Winner found → create 10 variations
- Change hook, CTA, colors, format
- 70/20/10 budget rule

### Statistical Significance

| Metric | Minimum Data |
|--------|--------------|
| CTR evaluation | 2,000+ impressions |
| CPC evaluation | 100+ clicks |
| Conversion decision | 20+ conversions |

### The "2x Rule"
> If one creative has 2x the conversion rate with 10+ conversions each, it's statistically significant.

### Kill Criteria

| Timeframe | Kill If |
|-----------|---------|
| Immediate | CTR <0.5% after 2,000 impressions |
| 72 hours | CTR <1% with 3,000 impressions |
| 5-7 days | CPA >1.5x target with 5+ conversions |

### Testing Timeline

| Day | Action |
|-----|--------|
| 1-3 | Launch, let run, NO changes |
| 4-5 | Check early signals, pause clear losers |
| 7 | First winner evaluation |
| 8-14 | Scale winners, launch round 2 |

### Weekly Rhythm
- **Monday:** Review weekend, plan changes
- **Tuesday:** Implement budget increases, launch new creative
- **Wed-Thu:** Monitor, don't touch
- **Friday:** Review week, pause losers, NO major changes
- **Weekend:** Let it run

---

## 8. LEGAL/PI SPECIFIC INSIGHTS

### PI Lead Gen Economics

| Metric | Value |
|--------|-------|
| Avg MVA Settlement | $25k-$40k |
| Firm Revenue (33% contingency) | $8k-$13k |
| Avg Cost Per Signed Case | $2,000-$3,000 |
| Intake Conversion (raw leads) | 10-20% |
| Live Transfer Conversion | 30-50% |

### What Works for PI Ads

**Winning Formats:**
1. Video ads (30-sec attorney explainer)
2. Testimonial videos
3. Carousel ads (case types)
4. Real team photos (not stock)

**Winning Hooks:**
- "Injured in a [type] accident?"
- "Don't talk to insurance until..."
- "The insurance company hopes you never..."

**CTAs That Convert:**
- "Schedule Your Free Case Review"
- "Click to Speak With an Attorney Now"
- "Call Now for Free Consultation"

### The Winning Sequence (Orlando PI Case Study)
1. **Cold Video Ad** — Attorney discussing common mistakes
2. **Retargeting Ad** — Client testimonial (50%+ video viewers)
3. **Conversion Ad** — Case results + "No fee unless you win"

**Results:** 82K reach → 4.2% CTR on retargeting → 41 qualified leads → 12 signed clients (29% conversion)

### Compliance Notes
- Ads must be truthful, no misleading language
- Include disclaimers per state bar
- Can't guarantee outcomes
- No targeting by health conditions (Meta policy)

---

## 9. MVA CAMPAIGN ASSETS

### Current Ads (24 Total)

**TIER 1 — Launch First (Proven)**
| Ad | Name | CPA |
|----|------|-----|
| 1 | Quality Volume | ~$80 |
| 4 | Vendor Secret | ~$85 |
| 7 | Rage Bait | ~$70 |
| 12-14 | Nothing Ads | **$78** ✓ |

**TIER 2 — Test Next**
| Ad | Name |
|----|------|
| 6 | Top Firms Quiet |
| 8 | FOMO |
| 10 | Comparison |

**TIER 3 — Rotate In**
- Ads 2, 3, 5, 9, 11

### V2 Campaign Ads (10 New)
- Guarantee Hook (7 cases in 30 days or free)
- Price Breakdown
- Exposé Style
- Model Problem
- Time Angle
- Emoji Attention Grabber
- Intake Defense
- Comparison Angle
- Nothing Style Guarantee

### Style Requirements
- **Background:** Near-black (#1A1A1A)
- **Accent:** #3399FF blue highlights
- **Bad options:** Red ELIMINATED stamps
- **Aesthetic:** Data visualization / financial calculator
- **Corners:** Sharp only (no rounded)
- **Avoid:** Warm colors, photos, soft gradients

### Key Messaging
- **Pricing:** ~$3,000/signed case
- **Qualifier:** 10+ cases/month firms
- **Team:** MVA-trained intake
- **Retention:** 87% after 90 days
- **Guarantee:** 7 cases in 30 days (V2)

---

## 10. IMPLEMENTATION CHECKLIST

### Before Launch
- [ ] Meta Pixel installed and firing
- [ ] Conversions API (CAPI) connected
- [ ] Event Match Quality >6.0
- [ ] Custom conversion for "Qualified Lead"
- [ ] 1% Lookalike from existing leads
- [ ] Customer list uploaded for exclusion
- [ ] UTM parameters configured
- [ ] Landing page <3 second load time

### Creative Prep
- [ ] 7 full-copy ads (static images)
- [ ] 3 nothing ads (minimal text)
- [ ] All images square (1:1)
- [ ] Ad copy for each (headline, primary, description)

### Campaign Setup
- [ ] Testing campaign: CBO, $50-100/day
- [ ] 2 ad sets minimum (Full Copy + Nothing)
- [ ] Broad targeting (US, 35-65)
- [ ] Advantage+ placements
- [ ] 7-day click, 1-day view attribution

### Post-Launch
- [ ] Day 1-3: NO changes
- [ ] Day 5: Pause clear losers
- [ ] Day 7: Identify winners
- [ ] Week 2: Move winners to Scaling campaign
- [ ] Ongoing: 5-10 new creatives/week

---

## QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────────┐
│           META ADS 2026 QUICK REF               │
├─────────────────────────────────────────────────┤
│ STRUCTURE:                                      │
│ • 2 campaigns: Testing (20%) + Scaling (80%)    │
│ • 3-5 ads per ad set, 2-4 ad sets              │
│ • CBO for both, ABO for retargeting            │
│                                                 │
│ TARGETING:                                      │
│ • Broad > Advantage+ > Lookalike > Interests   │
│ • 1-3% lookalikes are sweet spot               │
│ • Exclude existing leads/attorneys             │
│                                                 │
│ BUDGET:                                         │
│ • Start $50-100/day testing                    │
│ • 10x target CPA minimum                       │
│ • Scale 20% max per day                        │
│ • Wait 3 days between changes                  │
│                                                 │
│ CREATIVE:                                       │
│ • 25-40+ diverse ads needed                    │
│ • First 3 seconds must be unique               │
│ • UGC > polished brand content                 │
│ • Refresh every 2-4 weeks                      │
│                                                 │
│ METRICS (B2B Lead Gen):                        │
│ • CTR: >1.0% good, <0.5% kill                  │
│ • CPA: $30-75 target                           │
│ • Frequency: <2.5 good, >3.0 pause             │
│                                                 │
│ PI/MVA SPECIFIC:                               │
│ • CPL: $100-300 normal                         │
│ • Lead-to-client: 25-30%                       │
│ • Video + retargeting = winning combo          │
└─────────────────────────────────────────────────┘
```

---

*Document compiled from 12 parallel research agents. Sources: Supermemory, Notion KB, local files (26 documents), web research (2026 algorithm changes, legal benchmarks), expert X/Twitter insights (100+ posts).*

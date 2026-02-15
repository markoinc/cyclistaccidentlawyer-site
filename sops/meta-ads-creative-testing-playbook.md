# Meta Ads Creative Testing Playbook

## Overview
A systematic framework for testing, evaluating, and iterating on Meta ad creatives. This playbook provides specific rules to remove guesswork and ensure data-driven decisions.

---

## 1. Test Structure Rules

### Creatives Per Test
| Test Type | # of Creatives | Budget/Creative/Day | Min Total Daily Budget |
|-----------|----------------|---------------------|------------------------|
| **Initial Concept Test** | 3-5 creatives | $10-20 | $50-100 |
| **Iteration Test** | 2-3 variations | $15-25 | $45-75 |
| **Scale Validation** | 1-2 proven winners | $50+ | $100+ |

**Rule:** Never test more than 5 creatives simultaneously. Meta's algorithm needs enough data per creative to optimize.

### Campaign Structure for Testing
```
Campaign: Creative Test [Date] [Concept Name]
├── Ad Set: Broad Targeting (proven audience)
│   ├── Ad 1: Creative Variant A
│   ├── Ad 2: Creative Variant B
│   ├── Ad 3: Creative Variant C
│   └── (max 5 ads)
```

**Why single ad set?** Isolates creative performance. Multiple ad sets introduce audience variables.

---

## 2. Budget Rules

### Minimum Spend Thresholds
| Metric | Minimum Spend Before Decision |
|--------|------------------------------|
| **CTR evaluation** | 1,000 impressions per creative |
| **CPC evaluation** | 50+ clicks per creative |
| **Conversion evaluation** | 2-3x your target CPA spent |
| **Full test conclusion** | $50-100 per creative minimum |

### Budget Calculation Formula
```
Minimum Test Budget = (Target CPA × 3) × Number of Creatives

Example: $50 CPA target, testing 4 creatives
= ($50 × 3) × 4 = $600 total test budget needed
```

**Rule:** If you can't afford $150+ per creative in test budget, reduce the number of creatives being tested.

---

## 3. Test Duration Rules

### Minimum Test Duration
| Scenario | Minimum Duration |
|----------|------------------|
| **Standard test** | 5-7 days |
| **High-ticket ($500+ CPA)** | 10-14 days |
| **Low-ticket (< $20 CPA)** | 3-5 days |

### Why These Durations?
- **Days 1-2:** Learning phase, data unreliable
- **Days 3-4:** Patterns emerge, early signals
- **Days 5-7:** Statistical confidence, decision point

**Rule:** NEVER kill a creative before 72 hours and 1,000 impressions, regardless of early metrics.

### Day-of-Week Consideration
- Tests should span at least one full weekday-weekend cycle
- Start tests Monday-Wednesday for best data spread
- Avoid starting Friday (incomplete weekend data by Monday)

---

## 4. Statistical Significance Rules

### When Do You Have Enough Data?

**Minimum thresholds for confident decisions:**
| Metric | Minimum Sample | Confidence Level |
|--------|----------------|------------------|
| CTR | 2,000 impressions | 90%+ |
| CPC | 100 clicks | 90%+ |
| CPL/CPA | 20+ conversions | 80%+ |
| ROAS | 30+ purchases | 85%+ |

### Quick Significance Check
Use this simplified rule:
```
If Creative A has 20%+ better performance than Creative B 
AND both have 50+ of the measured event (clicks, leads, purchases)
= Statistically significant, act on it

If difference is < 20% with < 100 events each
= Not yet significant, continue testing
```

### The "2x Rule"
**If one creative has 2x the conversion rate of another with 10+ conversions each, it's a winner.** Don't wait for more data.

---

## 5. Kill Criteria (When to Turn Off)

### Immediate Kill (Within 24-48 hours)
Turn off immediately if:
- [ ] CTR < 0.5% after 2,000+ impressions
- [ ] CPM > 3x account average (signals Meta dislikes the creative)
- [ ] 0 clicks after 1,000 impressions
- [ ] Ad rejected or restricted

### Kill After 72 Hours
Turn off if:
- [ ] CTR < 1% with 3,000+ impressions (cold traffic)
- [ ] CTR < 2% with 3,000+ impressions (warm/retargeting)
- [ ] CPC > 2x your target CPC
- [ ] Cost per result > 2x your target with 3+ results
- [ ] Significantly underperforming vs other creatives in test (< 50% of best performer)

### Kill After 5-7 Days
Turn off if:
- [ ] CPA > 1.5x target with 5+ conversions
- [ ] ROAS < 70% of target with $500+ spend
- [ ] Clear loser vs other creatives (bottom performer by 30%+)

### The "Half-Life Rule"
**If a creative's performance drops by 50% from its first 3-day average over the next 3 days, kill it.** This indicates fatigue or algorithm deprioritization.

---

## 6. Scale Criteria (When to Increase Budget)

### Signs of a Winner (Green Lights)
| Metric | Winner Threshold |
|--------|------------------|
| CTR | > 1.5% (cold) / > 3% (warm) |
| CPA | < 80% of target |
| ROAS | > 120% of target |
| Hook Rate (video) | > 25% watched 3+ sec |
| Hold Rate (video) | > 10% watched 50%+ |

### Scale Decision Framework
```
SCALE if ALL of these are true:
✓ CPA/ROAS at or better than target
✓ 10+ conversions attributed
✓ Performance stable for 3+ days
✓ Outperforming other creatives by 20%+
```

### How to Scale (Progressive Method)
| Day | Budget Increase | Condition to Continue |
|-----|-----------------|----------------------|
| Day 1 | +20-30% | - |
| Day 2 | Hold | Monitor for 24h |
| Day 3 | +20-30% if stable | CPA within 20% of pre-scale |
| Day 4 | Hold | Monitor for 24h |
| Day 5+ | Repeat | Until efficiency drops |

**Rule:** Never increase budget more than 30% in a single day. Larger jumps reset the learning phase.

### Scale Kill Switch
If after scaling:
- CPA increases by > 30% for 2 consecutive days → Reduce budget by 50%
- CPA increases by > 50% → Pause and reassess

---

## 7. Iteration Methodology

### What to Test (Priority Order)

**Tier 1 (Biggest Impact):**
1. Hook (first 3 seconds of video / headline of static)
2. Visual style (UGC vs polished, person vs product)
3. Offer/CTA

**Tier 2 (Medium Impact):**
4. Body copy length
5. Format (video vs carousel vs static)
6. Thumbnail/cover image

**Tier 3 (Refinement):**
7. Colors/fonts
8. Music/sound
9. CTA button text

### Iteration Framework: "Winner + Variations"

When you find a winner:
```
Winner Creative = Control

Create 2-3 variations changing ONE element:
├── Variation A: New hook, same body
├── Variation B: Same hook, new body  
├── Variation C: Same content, new format

Test against Control with equal budget
```

### The 70/20/10 Creative Budget Rule
| Category | % of Creative Budget | Description |
|----------|---------------------|-------------|
| **Proven Winners** | 70% | Scaled creatives with track record |
| **Iterations** | 20% | Variations of winners |
| **Wild Tests** | 10% | Completely new concepts |

### Iteration Velocity
- **Test new creatives:** Weekly minimum
- **Refresh winning creatives:** Every 2-4 weeks
- **Full concept overhaul:** Monthly or when performance drops 30%+

---

## 8. Creative Fatigue Signals

### Early Warning Signs
- CTR dropping 20%+ week-over-week
- Frequency > 2.5 on prospecting, > 5 on retargeting
- CPM increasing while CTR stable (audience exhaustion)
- Comments saying "I keep seeing this ad"

### Fatigue Response Protocol
| Fatigue Level | Action |
|---------------|--------|
| **Mild** (10-20% CTR drop) | Reduce budget 20%, prepare iterations |
| **Moderate** (20-40% CTR drop) | Launch new creatives immediately |
| **Severe** (40%+ CTR drop) | Pause creative, launch replacements |

---

## 9. Testing Checklist (Use For Every Test)

### Pre-Launch
- [ ] Clear hypothesis for what you're testing
- [ ] Single variable isolated (or clearly documented multi-variable test)
- [ ] Budget sufficient for statistical significance
- [ ] Tracking/pixels verified
- [ ] UTMs applied
- [ ] Creative specs correct for placements

### During Test
- [ ] Check metrics daily (don't change anything days 1-3)
- [ ] Document observations in creative testing log
- [ ] Apply kill rules on schedule

### Post-Test
- [ ] Record results in testing database
- [ ] Document learnings (what worked, what didn't, why)
- [ ] Plan iterations based on findings
- [ ] Archive losing creatives with notes
- [ ] Schedule winner scaling

---

## 10. Quick Reference Decision Tree

```
START: Creative has run 72+ hours with 1,000+ impressions

├── CTR < 0.5%? 
│   └── YES → KILL immediately
│   └── NO → Continue ↓
│
├── CPA > 2x target with 3+ conversions?
│   └── YES → KILL
│   └── NO → Continue ↓
│
├── Worst performer by 50%+ vs other creatives?
│   └── YES → KILL
│   └── NO → Continue ↓
│
├── CPA < target with 10+ conversions?
│   └── YES → SCALE (20-30% budget increase)
│   └── NO → Continue ↓
│
├── Test duration > 7 days?
│   └── NO → Continue running
│   └── YES → Make final call ↓
│
└── Final Decision:
    ├── CPA within 20% of target → ITERATE (test variations)
    ├── CPA > 1.5x target → KILL
    └── Top performer but not at target → ITERATE with new hooks
```

---

## 11. Metrics Benchmarks by Industry

Use these as starting points; adjust based on your data:

| Industry | Target CTR | Acceptable CPC | Typical CPM |
|----------|------------|----------------|-------------|
| E-commerce | 1.0-2.0% | $0.50-2.00 | $8-15 |
| Lead Gen (B2C) | 0.8-1.5% | $1.00-3.00 | $10-20 |
| Lead Gen (B2B) | 0.5-1.0% | $2.00-8.00 | $15-35 |
| SaaS | 0.6-1.2% | $1.50-5.00 | $12-25 |
| Legal (MVA) | 0.8-1.5% | $2.00-6.00 | $15-30 |

---

## 12. Documentation Template

Track every test with this format:

```
## Creative Test: [Name] - [Date]

**Hypothesis:** [What are you testing and why]
**Test Duration:** [Start] to [End]
**Budget:** $[X] per creative, $[Y] total

### Creatives Tested:
1. [Creative A description]
2. [Creative B description]
3. [Creative C description]

### Results:
| Creative | Impressions | CTR | Clicks | CPA | ROAS | Result |
|----------|-------------|-----|--------|-----|------|--------|
| A        |             |     |        |     |      |        |
| B        |             |     |        |     |      |        |
| C        |             |     |        |     |      |        |

### Winner: [Creative X]
**Why it won:** [Analysis]

### Learnings:
- [Key takeaway 1]
- [Key takeaway 2]

### Next Steps:
- [ ] [Iteration plan]
- [ ] [Scale plan]
```

---

## Summary: The 7 Cardinal Rules

1. **Never test more than 5 creatives at once**
2. **Minimum 72 hours + 1,000 impressions before any decision**
3. **Kill at 2x target CPA with 3+ conversions**
4. **Scale at <80% target CPA with 10+ conversions**
5. **Increase budget max 30% per day when scaling**
6. **Always test one variable at a time for clear learnings**
7. **Document everything - your future self will thank you**

---

*Version 1.0 | Created: 2026-02-09*
*For: Kurios Brand / MVA Lead Gen*

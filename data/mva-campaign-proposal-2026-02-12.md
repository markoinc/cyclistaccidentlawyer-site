# MVA Campaign Proposal — Ready to Implement
> Created: 2026-02-12 | For: KuriosBrand LLC | By: Sierra

---

## EXECUTIVE SUMMARY

**Objective:** Launch 11-ad creative test for MVA lead generation
**Budget:** $150/day testing → scale to $500+/day
**Timeline:** 3-week test → ongoing scaling
**Target:** Beat current $78 CPA baseline

---

## CAMPAIGN STRUCTURE

### Campaign 1: [TEST] MVA Lead Gen - Feb 2026

| Setting | Value |
|---------|-------|
| **Objective** | Leads |
| **Budget Type** | CBO |
| **Daily Budget** | $100/day |
| **Bid Strategy** | Lowest Cost |
| **Attribution** | 7-day click, 1-day view |

#### Ad Set 1: Full Copy Ads
| Setting | Value |
|---------|-------|
| **Budget Minimum** | $50/day |
| **Targeting** | Broad: US, Ages 35-65 |
| **Placements** | Advantage+ |
| **Ads** | 7 (Ads 1-7 from Notion doc) |

#### Ad Set 2: Nothing Ads
| Setting | Value |
|---------|-------|
| **Budget Minimum** | $50/day |
| **Targeting** | Broad: US, Ages 35-65 |
| **Placements** | Advantage+ |
| **Ads** | 3 (Ads 12-14 from Notion doc) |

### Campaign 2: [SCALE] MVA Winners (Week 2+)

| Setting | Value |
|---------|-------|
| **Objective** | Leads |
| **Budget Type** | CBO |
| **Daily Budget** | $200-400/day |
| **Bid Strategy** | Cost Cap at $100 |

#### Ad Set 1: Broad Winners
- Winning ads from testing
- US, 35-65, no interests

#### Ad Set 2: Lookalike Winners
- 1% Lookalike of converted leads
- Same winning ads

#### Ad Set 3: State Expansion (Optional)
- TX, FL, CA, GA targeting
- Same winning ads

---

## THE 11 ADS TO TEST

### TIER 1 — Priority Launch

| # | Name | Hook | Expected CPA |
|---|------|------|--------------|
| 1 | Quality Volume | "You have a lead quality problem disguised as volume" | $65-85 |
| 4 | Vendor Secret | "Most vendors don't generate leads. They aggregate them." | $70-90 |
| 7 | Rage Bait | "They sold you 100 'exclusive' leads... you signed 5 cases" | $60-80 |
| 12 | Nothing A | "Stop Buying Leads. Start Receiving Cases." | $70-85 |
| 13 | Nothing B | "PI Attorneys: Signed MVA Cases — $3k Avg" | $70-85 |
| 14 | Nothing C | "Signed MVA Cases Delivered — 10+ Cases/Month Firms Only" | $70-85 |

### TIER 2 — Secondary Test

| # | Name | Hook | Expected CPA |
|---|------|------|--------------|
| 6 | Top Firms Quiet | "The best systems aren't crowdsourced" | $85-110 |
| 8 | FOMO | "Your market is either yours or someone else's" | $80-105 |
| 10 | Comparison | "TV: $50K, Billboards: $30K, Us: $3K/case" | $75-95 |

### TIER 3 — Rotate In

| # | Name | Hook |
|---|------|------|
| 5 | ROI Simple | "$3,000 per signed MVA case. That's the average." |
| 11 | Burnout | "Calling 100 leads to find 5 real cases is soul-crushing" |

---

## SUCCESS CRITERIA

### Winner Identification
| Metric | Threshold |
|--------|-----------|
| Minimum Spend | $150+ per ad |
| CPL | ≤ $78 (beat baseline) |
| Conversions | 3+ leads |
| Quality | >15% qualified rate |

### Kill Criteria
| Condition | Action |
|-----------|--------|
| $100 spent, 0 leads | Kill immediately |
| CPL >$156 (2x target) after $100 | Kill |
| CTR <0.5% after 2,000 impressions | Kill |

### Scaling Triggers
| Performance | Action |
|-------------|--------|
| CPL <$78 for 3 days | Move to Scaling campaign |
| CPL <$60 for 3 days | Duplicate + increase 30% |
| Frequency >2.5 | Expand audience |

---

## TIMELINE

### Week 1: Testing Phase
| Day | Action |
|-----|--------|
| Day 1 | Launch all 11 ads in Testing campaign |
| Day 2-3 | Observe, NO changes |
| Day 4 | Check early signals (CTR, CPM) |
| Day 5 | Pause clear losers ($75+ spent, 0 leads) |
| Day 7 | First winner evaluation |

### Week 2: Optimization
| Day | Action |
|-----|--------|
| Day 8 | Move top 3-4 winners to Scaling campaign |
| Day 9 | Launch Scaling at $200/day CBO |
| Day 10-14 | Monitor, scale winners 20% if CPL holds |

### Week 3+: Scale
| Action | Trigger |
|--------|---------|
| Increase to $300/day | CPL stable at <$80 |
| Increase to $500/day | CPL stable at <$70 |
| Add state-specific ad sets | Maxing out broad |
| Launch V2 ads | Need more creative volume |

---

## BUDGET PROJECTION

### Week 1 (Testing)
| Item | Daily | Weekly |
|------|-------|--------|
| Testing Campaign | $100 | $700 |
| **Total** | **$100** | **$700** |

### Week 2 (Testing + Scaling)
| Item | Daily | Weekly |
|------|-------|--------|
| Testing | $50 | $350 |
| Scaling | $200 | $1,400 |
| **Total** | **$250** | **$1,750** |

### Week 3+ (Full Scale)
| Item | Daily | Weekly |
|------|-------|--------|
| Testing | $50 | $350 |
| Scaling | $400 | $2,800 |
| **Total** | **$450** | **$3,150** |

### Expected Results (Week 3)
| Metric | Projection |
|--------|------------|
| Daily Spend | $450 |
| CPL (optimistic) | $70 |
| CPL (conservative) | $90 |
| Daily Leads | 5-7 |
| Weekly Leads | 35-50 |
| Monthly Leads | 150-200 |

---

## TRACKING SETUP

### Pixel Events
| Event | Trigger |
|-------|---------|
| PageView | Landing page load |
| Lead | Form submission (all) |
| CompleteRegistration | Qualified lead only (pixel conditioning) |

### UTM Template
```
?utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.name}}
```

### Lead Quality Tracking
- Tag leads by ad in GHL
- Track qualified rate per ad
- Weekly quality review

---

## NEXT STEPS

### Immediate (Today)
- [ ] Confirm Facebook Page ID for ads
- [ ] Verify landing page tracking
- [ ] Generate remaining ad images (Nano Banana)

### Before Launch
- [ ] Upload all 11 creatives
- [ ] Configure ad sets per above
- [ ] Set up lead notifications in GHL
- [ ] Create reporting dashboard

### Launch Day
- [ ] Activate Testing campaign
- [ ] Verify events firing
- [ ] Set calendar reminder: Day 5 review

---

## MARKO'S APPROVAL NEEDED

1. **Budget:** $100/day testing → $450/day by week 3?
2. **Facebook Page:** Which page to run from?
3. **Go-live date:** Ready when you are

---

## API IMPLEMENTATION (Optional)

If you want me to create via API instead of Ads Manager:

```javascript
// Testing Campaign
{
  name: "[TEST] MVA Lead Gen - Feb 2026",
  objective: "OUTCOME_LEADS",
  status: "PAUSED",
  special_ad_categories: [],
  daily_budget: 10000  // $100 in cents
}

// Ad Set
{
  name: "Full Copy Ads",
  campaign_id: "<campaign_id>",
  daily_budget: 5000,  // $50 minimum
  targeting: {
    geo_locations: { countries: ["US"] },
    age_min: 35,
    age_max: 65
  },
  optimization_goal: "LEAD_GENERATION"
}
```

**I have full API access to act_1940929156491998. Just say the word.**

---

*Projection saved to Notion for comparison in 2 weeks.*

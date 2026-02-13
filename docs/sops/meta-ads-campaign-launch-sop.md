# SOP: Meta Ads Campaign Research, Build & Launch

**Version:** 1.0  
**Created:** 2026-02-13  
**Author:** Sierra (AI Agent)  
**Purpose:** Enable autonomous agent execution of Meta ad campaign launches  
**Estimated Time:** 2-4 hours (automated), 4-8 hours (manual)

---

## Overview

This SOP documents the complete process for researching, building, and launching a Meta (Facebook/Instagram) advertising campaign for lead generation. It was developed during the launch of the MVA (Motor Vehicle Accident) lead gen campaign for KuriosBrand.

### Prerequisites

- [ ] Meta Business Manager access
- [ ] Ad Account with spending capability
- [ ] Meta Marketing API credentials (System User Token)
- [ ] Facebook Page linked to ad account
- [ ] Instagram Account linked (optional but recommended)
- [ ] Landing page/lead form ready
- [ ] Budget approved

### Credentials Required

```
~/.config/meta-ads/credentials.json
{
  "ad_account_id": "act_XXXXXXXXXX",
  "system_user_id": "XXXXXXXXXX",
  "access_token": "EAAG...",
  "page_id": "XXXXXXXXXX"
}
```

---

## Phase 1: Competitive Research

### Step 1.1: Identify Top Competitors

**Objective:** Find 3-5 advertisers in your niche who are running successful campaigns.

**Method:**
1. Go to [Meta Ad Library](https://www.facebook.com/ads/library)
2. Set filters:
   - Country: United States
   - Ad Category: All Ads
   - Media Type: Video (for engagement analysis)
3. Search for niche keywords:
   - For MVA: "car accident lawyer", "injury attorney", "settlement", "accident lawyer near me"
4. Sort by: "Longest Running" (indicates profitability)

**What to look for:**
- Ads running 30+ days (proven winners)
- High engagement (comments, shares visible)
- Multiple ad variations (indicates testing/scaling)
- Professional creative quality

**Output:** List of 3-5 competitor pages with active, long-running ads.

```bash
# Example competitor research output
competitors:
  - name: "Vibe Marketing Agency"
    page_id: "vibemarketing"
    ad_count: 50+
    longest_running: "90+ days"
    creative_style: "UGC testimonials, dashcam footage"
    
  - name: "Royce Law"
    page_id: "roycelawoffices"
    ad_count: 30+
    longest_running: "60+ days"
    creative_style: "Settlement reveals, attorney direct-to-camera"
```

### Step 1.2: Analyze Winning Ad Creatives

**Objective:** Identify patterns in successful ad creatives.

**For each competitor, document:**

1. **Hook Analysis (First 3 seconds)**
   - What grabs attention?
   - Visual hook (dramatic footage, text overlay, face)
   - Audio hook (statement, question, dramatic sound)
   
2. **Creative Format**
   - UGC (User Generated Content) testimonials
   - Dashcam/surveillance footage
   - Settlement amount reveals
   - Attorney talking head
   - Before/after scenarios
   - News-style reporting

3. **Copy Patterns**
   - Primary text structure
   - Headline formula
   - CTA language
   - Emotional triggers used

4. **Technical Specs**
   - Aspect ratio (9:16, 1:1, 4:5)
   - Video length
   - Caption style (burned-in vs. none)
   - Music/sound effects

**Template for Creative Analysis:**

```markdown
## Ad Analysis: [Competitor Name] - [Ad Description]

**URL:** [Ad Library Link]
**Running Since:** [Date or duration]
**Platforms:** FB Feed / IG Feed / IG Stories / IG Reels

### Hook (0-3 sec)
- Visual: [Description]
- Audio: [First words spoken or sound]
- Text Overlay: [Any text shown]

### Body (3-15 sec)
- Key message: [Main point]
- Social proof: [Settlement amount, testimonial, etc.]
- Pain points addressed: [List]

### CTA (Final seconds)
- Visual CTA: [Button, text overlay]
- Verbal CTA: [What they say]
- Urgency element: [If any]

### Copy
**Primary Text:**
> [Exact copy or paraphrase]

**Headline:**
> [Exact headline]

**CTA Button:** [Learn More / Get Quote / etc.]

### Performance Indicators
- Estimated engagement: [High/Medium/Low based on visible reactions]
- Number of variations: [How many similar ads]
- Running duration: [X days/weeks/months]
```

### Step 1.3: Download & Organize Assets

**Objective:** Collect creative assets for inspiration or direct use (if licensed/created).

**Methods to obtain creatives:**

1. **Meta Ad Library Download** (for analysis only)
   ```bash
   # Use browser developer tools or ad library download feature
   # Note: These are for reference, not direct use without rights
   ```

2. **Stock Footage Sources**
   - Pexels (free)
   - Storyblocks (subscription)
   - Artgrid (subscription)
   
3. **UGC Creation**
   - Hire UGC creators on Fiverr/Billo
   - Use customer testimonials (with permission)
   
4. **AI-Generated**
   - ElevenLabs for voiceover
   - Runway/Pika for video generation
   - Midjourney for images

**Asset Organization:**

```
/campaigns/[campaign-name]/
├── research/
│   ├── competitor-analysis.md
│   ├── ad-library-screenshots/
│   └── swipe-file/
├── assets/
│   ├── videos/
│   │   ├── raw/
│   │   └── edited/
│   ├── images/
│   ├── audio/
│   └── copy/
├── creatives/
│   ├── ad-01-dashcam/
│   ├── ad-02-testimonial/
│   └── ad-03-settlement/
└── docs/
    ├── targeting-strategy.md
    └── launch-checklist.md
```

---

## Phase 2: Strategy Development

### Step 2.1: Define Campaign Objective

**Objective:** Determine the right campaign objective based on business goal.

| Business Goal | Campaign Objective | Optimization |
|--------------|-------------------|--------------|
| Lead collection | Leads | Leads (form submissions) |
| Website traffic | Traffic | Link Clicks |
| Brand awareness | Awareness | Reach |
| Sales/Purchases | Sales | Purchases |
| App installs | App Promotion | App Installs |

**For MVA Lead Gen:** Use "Leads" objective with Lead Form or Landing Page.

### Step 2.2: Targeting Strategy

**Objective:** Define audience targeting approach.

**Recommended: Broad Targeting with Advantage+**

Meta's AI has become highly effective at finding converters. Broad targeting often outperforms detailed targeting.

```json
{
  "targeting": {
    "geo_locations": {
      "countries": ["US"]
    },
    "age_min": 18,
    "age_max": 65,
    "targeting_automation": {
      "advantage_audience": 1
    }
  }
}
```

**When to use detailed targeting:**
- Very niche B2B audiences
- Geographic restrictions (local businesses)
- Specific demographic requirements

**Interest-based targeting (if needed):**
```json
{
  "flexible_spec": [
    {
      "interests": [
        {"id": "6003139666611", "name": "Personal injury lawyer"},
        {"id": "6003025268438", "name": "Law firm"}
      ]
    }
  ]
}
```

### Step 2.3: Budget Strategy

**Objective:** Determine optimal budget allocation.

**Campaign Budget Optimization (CBO) - Recommended:**
- Set budget at campaign level
- Meta distributes to best-performing ad sets
- Minimum: $50/day for testing
- Scale: $100-500/day after winners identified

**Ad Set Budget Optimization (ABO):**
- Set budget at ad set level
- More control, less AI optimization
- Use when testing specific audiences

**Budget Phases:**

| Phase | Daily Budget | Duration | Goal |
|-------|-------------|----------|------|
| Testing | $50-100 | 3-7 days | Find winning creatives |
| Validation | $100-200 | 7-14 days | Confirm performance |
| Scaling | $200-1000+ | Ongoing | Maximize volume |

### Step 2.4: Creative Strategy Matrix

**Objective:** Plan creative variations for testing.

**The 3x3 Creative Matrix:**

| Hook Type | Format 1 (UGC) | Format 2 (Footage) | Format 3 (Direct) |
|-----------|----------------|--------------------|--------------------|
| Question | "Were you in an accident?" + testimonial | "Were you in an accident?" + dashcam | "Were you in an accident?" + attorney |
| Statement | "$500K settlement story" + testimonial | "$500K settlement story" + footage | "$500K settlement story" + attorney |
| Shock | Dramatic opening + testimonial | Dramatic footage + reveal | Dramatic stat + attorney |

**Minimum viable test:** 6 creatives (2 hooks × 3 formats)

---

## Phase 3: Campaign Build

### Step 3.1: Prepare API Environment

**Objective:** Set up Meta Marketing API access.

```bash
# Load credentials
CREDS=$(cat ~/.config/meta-ads/credentials.json)
AD_ACCOUNT_ID=$(echo $CREDS | jq -r '.ad_account_id')
ACCESS_TOKEN=$(echo $CREDS | jq -r '.access_token')
PAGE_ID=$(echo $CREDS | jq -r '.page_id')

# Test API access
curl -G "https://graph.facebook.com/v21.0/$AD_ACCOUNT_ID" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "fields=name,account_status,amount_spent"
```

**Expected response:**
```json
{
  "name": "Your Ad Account Name",
  "account_status": 1,
  "amount_spent": "XXXXX",
  "id": "act_XXXXXXXXXX"
}
```

### Step 3.2: Upload Creative Assets

**Objective:** Upload videos/images to Meta for use in ads.

**Upload Video:**
```bash
# Upload video to ad account
curl -X POST "https://graph.facebook.com/v21.0/$AD_ACCOUNT_ID/advideos" \
  -F "access_token=$ACCESS_TOKEN" \
  -F "source=@/path/to/video.mp4" \
  -F "title=Ad Creative - Dashcam Footage"
```

**Response:**
```json
{
  "id": "VIDEO_ID_HERE"
}
```

**Upload Image:**
```bash
curl -X POST "https://graph.facebook.com/v21.0/$AD_ACCOUNT_ID/adimages" \
  -F "access_token=$ACCESS_TOKEN" \
  -F "filename=@/path/to/image.jpg"
```

**Track uploaded assets:**
```json
{
  "assets": [
    {"name": "dashcam-footage-1", "video_id": "123456789", "type": "video"},
    {"name": "testimonial-ugc-1", "video_id": "987654321", "type": "video"},
    {"name": "thumbnail-1", "image_hash": "abc123def456", "type": "image"}
  ]
}
```

### Step 3.3: Create Campaign

**Objective:** Create the parent campaign container.

```bash
# Create campaign with CBO
CAMPAIGN_RESPONSE=$(curl -X POST "https://graph.facebook.com/v21.0/$AD_ACCOUNT_ID/campaigns" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "name=[TEST] MVA Lead Gen - $(date +%b\ %Y)" \
  -d "objective=OUTCOME_LEADS" \
  -d "status=PAUSED" \
  -d "special_ad_categories=[\"HOUSING_EMPLOYMENT_CREDIT\"]" \
  -d "daily_budget=5000" \
  -d "bid_strategy=LOWEST_COST_WITHOUT_CAP")

CAMPAIGN_ID=$(echo $CAMPAIGN_RESPONSE | jq -r '.id')
echo "Campaign created: $CAMPAIGN_ID"
```

**Key Parameters:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| objective | OUTCOME_LEADS | For lead generation |
| status | PAUSED | Start paused, review before launch |
| special_ad_categories | HOUSING_EMPLOYMENT_CREDIT | Required for legal ads |
| daily_budget | 5000 | In cents ($50.00) |
| bid_strategy | LOWEST_COST_WITHOUT_CAP | Let Meta optimize |

### Step 3.4: Create Ad Set

**Objective:** Define targeting and placement settings.

```bash
# Create ad set with broad targeting
ADSET_RESPONSE=$(curl -X POST "https://graph.facebook.com/v21.0/$AD_ACCOUNT_ID/adsets" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "campaign_id=$CAMPAIGN_ID" \
  -d "name=All Ads - Testing" \
  -d "status=PAUSED" \
  -d "billing_event=IMPRESSIONS" \
  -d "optimization_goal=LEAD_GENERATION" \
  -d "destination_type=WEBSITE" \
  -d "promoted_object={\"page_id\":\"$PAGE_ID\"}" \
  -d "targeting={\"geo_locations\":{\"countries\":[\"US\"]},\"age_min\":18,\"age_max\":65,\"targeting_automation\":{\"advantage_audience\":1}}" \
  -d "attribution_spec=[{\"event_type\":\"CLICK_THROUGH\",\"window_days\":7},{\"event_type\":\"VIEW_THROUGH\",\"window_days\":1}]")

ADSET_ID=$(echo $ADSET_RESPONSE | jq -r '.id')
echo "Ad Set created: $ADSET_ID"
```

**Key Parameters:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| billing_event | IMPRESSIONS | Standard for most objectives |
| optimization_goal | LEAD_GENERATION | Optimize for leads |
| destination_type | WEBSITE | Link to landing page |
| targeting_automation.advantage_audience | 1 | Enable Advantage+ |

### Step 3.5: Create Ad Creatives

**Objective:** Build the actual ad creatives with copy and media.

**For each video ad:**

```bash
# Create ad creative
CREATIVE_RESPONSE=$(curl -X POST "https://graph.facebook.com/v21.0/$AD_ACCOUNT_ID/adcreatives" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "name=Creative - Dashcam Hook" \
  -d 'object_story_spec={
    "page_id": "'$PAGE_ID'",
    "video_data": {
      "video_id": "'$VIDEO_ID'",
      "title": "Injured in an accident?",
      "message": "🚗 Injured in a car accident?\n\nYou could be entitled to compensation.\n\n✅ Free Case Review\n✅ No Win, No Fee\n✅ Get What You Deserve\n\n👇 Click below to see if you qualify 👇",
      "call_to_action": {
        "type": "LEARN_MORE",
        "value": {
          "link": "https://your-landing-page.com"
        }
      }
    }
  }')

CREATIVE_ID=$(echo $CREATIVE_RESPONSE | jq -r '.id')
echo "Creative created: $CREATIVE_ID"
```

**Copy Templates by Ad Type:**

**Template 1: Dashcam/Footage**
```
🚗 Injured in a car accident?

You could be entitled to compensation.

✅ Free Case Review
✅ No Win, No Fee  
✅ Get What You Deserve

👇 Click below to see if you qualify 👇
```

**Template 2: Settlement Reveal**
```
$[AMOUNT] Settlement 💰

This could be YOU after a car accident.

Most people don't realize how much their case is worth.

✅ Free consultation
✅ We fight for maximum compensation
✅ You pay nothing unless we win

Tap "Learn More" to see if you qualify ⬇️
```

**Template 3: UGC Testimonial**
```
"I never thought I'd get this much..." 

[Name] got $[AMOUNT] after their accident.

Were you recently injured? You might be entitled to significant compensation.

🔹 Free Case Evaluation
🔹 No Upfront Costs
🔹 Experienced Attorneys

See if you qualify 👇
```

### Step 3.6: Create Ads

**Objective:** Link creatives to ad set to create live ads.

```bash
# Create ad
AD_RESPONSE=$(curl -X POST "https://graph.facebook.com/v21.0/$AD_ACCOUNT_ID/ads" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "adset_id=$ADSET_ID" \
  -d "creative={\"creative_id\":\"$CREATIVE_ID\"}" \
  -d "name=Ad - Dashcam Hook" \
  -d "status=PAUSED")

AD_ID=$(echo $AD_RESPONSE | jq -r '.id')
echo "Ad created: $AD_ID"
```

**Repeat for each creative variation.**

**Naming Convention:**
```
Campaign: [TEST] MVA Lead Gen - Feb 2026
└── Ad Set: All Ads - Testing
    ├── Ad: Dashcam - $500K Settlement
    ├── Ad: UGC - Testimonial Sarah
    ├── Ad: Attorney - Direct Hook
    ├── Ad: Dashcam - Question Hook
    ├── Ad: Settlement Reveal - $1.2M
    └── Ad: News Style - Accident Report
```

---

## Phase 4: Pre-Launch Verification

### Step 4.1: Creative Review Checklist

**For each ad, verify:**

- [ ] Video plays correctly (no corruption)
- [ ] Audio is clear and audible
- [ ] Captions/text overlays are readable
- [ ] No spelling/grammar errors in copy
- [ ] CTA button is correct
- [ ] Landing page link works
- [ ] Landing page matches ad message
- [ ] Complies with Meta ad policies
- [ ] No prohibited claims (guaranteed results, etc.)

### Step 4.2: Targeting Review

- [ ] Geographic targeting is correct
- [ ] Age range is appropriate
- [ ] No accidental exclusions
- [ ] Advantage+ is enabled (if intended)
- [ ] Special ad category is set (if required)

### Step 4.3: Budget Review

- [ ] Daily budget is correct
- [ ] Bid strategy is appropriate
- [ ] Schedule is correct (if time-based)
- [ ] No accidental lifetime budget set

### Step 4.4: Tracking Verification

- [ ] Facebook Pixel is installed on landing page
- [ ] Conversion events are firing
- [ ] UTM parameters are set (if using)
- [ ] Lead form is connected (if using native forms)

**Test pixel firing:**
```bash
# Use Meta Pixel Helper Chrome extension
# Or check Events Manager for test events
```

---

## Phase 5: Campaign Launch

### Step 5.1: Final Status Check

```bash
# Verify campaign structure
curl -G "https://graph.facebook.com/v21.0/$CAMPAIGN_ID" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "fields=name,status,effective_status,daily_budget"

curl -G "https://graph.facebook.com/v21.0/$ADSET_ID" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "fields=name,status,effective_status,targeting"

# List all ads
curl -G "https://graph.facebook.com/v21.0/$ADSET_ID/ads" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "fields=name,status,effective_status,creative"
```

### Step 5.2: Activate Campaign

**Activation order (important):**
1. Activate ads first
2. Activate ad set
3. Activate campaign

```bash
# Activate all ads
for AD_ID in $AD_IDS; do
  curl -X POST "https://graph.facebook.com/v21.0/$AD_ID" \
    -d "access_token=$ACCESS_TOKEN" \
    -d "status=ACTIVE"
  echo "Activated ad: $AD_ID"
done

# Activate ad set
curl -X POST "https://graph.facebook.com/v21.0/$ADSET_ID" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "status=ACTIVE"

# Activate campaign
curl -X POST "https://graph.facebook.com/v21.0/$CAMPAIGN_ID" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "status=ACTIVE"
```

### Step 5.3: Launch Verification

```bash
# Confirm everything is active
curl -G "https://graph.facebook.com/v21.0/$CAMPAIGN_ID" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "fields=name,status,effective_status"
```

**Expected response:**
```json
{
  "name": "[TEST] MVA Lead Gen - Feb 2026",
  "status": "ACTIVE",
  "effective_status": "ACTIVE",
  "id": "120242084897650594"
}
```

### Step 5.4: Post-Launch Monitoring (First 24 Hours)

**Check every 4-6 hours:**

```bash
# Get campaign insights
curl -G "https://graph.facebook.com/v21.0/$CAMPAIGN_ID/insights" \
  -d "access_token=$ACCESS_TOKEN" \
  -d "fields=impressions,reach,clicks,spend,cpc,cpm,ctr,actions" \
  -d "date_preset=today"
```

**Key metrics to watch:**

| Metric | Healthy Range | Red Flag |
|--------|---------------|----------|
| CPM | $5-30 | >$50 (audience too narrow) |
| CTR | >1% | <0.5% (creative not resonating) |
| CPC | <$3 | >$5 (need creative refresh) |
| Delivery | Active | Learning Limited |

---

## Phase 6: Optimization & Scaling

### Step 6.1: Day 1-3 Analysis

**Do NOT make changes in first 24-48 hours** (learning phase)

**After 48 hours, check:**
- Which ads have >100 impressions
- CTR comparison across ads
- Any ads with 0 clicks (possible rejection)

### Step 6.2: Week 1 Optimization

**Kill underperformers:**
- Ads with CTR <0.5% after 500+ impressions
- Ads with CPL 3x higher than best performer

**Double down on winners:**
- Identify top 2-3 ads by CTR and conversion
- Create variations of winning hooks/formats
- Test new copy with winning creative

### Step 6.3: Scaling Strategy

**Vertical Scaling (increase budget):**
- Increase budget 20% every 2-3 days
- Monitor CPL — if it spikes, roll back
- Never more than 2x budget in single day

**Horizontal Scaling (new campaigns):**
- Duplicate winning ad sets to new campaign
- Test new audiences (lookalikes, interests)
- Launch new creative variations

---

## Appendix A: API Reference

### Campaign Objectives
| Objective | API Value |
|-----------|-----------|
| Leads | OUTCOME_LEADS |
| Sales | OUTCOME_SALES |
| Traffic | OUTCOME_TRAFFIC |
| Awareness | OUTCOME_AWARENESS |
| Engagement | OUTCOME_ENGAGEMENT |

### Bid Strategies
| Strategy | API Value | Use Case |
|----------|-----------|----------|
| Lowest Cost | LOWEST_COST_WITHOUT_CAP | Default, max volume |
| Cost Cap | COST_CAP | Control CPA |
| Bid Cap | LOWEST_COST_WITH_BID_CAP | Control CPM |
| ROAS Goal | LOWEST_COST_WITH_MIN_ROAS | E-commerce |

### Special Ad Categories
| Category | Value | Required For |
|----------|-------|--------------|
| Credit | CREDIT | Loans, credit cards |
| Employment | EMPLOYMENT | Job ads |
| Housing | HOUSING | Real estate |
| Social/Political | ISSUES_ELECTIONS_POLITICS | Political ads |

---

## Appendix B: Troubleshooting

### Common Errors

**Error: "Ad Not Approved"**
- Check ad copy for prohibited claims
- Verify landing page compliance
- Review special ad category requirements
- Submit appeal if false positive

**Error: "Learning Limited"**
- Budget too low for optimization goal
- Audience too narrow
- Increase budget or broaden targeting

**Error: "Payment Failed"**
- Check payment method in Business Settings
- Verify billing threshold not reached
- Contact Meta support if persistent

### API Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 100 | Invalid parameter | Check parameter format |
| 190 | Invalid access token | Refresh token |
| 200 | Permission denied | Check app permissions |
| 294 | Temporarily blocked | Wait and retry |
| 368 | Rate limited | Implement backoff |

---

## Appendix C: Automation Hooks

### For Agent Automation

**Environment Variables Required:**
```bash
META_AD_ACCOUNT_ID
META_ACCESS_TOKEN
META_PAGE_ID
META_INSTAGRAM_ACTOR_ID
LANDING_PAGE_URL
```

**Agent Decision Points:**

1. **Creative Selection**
   - Input: Competitor analysis, brand guidelines
   - Output: List of creatives to produce
   - Decision: Which formats/hooks to prioritize

2. **Targeting Configuration**
   - Input: Business type, geography, demographics
   - Output: Targeting JSON
   - Decision: Broad vs. detailed targeting

3. **Budget Allocation**
   - Input: Total budget, timeline, goals
   - Output: Daily budget, bid strategy
   - Decision: CBO vs. ABO

4. **Optimization Triggers**
   - Input: Performance metrics after 48+ hours
   - Output: Actions (pause, scale, duplicate)
   - Decision: Which ads to kill/scale

**Agent Loop:**
```
1. Research competitors (weekly)
2. Generate creative briefs (weekly)
3. Build campaigns (as needed)
4. Monitor performance (daily)
5. Optimize (every 48-72 hours)
6. Scale winners (when CPL stable)
7. Report results (weekly)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-13 | Initial creation based on MVA campaign launch |

---

*This SOP enables autonomous execution of Meta ad campaigns. For updates, contact the KuriosBrand team.*

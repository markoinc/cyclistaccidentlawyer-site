# Meta (Facebook) Marketing API — Comprehensive Practical Guide

> **For:** Marko's MVA lead gen operation ($6-7k/mo Meta ad spend)
> **Last updated:** February 2026
> **API Version:** v20.0 (latest stable)

---

## Table of Contents

1. [Authentication & Setup](#1-authentication--setup)
2. [Ads Reporting API (Insights)](#2-ads-reporting-api-insights)
3. [Campaign Management](#3-campaign-management)
4. [Lead Ads API](#4-lead-ads-api)
5. [Audiences API](#5-audiences-api)
6. [Conversions API (CAPI)](#6-conversions-api-capi)
7. [Automation Possibilities](#7-automation-possibilities)
8. [Rate Limits & Gotchas](#8-rate-limits--gotchas)
9. [Python Code Examples](#9-python-code-examples)
10. [Quick-Start Checklist](#10-quick-start-checklist)

---

## 1. Authentication & Setup

### Overview

The Meta Marketing API is built on top of the **Graph API** — a RESTful HTTP-based API. Everything is organized around:

- **Nodes** — Objects with unique IDs (Ad Account, Campaign, Ad Set, Ad)
- **Edges** — Connections between objects (`/campaigns`, `/adsets`, `/ads`, `/insights`)
- **Fields** — Properties you can read/write (`name`, `status`, `daily_budget`, `spend`)

**Base URL:** `https://graph.facebook.com/v20.0/`

### Step-by-Step Setup

#### 1.1 Create a Meta Developer Account
- Go to [developers.facebook.com](https://developers.facebook.com/)
- Log in with your Facebook account
- Click "Get Started" to set up your developer profile

#### 1.2 Create a Facebook App
1. Go to **My Apps → Create App**
2. Choose **"Business"** as the app type
3. Give it a name (e.g., "MVA Lead Gen Automation")
4. In the product list, add **Marketing API**
5. You'll receive an **App ID** and **App Secret**

#### 1.3 Verify Your Ad Account
Your ad account must:
- Be connected to a **Business Manager** (Meta Business Suite)
- Have a valid payment method
- Be in good standing (no policy violations)

#### 1.4 Configure API Permissions (OAuth Scopes)

| Permission | What It Does | Needed? |
|---|---|---|
| `ads_read` | Read ad performance data, campaign info | ✅ Yes |
| `ads_management` | Create, manage, delete campaigns (write access) | ✅ Yes |
| `leads_retrieval` | Pull lead form submissions | ✅ Yes |
| `pages_manage_ads` | Manage ads for your Facebook Pages | ✅ Yes |
| `pages_read_engagement` | Read comments on ads | Optional |
| `business_management` | Manage ad accounts/audiences on behalf of a Business | If managing multiple accounts |

**Standard Access** = works for your own ad accounts (enough for Marko)
**Advanced Access** = needed to manage other people's accounts (requires app review + business verification)

#### 1.5 Generate an Access Token

**Three token types you'll use:**

| Token Type | Lifespan | Best For |
|---|---|---|
| Short-lived User Token | ~1 hour | Quick testing in Graph Explorer |
| Long-lived User Token | Up to 60 days | Running scripts (manual renewal) |
| System User Token | Never expires (renewable) | Production automation (gold standard) |

**Quick way (for testing):**
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app
3. Choose "Get User Access Token"
4. Add permissions: `ads_management`, `ads_read`, `leads_retrieval`
5. Click "Generate Access Token"

**Extend to long-lived token:**
1. Click the blue info icon next to the token
2. Click "Open in Access Token Tool"
3. Click "Extend Access Token" → lasts ~60 days

**For production (System User — recommended):**
1. In Business Manager → Business Settings → System Users
2. Create a System User
3. Assign it to your ad account with appropriate permissions
4. Generate a token — this token won't expire as long as you maintain it

#### 1.6 Test Your Setup
```bash
# List your ad accounts
curl "https://graph.facebook.com/v20.0/me/adaccounts?access_token=YOUR_TOKEN"

# List campaigns in an account
curl "https://graph.facebook.com/v20.0/act_YOUR_ACCOUNT_ID/campaigns?fields=id,name,status&access_token=YOUR_TOKEN"
```

> ⚠️ **Security:** Treat access tokens like passwords. Never commit them to git, expose in client-side code, or share publicly. Store them in environment variables or encrypted secrets.

---

## 2. Ads Reporting API (Insights)

The **Insights API** is where you pull all performance data — spend, CPL, CPA, ROAS, impressions, clicks, etc.

### 2.1 Basic Structure

You can query insights at any level of the hierarchy:

```
GET /{object_id}/insights?fields=FIELDS&params=PARAMS
```

Where `object_id` can be:
- `act_{AD_ACCOUNT_ID}` — account level
- `{CAMPAIGN_ID}` — campaign level
- `{ADSET_ID}` — ad set level
- `{AD_ID}` — ad level

### 2.2 Key Fields for Lead Gen

These are the fields most relevant to your MVA campaigns:

| Field | Description |
|---|---|
| `spend` | Total amount spent |
| `impressions` | Number of times ads were shown |
| `reach` | Unique people who saw ads |
| `clicks` | All clicks |
| `cpc` | Cost per click |
| `cpm` | Cost per 1,000 impressions |
| `ctr` | Click-through rate |
| `actions` | All conversions (leads, purchases, etc.) — returned as an array |
| `cost_per_action_type` | CPA broken down by action type |
| `action_values` | Conversion values (for ROAS calculation) |
| `frequency` | Average times each person saw your ad |
| `quality_ranking` | Ad quality ranking |
| `engagement_rate_ranking` | Engagement rate ranking |
| `conversion_rate_ranking` | Conversion rate ranking |

**70+ fields are available** — only request what you need to minimize API load.

### 2.3 Date Ranges

**Presets:**
```
?date_preset=last_7d
```
Options: `today`, `yesterday`, `last_3d`, `last_7d`, `last_14d`, `last_28d`, `last_30d`, `last_90d`, `this_month`, `last_month`, `this_quarter`, `last_year`, `lifetime`

**Custom range:**
```
?time_range={"since":"2026-01-01","until":"2026-01-31"}
```

**Daily breakdown:**
```
?time_increment=1  (1 to 90, or "monthly")
```

### 2.4 Breakdowns

Split data by dimensions:
- `age`, `gender`, `country`, `region`, `dma`
- `placement`, `platform_position`, `device_platform`, `publisher_platform`
- `frequency_value`, `hourly_stats_aggregated_by_advertiser_time_zone`

**Example:** Get results by age and gender:
```
?breakdowns=age,gender
```

> ⚠️ **Warning:** Breakdowns multiply rows exponentially. 5 age buckets × 2 genders = 10 rows per object. Also, as of June 2025, reach broken down by age/gender is capped to the past 13 months.

### 2.5 Attribution Windows

```
?action_attribution_windows=["7d_click","1d_view"]
```

Options: `1d_click`, `7d_click`, `28d_click`, `1d_view`, `7d_view`, `28d_view`

Default is **7-day click / 1-day view**.

> As of mid-2025, Meta enforces unified attribution settings. On-Facebook conversions are counted at impression time, matching Ads Manager reporting.

### 2.6 Calculating CPL for Lead Gen

The `actions` field returns an array of objects. To get cost per lead:

```python
# From the insights response:
actions = insight['actions']
leads = next((a for a in actions if a['action_type'] == 'lead'), None)
if leads:
    lead_count = int(leads['value'])
    cpl = float(insight['spend']) / lead_count
```

### 2.7 Async Reports (for large data pulls)

For heavy queries (e.g., a year of daily data across hundreds of ads):

```
POST /act_{AD_ACCOUNT_ID}/insights
Body: { ..., "async": true }
```

Returns a `report_run_id`. Poll it until status is complete, then download.

### 2.8 Practical Example: Pull Last 30 Days Summary

```
GET /act_{ACCOUNT_ID}/insights
  ?level=campaign
  &date_preset=last_30d
  &fields=campaign_name,spend,impressions,clicks,ctr,actions,cost_per_action_type
  &access_token=TOKEN
```

---

## 3. Campaign Management

### 3.1 The Ad Object Hierarchy

```
Ad Account
  └── Campaign (objective, buying type)
       └── Ad Set (targeting, budget, schedule, placements)
            └── Ad (creative — image/video + copy)
                 └── Ad Creative (the actual content)
```

### 3.2 Create a Campaign

```
POST /act_{AD_ACCOUNT_ID}/campaigns
Body:
{
  "name": "MVA Lead Gen - Houston - Feb 2026",
  "objective": "OUTCOME_LEADS",
  "status": "PAUSED",
  "special_ad_categories": ["HOUSING"],
  "buying_type": "AUCTION"
}
```

> **Important for MVA/Legal:** You may need to use `special_ad_categories` if Meta classifies your ads under restricted categories. Legal services sometimes trigger this.

Returns: `{ "id": "CAMPAIGN_ID" }`

### 3.3 Create an Ad Set

```
POST /act_{AD_ACCOUNT_ID}/adsets
Body:
{
  "campaign_id": "CAMPAIGN_ID",
  "name": "MVA - Ages 25-65 - Texas",
  "daily_budget": 20000,  // in cents ($200/day)
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "LEAD_GENERATION",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "start_time": "2026-02-05T00:00:00-0600",
  "targeting": {
    "geo_locations": {
      "regions": [{"key": "4063"}]  // Texas
    },
    "age_min": 25,
    "age_max": 65,
    "genders": [0],  // 0=all, 1=male, 2=female
    "interests": [{"id": "6003349442621", "name": "Personal injury lawyer"}]
  },
  "promoted_object": {
    "page_id": "YOUR_PAGE_ID"
  },
  "status": "PAUSED"
}
```

> **Note:** Budget values are in **cents** (USD). So `20000` = $200.00/day.

### 3.4 Create an Ad Creative

```
POST /act_{AD_ACCOUNT_ID}/adcreatives
Body:
{
  "name": "MVA Creative - Were You Injured",
  "object_story_spec": {
    "page_id": "YOUR_PAGE_ID",
    "link_data": {
      "message": "Were you injured in a car accident? You may be entitled to compensation. Get a free case review now.",
      "link": "https://yoursite.com/free-case-review",
      "name": "Free Case Review — No Fees Unless We Win",
      "call_to_action": {
        "type": "LEARN_MORE"
      },
      "image_hash": "IMAGE_HASH_FROM_UPLOAD"
    }
  }
}
```

**Upload an image first:**
```
POST /act_{AD_ACCOUNT_ID}/adimages
Body: (multipart form data with the image file)
```
Returns: `image_hash` to reference in the creative.

### 3.5 Create the Ad

```
POST /act_{AD_ACCOUNT_ID}/ads
Body:
{
  "adset_id": "ADSET_ID",
  "name": "MVA Ad - Image A",
  "creative": {"creative_id": "CREATIVE_ID"},
  "status": "PAUSED"
}
```

### 3.6 Edit Existing Objects

```
POST /{CAMPAIGN_ID}
Body: { "name": "Updated Campaign Name", "status": "ACTIVE" }

POST /{ADSET_ID}
Body: { "daily_budget": 30000 }  // Scale to $300/day

POST /{AD_ID}
Body: { "status": "PAUSED" }  // Kill an underperformer
```

> ⚠️ Some edits (like changing targeting significantly) can **reset the learning phase**. Budget changes of <20% generally don't.

### 3.7 Delete Objects

```
DELETE /{AD_ID}
DELETE /{ADSET_ID}
DELETE /{CAMPAIGN_ID}
```

### 3.8 Common Status Values

| Status | Meaning |
|---|---|
| `ACTIVE` | Running / will run |
| `PAUSED` | Paused by you |
| `DELETED` | Soft deleted |
| `ARCHIVED` | Archived (can't be unarchived) |
| `WITH_ISSUES` | Has delivery issues |

---

## 4. Lead Ads API

This is the most relevant section for your MVA operation. Lead Ads let you collect contact info (name, phone, email) directly on Facebook without users leaving the platform.

### 4.1 Architecture

```
Ad → Lead Form (on Facebook) → Lead Submission → Your CRM/Database
```

Two ways to get leads:
1. **Bulk Read** — Poll the API periodically to fetch new leads
2. **Webhooks** — Get real-time notifications when a new lead comes in (recommended)

### 4.2 Required Permissions

- `leads_retrieval` — Required to read lead data
- `pages_manage_ads` — Required to manage lead ads
- Page Admin access on the Facebook Page associated with the lead form
- App must be in **Live mode** (not Development) to access all leads

### 4.3 Bulk Read Leads

**Read leads from a specific form:**
```
GET /{FORM_ID}/leads?access_token=PAGE_ACCESS_TOKEN
```

**Read leads from a specific ad:**
```
GET /{AD_ID}/leads?access_token=PAGE_ACCESS_TOKEN
```

**Response:**
```json
{
  "data": [
    {
      "id": "LEAD_ID",
      "created_time": "2026-02-04T10:30:00+0000",
      "field_data": [
        {"name": "full_name", "values": ["John Smith"]},
        {"name": "phone_number", "values": ["+13125551234"]},
        {"name": "email", "values": ["john@example.com"]}
      ],
      "ad_id": "AD_ID",
      "form_id": "FORM_ID"
    }
  ]
}
```

**Filter by time (to get only new leads):**
```
GET /{FORM_ID}/leads?filtering=[{"field":"time_created","operator":"GREATER_THAN","value":UNIX_TIMESTAMP}]
```

> **Leads are stored for 90 days.** After that, they're gone. Pull them regularly!

### 4.4 Webhooks for Real-Time Leads (Recommended)

This is the better approach — you get notified instantly when someone fills out your form.

**Setup Steps:**

1. **Create a webhook endpoint** on your server (a URL that accepts POST requests)

2. **Subscribe your app** to the `leadgen` field:
   ```
   POST /{PAGE_ID}/subscribed_apps
   Body: {
     "subscribed_fields": ["leadgen"],
     "access_token": "PAGE_ACCESS_TOKEN"
   }
   ```

3. **Configure the webhook** in your app's dashboard:
   - Go to App Dashboard → Webhooks
   - Choose "Page" as the object
   - Subscribe to `leadgen`
   - Enter your callback URL and verify token

4. **When a lead comes in**, Facebook sends a POST to your endpoint:
   ```json
   {
     "entry": [{
       "id": "PAGE_ID",
       "time": 1707043800,
       "changes": [{
         "field": "leadgen",
         "value": {
           "leadgen_id": "LEAD_ID",
           "form_id": "FORM_ID",
           "page_id": "PAGE_ID",
           "created_time": 1707043800,
           "ad_id": "AD_ID",
           "adgroup_id": "ADSET_ID"
         }
       }]
     }]
   }
   ```

5. **Fetch the full lead data** using the lead ID:
   ```
   GET /{LEAD_ID}?access_token=PAGE_ACCESS_TOKEN
   ```

### 4.5 Create a Lead Form via API

```
POST /{PAGE_ID}/leadgen_forms
Body:
{
  "name": "MVA Free Case Review Form",
  "questions": [
    {"type": "FULL_NAME"},
    {"type": "PHONE"},
    {"type": "EMAIL"},
    {"type": "CUSTOM", "key": "accident_date", "label": "When did the accident happen?"}
  ],
  "privacy_policy": {
    "url": "https://yoursite.com/privacy"
  },
  "follow_up_action_url": "https://yoursite.com/thank-you",
  "context_card": {
    "title": "Were You Injured in a Car Accident?",
    "content": ["Free case review", "No fees unless we win", "Available 24/7"]
  }
}
```

### 4.6 Lead Ads + Conversions API Integration

For optimizing toward **quality** leads (not just volume), you can send conversion events back via CAPI to tell Meta which leads actually converted to cases. This trains the algorithm to find more people like your best leads.

---

## 5. Audiences API

### 5.1 Custom Audiences

Custom Audiences let you target specific groups of people.

**Types relevant to your MVA operation:**

| Type | Description | Use Case |
|---|---|---|
| Customer File | Upload email/phone list | Retarget past leads, exclude existing clients |
| Website Traffic | Based on Pixel/CAPI events | Retarget site visitors |
| Lead Form | People who opened/submitted your lead form | Retarget people who opened but didn't submit |
| Engagement | People who engaged with your Page/posts | Warm audiences |
| Lookalike | Find people similar to a source audience | Scale by finding people like your best leads |

### 5.2 Create a Custom Audience (Customer File)

**Step 1: Create the audience:**
```
POST /act_{AD_ACCOUNT_ID}/customaudiences
Body:
{
  "name": "MVA Leads - Past Clients - Exclude",
  "subtype": "CUSTOM",
  "description": "Past MVA clients to exclude from targeting",
  "customer_file_source": "USER_PROVIDED_ONLY"
}
```

**Step 2: Upload users to the audience:**
```
POST /{AUDIENCE_ID}/users
Body:
{
  "payload": {
    "schema": ["EMAIL", "PHONE", "FN", "LN"],
    "data": [
      ["sha256_hashed_email", "sha256_hashed_phone", "sha256_first", "sha256_last"],
      ["sha256_hashed_email2", "sha256_hashed_phone2", "sha256_first2", "sha256_last2"]
    ]
  }
}
```

> ⚠️ **All PII must be SHA-256 hashed before uploading.** Lowercase and trim whitespace first. Meta will NOT accept unhashed data.

**Hashing example:**
```python
import hashlib
hashed = hashlib.sha256("john@example.com".strip().lower().encode()).hexdigest()
```

**Limits:**
- Max 500 Custom Audiences per ad account
- Max 10,000 users per API request (batch uploads)

### 5.3 Create a Lookalike Audience

```
POST /act_{AD_ACCOUNT_ID}/customaudiences
Body:
{
  "name": "MVA Lookalike - 1% - Texas",
  "subtype": "LOOKALIKE",
  "origin_audience_id": "SOURCE_AUDIENCE_ID",
  "lookalike_spec": {
    "type": "similarity",
    "country": "US",
    "ratio": 0.01,  // 1% lookalike (most similar)
    "location_spec": {
      "geo_locations": {
        "regions": [{"key": "4063"}]  // Texas
      }
    }
  }
}
```

**Lookalike ratios:** 0.01 (1%) to 0.10 (10%). For lead gen, 1-3% typically works best.

### 5.4 Website Custom Audience

```
POST /act_{AD_ACCOUNT_ID}/customaudiences
Body:
{
  "name": "MVA Site Visitors - Last 30 Days",
  "subtype": "WEBSITE",
  "rule": {
    "inclusions": {
      "operator": "or",
      "rules": [{
        "event_sources": [{"id": "PIXEL_ID", "type": "pixel"}],
        "retention_seconds": 2592000,  // 30 days
        "filter": {
          "operator": "and",
          "filters": [{
            "field": "url",
            "operator": "i_contains",
            "value": "/car-accident"
          }]
        }
      }]
    }
  }
}
```

### 5.5 Practical Use Cases for MVA

1. **Exclude past leads** — Upload your existing lead list, use as exclusion in targeting
2. **Lookalike from converted leads** — Upload leads that became actual clients, create 1% lookalike
3. **Retarget form openers** — Target people who opened your lead form but didn't submit
4. **Site visitor retargeting** — Target people who visited your MVA landing page but didn't fill out a form
5. **Value-based lookalike** — If some leads are worth more (e.g., serious injuries = higher case value), upload with LTV values

---

## 6. Conversions API (CAPI)

### 6.1 What Is It?

CAPI sends conversion events **from your server** directly to Meta's servers — bypassing browser limitations (ad blockers, iOS privacy, cookie restrictions).

**Why it matters for MVA lead gen:**
- Ad blockers block the Meta Pixel → you lose conversion data → Meta can't optimize
- CAPI ensures Meta sees ALL your conversions
- Better data = better optimization = lower CPL
- You can send offline events (e.g., "this lead became a signed case")

### 6.2 How It Works

```
Your Website → Form Submit → Your Server → CAPI → Meta
                                ↕
Your CRM → Lead qualifies/signs → Your Server → CAPI → Meta (offline conversion)
```

The endpoint:
```
POST /v20.0/{PIXEL_ID}/events?access_token=TOKEN
```

### 6.3 Standard Events for Lead Gen

| Event Name | When to Fire | Why |
|---|---|---|
| `PageView` | Page loads | Baseline tracking |
| `Lead` | Form submission | Core conversion event |
| `ViewContent` | Landing page view | Funnel optimization |
| `Contact` | Phone call initiated | Track calls |
| `SubmitApplication` | Extended form submission | Quality signal |
| Custom: `QualifiedLead` | Lead passes qualification | Train algo on quality |
| Custom: `SignedCase` | Lead becomes a case | Ultimate conversion |

### 6.4 Event Payload Structure

```json
{
  "data": [
    {
      "event_name": "Lead",
      "event_time": 1707043800,
      "event_source_url": "https://yoursite.com/car-accident-claim",
      "action_source": "website",
      "user_data": {
        "em": ["sha256_hashed_email"],
        "ph": ["sha256_hashed_phone"],
        "fn": ["sha256_hashed_first_name"],
        "ln": ["sha256_hashed_last_name"],
        "client_ip_address": "1.2.3.4",
        "client_user_agent": "Mozilla/5.0...",
        "fbc": "fb.1.1554763741205.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890",
        "fbp": "fb.1.1558571054389.1098115397"
      },
      "custom_data": {
        "lead_type": "mva",
        "accident_state": "TX"
      }
    }
  ]
}
```

### 6.5 Key Parameters for High Match Rate

The more user data you send, the higher Meta can match the event to the right user:

| Parameter | Description | Hashing Required? |
|---|---|---|
| `em` | Email | Yes (SHA-256) |
| `ph` | Phone | Yes (SHA-256, digits only) |
| `fn` | First name | Yes |
| `ln` | Last name | Yes |
| `client_ip_address` | User's IP | No |
| `client_user_agent` | Browser user agent | No |
| `fbc` | Facebook click ID (from `_fbc` cookie) | No |
| `fbp` | Facebook browser ID (from `_fbp` cookie) | No |
| `external_id` | Your internal lead ID | Yes |

> 🎯 **Pro tip:** The `fbc` and `fbp` cookies are the highest-quality match signals. Always pass them when available.

### 6.6 Event Deduplication

If you run both the Meta Pixel AND CAPI (recommended), you need to deduplicate:

- Include the same `event_id` in both the Pixel event and the CAPI event
- Meta will automatically deduplicate events with matching `event_id` + `event_name`

### 6.7 The Killer Feature: Offline Conversions

This is where CAPI gets really powerful for MVA:

When a lead from your Meta ad actually **signs a retainer** (becomes a case), you can fire a custom event back to Meta. This tells the algorithm: "This is what a GOOD lead looks like — find me more of these."

```python
# When a lead signs → fire this event back to Meta
event = {
    "event_name": "SignedCase",
    "event_time": int(time.time()),
    "action_source": "system_generated",
    "user_data": {
        "em": [hash_email(lead.email)],
        "ph": [hash_phone(lead.phone)],
        "external_id": [hash_value(str(lead.id))]
    },
    "custom_data": {
        "value": 5000.00,  # estimated case value
        "currency": "USD"
    }
}
```

Then optimize your campaigns for `SignedCase` instead of just `Lead`. Your CPL might go up, but your cost per SIGNED CASE goes way down.

---

## 7. Automation Possibilities

### 7.1 Ad Rules API (Automated Rules)

Meta has a native **Ad Rules API** that lets you create automated rules — the same ones available in Ads Manager, but programmatically.

**Create a rule via API:**
```
POST /act_{AD_ACCOUNT_ID}/adrules_library
Body:
{
  "name": "Pause High CPL Ad Sets",
  "evaluation_spec": {
    "evaluation_type": "SCHEDULE",
    "filters": [
      {
        "field": "entity_type",
        "value": "ADSET",
        "operator": "EQUAL"
      },
      {
        "field": "time_preset",
        "value": "LAST_3_DAYS",
        "operator": "EQUAL"
      },
      {
        "field": "impressions",
        "value": 1000,
        "operator": "GREATER_THAN"
      },
      {
        "field": "cost_per_lead",
        "value": 50,
        "operator": "GREATER_THAN"
      }
    ]
  },
  "execution_spec": {
    "execution_type": "PAUSE"
  },
  "schedule_spec": {
    "schedule_type": "CUSTOM",
    "schedule": [
      {"days": [0,1,2,3,4,5,6], "start_minute": 0, "end_minute": 1439}
    ]
  }
}
```

### 7.2 Practical Automation Rules for MVA Lead Gen

Here are the rules that matter for your operation:

#### Rule 1: Kill Underperformers
- **Trigger:** CPL > $50 AND impressions > 1,000 (over last 3 days)
- **Action:** Pause the ad set
- **Why:** Don't waste budget on ad sets that aren't converting

#### Rule 2: Scale Winners
- **Trigger:** CPL < $25 AND leads > 5 (over last 3 days)
- **Action:** Increase daily budget by 20%
- **Why:** Put more money behind what's working

#### Rule 3: Frequency Cap
- **Trigger:** Frequency > 4.0 (over last 7 days)
- **Action:** Pause the ad set
- **Why:** People are seeing your ad too many times — creative fatigue

#### Rule 4: Budget Protection
- **Trigger:** Spend > $300/day AND leads = 0 (today)
- **Action:** Pause the ad set + send notification
- **Why:** Something's broken — stop the bleeding

### 7.3 Custom Automation Scripts (Beyond Native Rules)

Native rules are limited. For more sophisticated automation, build Python scripts:

**Budget rebalancing:**
```python
# Pseudocode: Daily at 9 AM
for adset in get_active_adsets():
    insights = adset.get_insights(date_preset='last_3d')
    cpl = calculate_cpl(insights)
    
    if cpl < target_cpl * 0.7:  # 30% better than target
        scale_budget(adset, increase=0.20)  # +20%
    elif cpl > target_cpl * 1.5:  # 50% worse than target
        pause_adset(adset)
    elif cpl > target_cpl * 1.2:  # 20% worse
        reduce_budget(adset, decrease=0.15)  # -15%
```

**Creative rotation:**
```python
# Check ad fatigue weekly
for ad in get_active_ads():
    insights = ad.get_insights(date_preset='last_7d')
    if insights['frequency'] > 3.5 or ctr_declining(ad):
        pause_ad(ad)
        launch_next_creative(ad.adset_id)
```

**Lead quality feedback loop:**
```python
# Daily: sync CRM data back to Meta
for lead in get_yesterdays_qualified_leads():
    send_capi_event(
        event_name='QualifiedLead',
        user_data=lead,
        custom_data={'value': lead.estimated_value}
    )
```

### 7.4 Scheduling with Cron

Run your automation scripts on a schedule:

```bash
# Check every 4 hours for underperformers
0 */4 * * * python3 /path/to/pause_underperformers.py

# Daily budget rebalancing at 9 AM
0 9 * * * python3 /path/to/rebalance_budgets.py

# Sync qualified leads back to Meta every evening
0 20 * * * python3 /path/to/sync_qualified_leads.py
```

---

## 8. Rate Limits & Gotchas

### 8.1 Rate Limiting Structure

Meta uses a **rolling 1-hour window** with multiple layers:

#### Ad Account Level (API-Level)

| Access Tier | Max Score | Decay Time | Block Duration |
|---|---|---|---|
| Development | 60 | 300 seconds | 300 seconds |
| Standard | 9,000 | 300 seconds | 60 seconds |

#### Business Use Case Limits

| Endpoint Type | Dev Tier | Standard Tier |
|---|---|---|
| `ads_insights` | 600 + 400 × active_ads | 190,000 + 400 × active_ads |
| `custom_audience` | 5,000 + 40 × active_audiences | 190,000 + 40 × active_audiences |
| General Marketing API | ~200 calls/hour/app/account | Higher with Standard Access |

#### Insights-Specific Throttle

The `x-fb-ads-insights-throttle` response header tells you:
```json
{
  "acc_id_util_pct": 45.5,   // % of account quota used
  "app_id_util_pct": 12.3    // % of app quota used
}
```

**Lead Retrieval Rate Limit:**
```
200 × 24 × (number of leads in past 90 days) per Page per 24 hours
```

### 8.2 How to Monitor

Check these response headers after every API call:
- `x-fb-ads-insights-throttle` — Insights-specific usage
- `x-business-use-case-usage` — Business use case usage
- `x-app-usage` — App-level usage
- `x-ad-account-usage` — Account-level usage

### 8.3 Best Practices to Avoid Throttling

1. **Implement exponential backoff** — Wait 1s, then 2s, then 4s on rate limit errors
2. **Use batch requests** — Group multiple calls into one HTTP request (up to 50 per batch)
3. **Request only needed fields** — Don't pull all 70+ fields if you only need 5
4. **Use smaller date ranges** — Split large queries into monthly chunks
5. **Use async reports** for heavy data pulls
6. **Cache results** — Don't re-pull data that hasn't changed
7. **Use Page tokens** instead of User tokens for lead retrieval (better rate limits)

### 8.4 Common Error Codes

| Error Code | Meaning | Fix |
|---|---|---|
| `#4` | Application request limit reached | Wait and retry with backoff |
| `#17` | User request limit reached | Wait and retry |
| `#32` | Page request limit reached | Wait and retry |
| `#100` | Invalid parameter / Missing permission | Check params and scopes |
| `#200` | Permission denied | Check token and account access |
| `#2635` | Rate limit for ad rules | Reduce rule check frequency |
| `#190` | Invalid OAuth token | Token expired — refresh it |

### 8.5 Gotchas & Things to Watch Out For

1. **Token expiration** — Short-lived tokens expire in ~1 hour. Use System User tokens for production.

2. **Budget values are in cents** — `daily_budget: 20000` = $200, not $20,000. Double-check!

3. **Learning phase reset** — Significant changes to targeting, budget (>20%), or creative restart the learning phase (~50 conversions needed to exit).

4. **Data lag** — Insights data can be delayed up to 3 hours. Don't make real-time decisions on very recent data.

5. **API version deprecation** — Meta releases new versions quarterly. Old versions are supported for ~2 years. Always specify version in your calls (e.g., `/v20.0/`).

6. **Leads expire after 90 days** — Pull and store them in your own database immediately.

7. **Ad review** — All ads (even API-created) go through Meta's ad review. Legal/MVA content may face stricter review.

8. **Special Ad Categories** — Legal services ads may require `special_ad_categories: ["HOUSING"]` or similar. This limits targeting options (can't target by age, gender, or ZIP in some categories).

9. **Breakdown + unique metrics conflicts** — Combining certain breakdowns with unique metrics in one query will fail. Split into separate queries.

10. **Webhook verification** — Facebook periodically re-verifies your webhook endpoint. Keep it running 24/7.

---

## 9. Python Code Examples

### 9.1 Setup & Installation

```bash
pip install facebook_business requests
```

### 9.2 Initialize the SDK

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

# Load from environment variables (never hardcode!)
import os

APP_ID = os.environ['META_APP_ID']
APP_SECRET = os.environ['META_APP_SECRET']
ACCESS_TOKEN = os.environ['META_ACCESS_TOKEN']
AD_ACCOUNT_ID = os.environ['META_AD_ACCOUNT_ID']  # format: act_123456

FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)
account = AdAccount(AD_ACCOUNT_ID)
```

### 9.3 Pull Campaign Performance (Spend, CPL, Leads)

```python
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights

def get_campaign_performance(account_id, date_preset='last_30d'):
    """Pull campaign-level performance data with CPL calculation."""
    account = AdAccount(account_id)
    
    params = {
        'date_preset': date_preset,
        'level': 'campaign',
        'time_increment': 1,  # daily breakdown
    }
    
    fields = [
        'campaign_name',
        'campaign_id',
        'spend',
        'impressions',
        'clicks',
        'ctr',
        'cpc',
        'actions',
        'cost_per_action_type',
        'frequency',
    ]
    
    insights = account.get_insights(fields=fields, params=params)
    
    results = []
    for row in insights:
        # Extract lead count from actions
        leads = 0
        actions = row.get('actions', [])
        for action in actions:
            if action['action_type'] in ('lead', 'onsite_conversion.lead_grouped'):
                leads += int(action['value'])
        
        # Extract CPL from cost_per_action_type
        cpl = None
        cost_per_actions = row.get('cost_per_action_type', [])
        for cpa in cost_per_actions:
            if cpa['action_type'] in ('lead', 'onsite_conversion.lead_grouped'):
                cpl = float(cpa['value'])
        
        # Calculate CPL manually if not returned
        spend = float(row.get('spend', 0))
        if cpl is None and leads > 0:
            cpl = spend / leads
        
        results.append({
            'date': row.get('date_start'),
            'campaign_name': row.get('campaign_name'),
            'campaign_id': row.get('campaign_id'),
            'spend': spend,
            'impressions': int(row.get('impressions', 0)),
            'clicks': int(row.get('clicks', 0)),
            'ctr': float(row.get('ctr', 0)),
            'leads': leads,
            'cpl': round(cpl, 2) if cpl else None,
            'frequency': float(row.get('frequency', 0)),
        })
    
    return results

# Usage
performance = get_campaign_performance('act_YOUR_ACCOUNT_ID')
for day in performance:
    print(f"{day['date']} | {day['campaign_name']} | "
          f"Spend: ${day['spend']:.2f} | Leads: {day['leads']} | "
          f"CPL: ${day['cpl']:.2f}" if day['cpl'] else "N/A")
```

### 9.4 Create a Full Campaign (Campaign + Ad Set + Creative + Ad)

```python
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
import datetime

def create_mva_campaign(account_id, page_id, daily_budget_dollars=200):
    """Create a complete MVA lead gen campaign."""
    account = AdAccount(account_id)
    
    # 1. Create Campaign
    campaign = account.create_campaign(params={
        'name': f'MVA Lead Gen - {datetime.date.today()}',
        'objective': 'OUTCOME_LEADS',
        'status': 'PAUSED',
        'special_ad_categories': [],  # Add if needed for legal
        'buying_type': 'AUCTION',
    })
    print(f"Campaign created: {campaign['id']}")
    
    # 2. Create Ad Set
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%dT00:00:00-0600')
    
    adset = account.create_ad_set(params={
        'campaign_id': campaign['id'],
        'name': 'MVA - Texas - Ages 25-65',
        'daily_budget': daily_budget_dollars * 100,  # Convert to cents!
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'LEAD_GENERATION',
        'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
        'start_time': tomorrow,
        'targeting': {
            'geo_locations': {
                'regions': [{'key': '4063'}],  # Texas
            },
            'age_min': 25,
            'age_max': 65,
        },
        'promoted_object': {
            'page_id': page_id,
        },
        'status': 'PAUSED',
    })
    print(f"Ad Set created: {adset['id']}")
    
    # 3. Create Ad Creative (using an existing post or new creative)
    creative = account.create_ad_creative(params={
        'name': 'MVA Creative - Were You Injured',
        'object_story_spec': {
            'page_id': page_id,
            'link_data': {
                'message': ('Were you injured in a car accident in Texas? '
                           'You may be entitled to compensation. '
                           'Get your FREE case review now.'),
                'link': 'https://yoursite.com/free-case-review',
                'name': 'Free Case Review — No Fees Unless We Win',
                'call_to_action': {
                    'type': 'LEARN_MORE',
                },
            },
        },
    })
    print(f"Creative created: {creative['id']}")
    
    # 4. Create Ad
    ad = account.create_ad(params={
        'adset_id': adset['id'],
        'name': 'MVA Ad v1',
        'creative': {'creative_id': creative['id']},
        'status': 'PAUSED',
    })
    print(f"Ad created: {ad['id']}")
    
    return {
        'campaign_id': campaign['id'],
        'adset_id': adset['id'],
        'creative_id': creative['id'],
        'ad_id': ad['id'],
    }

# Usage
ids = create_mva_campaign('act_YOUR_ACCOUNT_ID', 'YOUR_PAGE_ID', daily_budget_dollars=200)
```

### 9.5 Pull Leads from Lead Forms

```python
import requests
import json

def pull_leads(form_id, page_access_token, since_timestamp=None):
    """Pull leads from a specific lead form."""
    url = f"https://graph.facebook.com/v20.0/{form_id}/leads"
    params = {
        'access_token': page_access_token,
        'limit': 500,
    }
    
    if since_timestamp:
        params['filtering'] = json.dumps([{
            'field': 'time_created',
            'operator': 'GREATER_THAN',
            'value': since_timestamp
        }])
    
    all_leads = []
    while url:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"Error: {data['error']['message']}")
            break
        
        leads = data.get('data', [])
        all_leads.extend(leads)
        
        # Pagination
        url = data.get('paging', {}).get('next')
        params = {}  # Next URL includes all params
    
    # Parse lead data
    parsed_leads = []
    for lead in all_leads:
        lead_data = {
            'id': lead['id'],
            'created_time': lead['created_time'],
            'ad_id': lead.get('ad_id'),
            'form_id': lead.get('form_id'),
        }
        for field in lead.get('field_data', []):
            lead_data[field['name']] = field['values'][0] if field['values'] else None
        parsed_leads.append(lead_data)
    
    return parsed_leads

# Usage
leads = pull_leads('FORM_ID', 'PAGE_ACCESS_TOKEN')
for lead in leads:
    print(f"{lead['created_time']} | {lead.get('full_name')} | {lead.get('phone_number')}")
```

### 9.6 Webhook Handler (Flask)

```python
from flask import Flask, request, jsonify
import requests
import hmac
import hashlib

app = Flask(__name__)

VERIFY_TOKEN = 'your_verify_token_here'
APP_SECRET = 'your_app_secret'
PAGE_ACCESS_TOKEN = 'your_page_access_token'

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Facebook webhook verification."""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return 'Forbidden', 403

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming lead notifications."""
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256', '')
    payload = request.get_data()
    expected = 'sha256=' + hmac.new(
        APP_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected):
        return 'Invalid signature', 403
    
    data = request.json
    
    for entry in data.get('entry', []):
        for change in entry.get('changes', []):
            if change['field'] == 'leadgen':
                lead_id = change['value']['leadgen_id']
                form_id = change['value']['form_id']
                ad_id = change['value'].get('ad_id')
                
                # Fetch full lead data
                lead_data = fetch_lead(lead_id)
                
                # Process the lead (send to CRM, database, etc.)
                process_lead(lead_data, ad_id)
    
    return jsonify({'status': 'ok'}), 200

def fetch_lead(lead_id):
    """Fetch full lead data from the API."""
    url = f"https://graph.facebook.com/v20.0/{lead_id}"
    params = {'access_token': PAGE_ACCESS_TOKEN}
    response = requests.get(url, params=params)
    return response.json()

def process_lead(lead_data, ad_id):
    """Process and store the lead."""
    # Parse fields
    fields = {}
    for field in lead_data.get('field_data', []):
        fields[field['name']] = field['values'][0] if field['values'] else None
    
    print(f"🚨 NEW LEAD: {fields.get('full_name')} | "
          f"Phone: {fields.get('phone_number')} | "
          f"Email: {fields.get('email')} | "
          f"Ad: {ad_id}")
    
    # TODO: Send to GHL, database, notification, etc.

if __name__ == '__main__':
    app.run(port=5000, debug=True)
```

### 9.7 Send Conversions API Event

```python
import requests
import hashlib
import time
import json

def hash_value(value):
    """SHA-256 hash a value for CAPI."""
    if not value:
        return None
    return hashlib.sha256(str(value).strip().lower().encode()).hexdigest()

def send_capi_event(pixel_id, access_token, event_name, user_data, 
                     custom_data=None, event_source_url=None):
    """Send a conversion event via CAPI."""
    url = f"https://graph.facebook.com/v20.0/{pixel_id}/events"
    
    # Build user data (hash PII)
    ud = {}
    if user_data.get('email'):
        ud['em'] = [hash_value(user_data['email'])]
    if user_data.get('phone'):
        # Remove non-digits, then hash
        phone = ''.join(filter(str.isdigit, user_data['phone']))
        ud['ph'] = [hash_value(phone)]
    if user_data.get('first_name'):
        ud['fn'] = [hash_value(user_data['first_name'])]
    if user_data.get('last_name'):
        ud['ln'] = [hash_value(user_data['last_name'])]
    if user_data.get('ip'):
        ud['client_ip_address'] = user_data['ip']  # NOT hashed
    if user_data.get('user_agent'):
        ud['client_user_agent'] = user_data['user_agent']  # NOT hashed
    if user_data.get('fbc'):
        ud['fbc'] = user_data['fbc']
    if user_data.get('fbp'):
        ud['fbp'] = user_data['fbp']
    if user_data.get('external_id'):
        ud['external_id'] = [hash_value(str(user_data['external_id']))]
    
    event = {
        'event_name': event_name,
        'event_time': int(time.time()),
        'action_source': 'website',
        'user_data': ud,
    }
    
    if event_source_url:
        event['event_source_url'] = event_source_url
    if custom_data:
        event['custom_data'] = custom_data
    
    payload = {
        'data': json.dumps([event]),
        'access_token': access_token,
    }
    
    response = requests.post(url, data=payload)
    result = response.json()
    
    if 'error' in result:
        print(f"CAPI Error: {result['error']['message']}")
    else:
        print(f"CAPI Success: {result}")
    
    return result

# Usage: When a lead submits a form
send_capi_event(
    pixel_id='YOUR_PIXEL_ID',
    access_token='YOUR_ACCESS_TOKEN',
    event_name='Lead',
    user_data={
        'email': 'john@example.com',
        'phone': '+1-312-555-1234',
        'first_name': 'John',
        'last_name': 'Smith',
        'ip': '1.2.3.4',
        'fbc': 'fb.1.1554763741205.AbCdEf...',
        'fbp': 'fb.1.1558571054389.1098115397',
    },
    event_source_url='https://yoursite.com/car-accident-claim',
    custom_data={
        'lead_type': 'mva',
        'state': 'TX',
    }
)

# Usage: When a lead qualifies / signs retainer (offline conversion)
send_capi_event(
    pixel_id='YOUR_PIXEL_ID',
    access_token='YOUR_ACCESS_TOKEN',
    event_name='SignedCase',
    user_data={
        'email': 'john@example.com',
        'phone': '+1-312-555-1234',
        'external_id': 'lead_12345',
    },
    custom_data={
        'value': 5000.00,
        'currency': 'USD',
    }
)
```

### 9.8 Pause Underperforming Ad Sets (Automation Script)

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
import os

# Config
MAX_CPL = 50.00  # Kill ad sets with CPL above this
MIN_IMPRESSIONS = 1000  # Only evaluate ad sets with enough data
LOOKBACK = 'last_3d'

FacebookAdsApi.init(
    os.environ['META_APP_ID'],
    os.environ['META_APP_SECRET'],
    os.environ['META_ACCESS_TOKEN']
)

account = AdAccount(os.environ['META_AD_ACCOUNT_ID'])

# Get active ad sets with insights
adsets = account.get_ad_sets(
    fields=['id', 'name', 'status', 'daily_budget'],
    params={'filtering': [{'field': 'effective_status', 'operator': 'IN', 'value': ['ACTIVE']}]}
)

paused = []
for adset in adsets:
    insights = AdSet(adset['id']).get_insights(
        fields=['spend', 'impressions', 'actions', 'cost_per_action_type'],
        params={'date_preset': LOOKBACK}
    )
    
    if not insights:
        continue
    
    row = insights[0]
    impressions = int(row.get('impressions', 0))
    spend = float(row.get('spend', 0))
    
    if impressions < MIN_IMPRESSIONS:
        continue  # Not enough data yet
    
    # Calculate CPL
    leads = 0
    for action in row.get('actions', []):
        if action['action_type'] in ('lead', 'onsite_conversion.lead_grouped'):
            leads += int(action['value'])
    
    if leads == 0 and spend > 100:
        # Spent $100+ with zero leads — pause it
        AdSet(adset['id']).api_update(params={'status': 'PAUSED'})
        paused.append(f"{adset['name']} — ${spend:.2f} spent, 0 leads")
        continue
    
    if leads > 0:
        cpl = spend / leads
        if cpl > MAX_CPL:
            AdSet(adset['id']).api_update(params={'status': 'PAUSED'})
            paused.append(f"{adset['name']} — CPL: ${cpl:.2f}")

# Report
if paused:
    print(f"⚠️ Paused {len(paused)} ad sets:")
    for p in paused:
        print(f"  → {p}")
else:
    print("✅ All ad sets performing within thresholds")
```

### 9.9 Upload Custom Audience

```python
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience
import hashlib

def create_and_populate_audience(account_id, name, emails, phones=None):
    """Create a custom audience and upload hashed user data."""
    account = AdAccount(account_id)
    
    # Create the audience
    audience = account.create_custom_audience(params={
        'name': name,
        'subtype': 'CUSTOM',
        'description': f'{name} - uploaded via API',
        'customer_file_source': 'USER_PROVIDED_ONLY',
    })
    audience_id = audience['id']
    print(f"Audience created: {audience_id}")
    
    # Prepare hashed data
    def sha256(value):
        return hashlib.sha256(str(value).strip().lower().encode()).hexdigest()
    
    schema = ['EMAIL']
    data = [[sha256(email)] for email in emails]
    
    if phones:
        schema = ['EMAIL', 'PHONE']
        data = [
            [sha256(email), sha256(''.join(filter(str.isdigit, phone)))]
            for email, phone in zip(emails, phones)
        ]
    
    # Upload in batches of 10,000
    BATCH_SIZE = 10000
    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i:i + BATCH_SIZE]
        CustomAudience(audience_id).add_users(params={
            'payload': {
                'schema': schema,
                'data': batch,
            },
        })
        print(f"Uploaded batch {i // BATCH_SIZE + 1} ({len(batch)} users)")
    
    return audience_id

# Usage: Upload past leads to exclude
emails = ['john@example.com', 'jane@example.com']  # From your CRM
phones = ['+13125551234', '+17135559876']
audience_id = create_and_populate_audience(
    'act_YOUR_ACCOUNT_ID',
    'MVA Past Leads - Exclude',
    emails, phones
)
```

### 9.10 Daily Report Script

```python
"""
Daily MVA Campaign Report
Run via cron: 0 8 * * * python3 /path/to/daily_report.py
"""
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
from datetime import datetime

FacebookAdsApi.init(
    os.environ['META_APP_ID'],
    os.environ['META_APP_SECRET'],
    os.environ['META_ACCESS_TOKEN']
)

account = AdAccount(os.environ['META_AD_ACCOUNT_ID'])

# Yesterday's data
insights = account.get_insights(
    fields=[
        'campaign_name', 'spend', 'impressions', 'clicks',
        'ctr', 'actions', 'cost_per_action_type',
    ],
    params={
        'date_preset': 'yesterday',
        'level': 'campaign',
        'filtering': [{'field': 'spend', 'operator': 'GREATER_THAN', 'value': '0'}],
    }
)

report_lines = [f"📊 MVA Daily Report — {datetime.now().strftime('%Y-%m-%d')}"]
report_lines.append("=" * 50)

total_spend = 0
total_leads = 0

for row in insights:
    spend = float(row.get('spend', 0))
    total_spend += spend
    
    leads = 0
    for action in row.get('actions', []):
        if action['action_type'] in ('lead', 'onsite_conversion.lead_grouped'):
            leads += int(action['value'])
    total_leads += leads
    
    cpl = spend / leads if leads > 0 else float('inf')
    
    report_lines.append(f"\n🎯 {row.get('campaign_name')}")
    report_lines.append(f"   Spend: ${spend:.2f}")
    report_lines.append(f"   Leads: {leads}")
    report_lines.append(f"   CPL: ${cpl:.2f}" if leads > 0 else "   CPL: N/A")
    report_lines.append(f"   Impressions: {row.get('impressions', 0)}")
    report_lines.append(f"   CTR: {row.get('ctr', 0)}%")

total_cpl = total_spend / total_leads if total_leads > 0 else 0
report_lines.append(f"\n{'=' * 50}")
report_lines.append(f"💰 TOTAL: ${total_spend:.2f} | {total_leads} leads | CPL: ${total_cpl:.2f}")

report = '\n'.join(report_lines)
print(report)

# TODO: Send via Slack, email, or SMS
```

---

## 10. Quick-Start Checklist

### Week 1: Foundation
- [ ] Create Meta Developer account
- [ ] Create Facebook App with Marketing API
- [ ] Generate System User token (or long-lived token to start)
- [ ] Install `facebook_business` Python SDK
- [ ] Make first API call: list campaigns
- [ ] Pull last 30 days of insights data
- [ ] Store credentials securely in environment variables

### Week 2: Reporting
- [ ] Build daily report script (Section 9.10)
- [ ] Set up cron job to run daily at 8 AM
- [ ] Test pulling lead form data (Section 9.5)
- [ ] Verify lead data matches Ads Manager numbers

### Week 3: Lead Automation
- [ ] Set up webhook endpoint for real-time leads (Section 9.6)
- [ ] Subscribe your app to `leadgen` webhooks
- [ ] Connect webhook to your CRM/GHL
- [ ] Test with a real lead submission

### Week 4: Optimization
- [ ] Set up CAPI for form submissions (Section 9.7)
- [ ] Create automation rules for pausing underperformers (Section 9.8)
- [ ] Upload custom audience of past leads for exclusion (Section 9.9)
- [ ] Create lookalike audience from best leads
- [ ] Set up the offline conversion loop (Section 6.7)

### Ongoing
- [ ] Send qualified lead / signed case events back via CAPI
- [ ] Review and refine automation thresholds
- [ ] Monitor rate limits and API health
- [ ] Update API version when Meta releases new versions

---

## Appendix A: Useful API Endpoints Reference

| Task | Method | Endpoint |
|---|---|---|
| List campaigns | GET | `/act_{ID}/campaigns` |
| List ad sets | GET | `/act_{ID}/adsets` |
| List ads | GET | `/act_{ID}/ads` |
| Get insights | GET | `/act_{ID}/insights` or `/{OBJECT_ID}/insights` |
| Create campaign | POST | `/act_{ID}/campaigns` |
| Create ad set | POST | `/act_{ID}/adsets` |
| Create ad | POST | `/act_{ID}/ads` |
| Create creative | POST | `/act_{ID}/adcreatives` |
| Upload image | POST | `/act_{ID}/adimages` |
| Get leads | GET | `/{FORM_ID}/leads` |
| Create custom audience | POST | `/act_{ID}/customaudiences` |
| Add users to audience | POST | `/{AUDIENCE_ID}/users` |
| Send CAPI event | POST | `/{PIXEL_ID}/events` |
| Create ad rule | POST | `/act_{ID}/adrules_library` |
| Update any object | POST | `/{OBJECT_ID}` |
| Delete any object | DELETE | `/{OBJECT_ID}` |

## Appendix B: Resources

- [Official Marketing API Docs](https://developers.facebook.com/docs/marketing-apis)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Python Business SDK (GitHub)](https://github.com/facebook/facebook-python-business-sdk)
- [CAPI Payload Helper](https://developers.facebook.com/docs/marketing-api/conversions-api/payload-helper)
- [API Changelog](https://developers.facebook.com/docs/graph-api/changelog)
- [Insights API Parameters (full list)](https://developers.facebook.com/docs/marketing-api/insights/parameters)
- [Ad Rules Reference](https://developers.facebook.com/docs/marketing-api/reference/ad-rule/)

---

*Guide compiled from official Meta developer documentation, API reference, and community resources. All code examples use the `facebook-business` Python SDK v20.0+.*

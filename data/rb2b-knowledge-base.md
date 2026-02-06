# RB2B Complete Knowledge Base
> Comprehensive documentation from https://support.rb2b.com/en/ — 250+ articles
> Last updated: February 2026

---

## Table of Contents
1. [What is RB2B](#what-is-rb2b)
2. [How It Works](#how-it-works)
3. [Data & Fields Available](#data--fields-available)
4. [Pricing Plans & Credits](#pricing-plans--credits)
5. [Script Installation & Configuration](#script-installation--configuration)
6. [Features](#features)
7. [Integrations](#integrations)
8. [Best Practices](#best-practices)
9. [Security & Compliance](#security--compliance)
10. [Troubleshooting](#troubleshooting)
11. [Partner Programs & API](#partner-programs--api)
12. [Service Updates](#service-updates)

---

## What is RB2B

RB2B is a **B2B website visitor identification platform** built by Retention.com. It identifies anonymous website visitors at the **person-level and company-level**, even when they haven't filled out forms. It uses proprietary identification algorithms and privacy-compliant data enrichment methods.

### Key Capabilities
- Identifies **20-30% of qualified US-based traffic** at individual level (Pro plan)
- **40-45% contact-level identification rate** for unique US visitors (Pro users average)
- Combined person + company identification: **70-80% of US traffic** (Pro+ plan)
- Company-level identification works **globally** (including EU)
- Person-level identification is **US-only**
- Uses both first-party and third-party cookies, device identifiers, and IP data
- Enriches profiles using LinkedIn and verified professional databases

### Identity Graph
- **85% of lookups** powered by RB2B's own proprietary identity graph (built since late 2023)
- Only **~15% relies on external data vendors** (for edge cases)
- This proprietary data is **exclusive to RB2B** — unavailable to competitors
- Part of broader Retention.com ecosystem

---

## How It Works

### 4-Step Process

**Step 1: Activation & Initial Screening**
- Script activates when visitor lands on website
- If using CookieYes, script runs only after cookie acceptance (automatic)
- Other consent tools require manual configuration to delay script
- **Geofence verification**: Checks if visitor is in the US via IP geolocation
- Non-US visitors may get company-level ID only (never PII)
- Evaluates visitor quality before proceeding

**Step 2: Information Correlation**
- Correlates multiple non-sensitive data points: first/third-party cookies, device IDs, IP data
- All privacy-compliant and consent-based
- For non-CookieYes consent tools, you must manually delay RB2B script until consent

**Step 3: Professional Profiling**
- When identified, RB2B enriches with LinkedIn and professional databases
- Appends: name, title, company, email, industry, etc.
- Identifies ~20-30% of qualified US traffic at individual level
- Built-in **email validation** (launched April 2025) — validates all emails before surfacing

**Step 4: Value Assessment & Transmission**
- Validates completeness, consistency, confidence level
- Discards incomplete/low-quality matches
- Sends validated profiles to dashboard and integrations in real-time

### The Script
- **Asynchronous** — doesn't block page load or slow down website
- Served over HTTPS from Amazon CloudFront CDN
- Should be placed in `<head>` tag for best performance
- Install on **ALL pages** — users with site-wide install collect ~1863% more profiles
- Script begins working **immediately** upon installation

---

## Data & Fields Available

### Contact-Level Profile Information (Paid Plans)
| Field | Description |
|-------|-------------|
| LinkedInUrl | Visitor's LinkedIn profile URL |
| FirstName | First name |
| LastName | Last name |
| Title | Job title |
| WorkEmail | Business email (**Pro/Pro+ only**) |
| CompanyName | Company name |
| Website | Company website URL |
| Industry | Company industry |
| EstimatedEmployeeCount | Company employee count |
| EstimateRevenue | Company estimated revenue |
| City | City at time of identification |
| State | State at time of identification |
| Zipcode | Zipcode at time of identification |
| TwitterUrl | Twitter/X profile URL |
| FacebookUrl | Facebook profile URL |

### Behavioral/Visit Data
| Field | Description |
|-------|-------------|
| AllTimePageViews | Total page views since first identification |
| LastSeenAt | Last visit timestamp |
| FirstSeenAt | First identification timestamp |
| NewProfile | True/False if new during CSV timeframe |
| MostRecentReferrer | Referring URL of most recent visit |
| RecentPageCount | Page views during CSV timeframe |
| RecentPageUrls | Pages visited during CSV timeframe |
| Tags | Hot Lead, Hot Page, or null |
| FilterMatches | Hot Leads tag names matched |
| ProfileType | "Person" or "Company" |

### Company-Level Only (Free Plan)
- Company Name
- Repeat Visitor Tracking
- Basic visit data

### What's NOT Available by Plan
| Data | Free | Starter | Pro | Pro+ |
|------|------|---------|-----|------|
| LinkedIn Profile | ❌ | ✅ | ✅ | ✅ |
| Full Name | ❌ | ✅ | ✅ | ✅ |
| Job Title | ❌ | ✅ | ✅ | ✅ |
| Business Email | ❌ | ❌ | ✅ | ✅ |
| Pageview History | ❌ | ✅ | ✅ | ✅ |
| Company Name | ✅ | ✅ | ✅ | ✅ |
| Industry | ❌ | ✅ | ✅ | ✅ |

### UTM Parameters
- NOT shown in dashboard or standard CSV exports
- Passed through to **HubSpot CRM** and **Salesforce CRM** integrations
- utm_source, utm_medium, utm_campaign available when present

### Email Validation (Launched April 2025)
- Built-in, automatic — no setup required
- Validates all newly resolved emails before surfacing
- Invalid/outdated emails excluded from profiles
- Validation tags shown next to emails in dashboard

---

## Pricing Plans & Credits

### Plan Comparison (as of January 2026)

| Plan | Monthly Cost | Credits/Month | Contact-Level ID | Company-Level ID | Coverage |
|------|-------------|---------------|-------------------|-------------------|----------|
| **Free** | $0 | 150 | ❌ | ✅ (Global) | 15-20% |
| **Starter** | $79 | 300 | ✅ (US) | ✅ (Global) | 30-40% |
| **Pro** | From $149 | From 600 | ✅ (US) | ✅ (Global) | 30-40% |
| **Pro+** | From $199 | From 600 | ✅ (US) | ✅ (Global) | 70-80% |

### Pro & Pro+ Pricing Tiers

| Credits | Pro | Pro+ |
|---------|-----|------|
| 600 | $149 | $199 |
| 1,250 | $249 | $299 |
| 2,500 | $349 | $399 |
| 5,000 | $499 | — |
| 7,500 | $648 | — |
| 10,000 | $799 | — |
| 12,500 | $849 | — |
| 20,000 | $949 | — |
| 25,000 | $1,149 | — |
| 50,000 | $1,699 | — |
| 75,000 | $2,399 | — |
| 125,000 | $3,699 | — |
| 250,000 | $7,199 | — |
| 500,000 | $10,499 | — |
| 1,250,000 | $25,000 | — |
| 2,500,000 | $50,000 | — |

### Pro vs Pro+
- **Pro**: Uses RB2B's internal identification graph only
- **Pro+**: Adds "Premium Resolution" — waterfall of additional external identity graphs for maximum coverage
- Pro+ has significantly higher overall identification/match rates

### Credit System
- **1 credit = 1 unique visitor identified** in a 30-day period
- Same visitor revisiting = no additional credit in same billing cycle
- Max 12 credits per visitor per year
- Credits **do not roll over** — expire at end of billing cycle
- **Every identified visitor** consumes a credit (since Jan 2026 billing update — both person and company level)
- Credits doubled across all paid plans to compensate for this change

### Overages (Pro plans, monthly subscriptions only)
- Can set overage threshold in account settings
- **<1000 credits plan**: $0.85/credit overage
- **≥1000 credits plan**: $0.45/credit overage
- Billed at end of billing cycle, added to next month
- Can disable overages; script stops when credits exhausted
- Free and annual plans cannot enable overages

### Billing Changes (January 2026)
- **Month-to-month only** — no new annual plans available
- Existing annual subscribers can keep their plan unless they change
- Every identified visitor now consumes a credit (person or company)
- Credit limits doubled to compensate
- New Starter plan ($79/mo, 300 credits) introduced
- Free plan limited to company-level only (no person-level data)

### Multiple Domains
- Up to 5 additional domains per account
- **$99/month per additional domain**
- All data consolidated into single account
- Unused domain seats removed at billing cycle renewal
- Pro/Pro+ plans only

---

## Script Installation & Configuration

### Installation Methods
- **Direct**: Add script to `<head>` tag of every page
- **Google Tag Manager**: Via custom HTML tag
- **WordPress**: Plugin available or manual header insertion
- **Webflow, Wix, Framer, Squarespace**: Platform-specific guides available
- **React, Next.js, Angular**: Ensure script fires on every page view
- **Programming Languages**: PHP, Python, Ruby, Node.js, Java guides available

### Key Installation Rules
1. Place in `<head>` tag (not `<body>`) for optimal performance
2. Install on **ALL public-facing pages** (site-wide)
3. Must authorize domain in RB2B dashboard before script works
4. Script self-verifies on first data transmission
5. Cannot work in iframes (e.g., GoDaddy Website Builder)

### Configuration Options (Pro/Pro+)

**URL Restrictions**
- Exclude specific pages: "trigger on all pages except..."
- Include only specific pages: "only trigger on URLs listed below"
- Uses URL stubs (e.g., /pricing, /careers)
- Max 80 characters per entry
- Applies uniformly across all domains/subdomains

**Domain Exclusion List**
- Prevent identification of visitors from specific email domains
- Use to exclude: employees, existing customers, partners, internal traffic
- Excludes based on email domain match, not specific email addresses

**Repeat Visitor Collection**
- Toggle on/off in Script settings
- On by default — disable to save credits
- When off, repeat visitors not identified or counted

### Cookies Set by RB2B
| Cookie | Expiration | Purpose |
|--------|-----------|---------|
| _reb2bgeo | 20 days | Geolocation for identification |
| _reb2bloaded | 1 second | Prevents duplicate script execution |
| _reb2bref | 15 days | Stores referring URL |
| _reb2sessionID | 30 minutes | Temporary session identifier |
| _reb2buid | 360 days | Persistent unique ID for person-level identification |
| _reb2bfxf | 1 month | Internal tracking |
| _reb2btd | 1 month | Identity resolution data |
| _reb2bli | 1 month | Links browser session to ID records |
| _reb2bresolve | 2 days | Temp storage during identity resolution |
| _reb2butk | 1 year | Long-term unique token for persistent identification |

---

## Features

### Hot Leads Tagging (Pro/Pro+)
Tag visitors matching your ICP automatically. **6 tagging categories**:
1. **Company Revenue**: Below $500k to Above $50m
2. **Company Size**: 1-10 to Above 5000 employees
3. **Seniority**: Owner, Founder, C Suite, VP, Director, Manager, etc.
4. **Department**: Consulting, Engineering, Finance, Marketing, Sales, etc.
5. **Industry**: 20+ categories with sub-categories
6. **States**: All US states

- Uses **OR logic** between categories
- Set required number of matches (default: 1)
- Apply tags to integrations to send only Hot Leads
- Tags can be applied manually to individual profiles
- New tags do NOT apply retroactively
- Cannot limit credit usage to ICP-only profiles

### Hot Pages (Pro/Pro+)
- Tag visitors who visit specific important pages
- Enter URL or keyword within URL
- Supports subdomains
- Visitors tagged automatically
- Tag persists regardless of plan changes

### CSV Exports (Pro/Pro+)
- Download from dashboard: https://app.rb2b.com/profiles/exports
- Date ranges: Today, Past 3 Days, Past 7 Days, Past 30 Days
- **Max export range: 30 days** (no workaround)
- Can filter profiles before exporting
- Exports generated in background; link sent via email
- **No API for CSV download** — no API on roadmap
- Cannot auto-send CSVs to external databases

### Email Validation
- Automatic for all users since April 2025
- Validates all newly resolved emails in real-time
- Invalid emails excluded from profiles
- Validation type tags shown in dashboard

### Multiple Domains
- Up to 5 additional domains per account
- $99/month each
- Consolidated data across all domains
- Pro/Pro+ plans only

---

## Integrations

### How Integrations Work
- Data sent in **real-time** when visitor identified
- One active connection per integration per account
- Can connect to multiple different platforms simultaneously
- Most integrations only receive new visitor data (not repeat visits)
- **HubSpot CRM** and **Salesforce CRM** continue receiving page view updates
- Repeat visit data available in dashboard and CSV exports always

### Integration Availability by Plan
| Integration | Free | Starter | Pro | Pro+ |
|-------------|------|---------|-----|------|
| Slack | ✅ | ✅ | ✅ | ✅ |
| Microsoft Teams | ✅ | ✅ | ✅ | ✅ |
| CSV Export | ❌ | ❌ | ✅ | ✅ |
| HubSpot CRM | ❌ | ❌ | ✅ | ✅ |
| Salesforce CRM | ❌ | ❌ | ✅ | ✅ |
| Clay | ❌ | ❌ | ✅ | ✅ |
| Webhook | ❌ | ❌ | ✅ | ✅ |
| n8n | ❌ | ❌ | ✅ | ✅ |
| Zapier | ❌ | ❌ | ✅ | ✅ |
| All others | ❌ | ❌ | ✅ | ✅ |

### Key Integrations

#### Slack
- Real-time visitor notifications to chosen channel
- Daily recap messages (can toggle on/off)
- "Push to Apollo" button on profiles (if Apollo connected)
- Available on all plans
- Can manage multiple RB2B Slack integrations with single Slack user
- Can enable both personal and company-level profiles

#### HubSpot CRM
- Creates/updates contacts and companies
- Custom RB2B properties in HubSpot
- Timeline events for visit activity
- Continues sending page view updates for repeat visitors
- UTM data mapped to contact records
- Can customize settings and field mapping
- Workflows can trigger based on RB2B properties

#### Salesforce CRM
- Creates/updates Contacts and Accounts
- Logs webpage activity as Tasks
- Requires specific object permissions (Contact, Account, Task)
- Custom RB2B fields created
- Continues sending repeat visitor data
- UTM data passed to records
- Can add "RB2B" to Lead Source/Account Source picklists

#### Clay
- Webhook-based integration
- Send data to Clay tables for enrichment, scoring, routing
- Configure required fields
- Toggle repeat visitor data on/off
- Use Clay for: enrichment + CRM sync, intent alerts, lead routing, re-engagement tracking

#### Webhook (Generic)
- Single webhook URL per account
- Simple POST requests — no custom headers or payload needed
- Required fields must have values for payload to send
- Auto-disables on repeated failures (schema mismatches, timeouts)
- Must re-enable manually after fixing issues

#### n8n
- Webhook-based integration
- Use for: lead scoring, return visitor detection, account-level tracking
- Example workflows available for: page view tracking, multi-person company detection, returning visitor alerts
- Build lead scores using available fields

#### Zapier
- Connects RB2B to 8,000+ apps
- Uses API keys (generated in RB2B)
- Trigger events available for new visitor identification
- Bridge to any platform without native integration

#### Apollo.io
- API key integration (must be master key)
- Manual pushes (via Slack "Push to Apollo" button)
- Automatic pushes (toggle Auto Sync)
- Hot Leads sent even if some contact info missing
- Choose sequences for auto-enrollment

#### Make.com
- Webhook-based integration
- Install RB2B's Make.com app first
- Generate webhook URL in Make.com Scenario
- Similar settings to other webhook integrations

#### Microsoft Teams
- Real-time visitor notifications (like Slack)
- Available on all plans
- Added January 2026

#### Other Native Integrations
- BetterContact, Growth-X, HeyReach, Highperformr, HireQuotient
- Instantly, La Growth Machine, Mixmax, Outplay, Pocus
- Reply.io, Salesforge, Samplead, Sendspark, Smartlead
- SmartReach, SuperAGI, Tapistro, Warmly

### LinkedIn Automation
RB2B doesn't have built-in LinkedIn automation but integrates with:
- HeyReach, Growth-X, Reply.io, Samplead
- La Growth Machine, SuperAGI, Highperformr

**Best practices for LinkedIn outreach:**
- Don't mention "visited your website" — use broader relevance
- Keep messages conversational, not robotic
- Space messages over 7-10 days
- Prioritize Hot Leads first
- Combine data signals (ICP match + return visits + high-intent pages)

### Repeat Visitor Data in Integrations
- **Always on**: HubSpot CRM, Salesforce CRM
- **On by default (can disable)**: Slack, Microsoft Teams
- **Optional toggle**: Clay, Webhook, n8n, Make.com, Zapier, and most others

---

## Best Practices

### Improving Collection Rates
1. Configure domain properly (resolve with/without www)
2. Install script on ALL public pages (not just homepage)
3. Increase US-based traffic (strongest identification coverage)
4. Verify script regularly (especially after CMS updates)
5. Don't tie script to cookie acceptance unnecessarily (US law allows opt-out model)

### Filtering for Relevant Leads
1. **Hot Leads**: Define ICP criteria, send only Hot Leads to integrations
2. **URL Restrictions**: Exclude low-intent pages (careers, support, etc.)
3. **Domain Exclusion**: Filter out employees, existing customers, internal traffic

### Optimizing Credit Consumption
- Use URL Restrictions to track only high-intent pages
- Use Domain Exclusion to exclude known low-intent domains
- Toggle off repeat visitor collection if credit-conscious
- Start with broader criteria, then tighten over time
- Monitor credit usage regularly

### Knowing When to Reach Out
**Strong signals:**
- High-intent page views (pricing, demo, product pages)
- Return visits across multiple days
- ICP match + Hot Leads tag
- Multiple visitors from same company

### How to Reach Out
- Act within hours, not days
- Personalize with: role/title, company name, pages visited
- Choose channel based on signal strength (LinkedIn, email, phone)
- Keep it conversational, not transactional
- Coordinate across sales and marketing teams

### Outreach Templates
**LinkedIn Connection Request:**
> "Hi [First Name], I noticed we work in similar spaces around [topic/problem area]. Would love to connect."

**Follow-up (2-3 days later):**
> "Thanks for connecting! Many [industry] teams I talk to are focused on [goal/problem]. We've been helping a few achieve [specific result]. Would it make sense to share a quick example?"

### Ad Retargeting with RB2B
- Not a replacement for ad platforms/pixels
- Use as signal amplifier for high-intent traffic
- Segment visitors before retargeting (ICP fit, page depth, frequency)
- Send data to CRM → CRM-based retargeting
- Great for account-based marketing (ABM)
- LinkedIn best channel for B2B retargeting

### Using Clay with RB2B
- Send only Hot Leads to Clay
- Use Clay to enrich + score leads
- Route leads automatically: RB2B → Clay → CRM/Outreach
- Track return visits via Clay tables
- Combine with Slack for instant Hot Lead alerts

### Using n8n with RB2B
- Build lead scoring using: Tags, Captured URL, Title, Industry
- Detect returning visitors by logging timestamps
- Group visitors by company domain for account-level signals
- Route to CRM/sequencer based on score
- Build weekly reporting with Google Sheets/Airtable

---

## Security & Compliance

### Encryption
- **At rest**: AES-256 database encryption
- **In transit**: TLS 1.3 for all data
- **API/Auth**: SSL/TLS encrypted
- **Website**: HTTPS only
- **Data integrity**: SHA-256 with RSA signature
- **Queue messages**: Encrypted SQS

### Certifications
- **SOC 2 Type 2 compliant** (RB2B and parent Retention.com)
- Trust portal: https://retention.securitypal.com/
- Script served via Amazon CloudFront CDN (HTTPS, TLS, DDoS protection)

### Data Broker Registration
- Registered in **California, Texas, Vermont, and Oregon**
- Complies with state data broker laws

### GDPR Compliance
- Person-level identification is **US-only** (never for EU visitors)
- Company-level identification works globally (including EU)
- Session cookies set before consent don't store PII
- Geo-IP service only returns true/false location (no IP sharing)
- Users responsible for their own consent management and compliance
- Can disable international tracking for company-level visitors
- Opt-out link: https://app.retention.com/optout
- GDPR opt-out: https://www.rb2b.com/rb2b-gdpr-opt-out

### Cookie Consent / Privacy Policy
- **Must update privacy policy** to reflect RB2B usage
- **Must update cookie banner** to list RB2B cookies
- CookieYes integration is automatic — others require manual setup
- Under CCPA: can choose notification-only (with opt-out) or consent-based model
- Opt-out link can be in Privacy Policy rather than cookie banner (US law)
- RB2B does NOT monitor or verify user compliance — responsibility is on user

### Standard Privacy Policy Language
> "When you visit or log in to our website, cookies and similar technologies may be used by our online data partners or vendors to associate these activities with other personal information they or others have about you, including by association with your email. We (or service providers on our behalf) may then send communications and marketing to these email. You may opt out of receiving this advertising by visiting https://app.retention.com/optout."

---

## Troubleshooting

### No Collection / Script Not Working
1. **Trial ended** without selecting a plan → account suspended
2. **Monthly cap reached** → collection paused until next cycle
3. **Payment failed** → check credit card
4. **Script removed** during website update → reinstall
5. **WP Rocket "Delay JavaScript Execution"** breaks RB2B → exclude RB2B from delay
6. **Server-side caching** serving old pages → clear cache after install
7. **Content Security Policy** blocking script → whitelist RB2B domains

### Low Profile Volume
1. Repeat Visitor Collection disabled → re-enable
2. URL Restrictions too narrow → broaden
3. Low US traffic → adjust targeting
4. Domain Exclusion List too broad → review
5. Script tied to cookie acceptance → consider opt-out model
6. WordPress plugin interference → exclude RB2B from optimization

### Login Issues
- **403 error**: Disconnect VPN/proxy, wait 10 minutes
- **Password prompt**: You're on wrong dashboard (use https://app.rb2b.com/login — magic link, no password)

### CSV Export Issues
- Max range: 30 days
- If CSV looks like gibberish: right-click → Save As (don't open in browser)
- Cannot export all-time data
- No API for exports

### Script Verification
- Built-in test tool on Script page
- Not mandatory — script self-verifies on first data transmission
- Common issues: caching, CSP blocking, cookie banner blocking

---

## Partner Programs & API

### API Partner Program
- Access to RB2B's **Identity APIs**
- Sign up: https://ui.api.rb2b.com/signup
- **Identification Endpoints**: Convert IP + user agent → business data
- **Enrichment Endpoints**: Enrich hashed emails (HEM) with professional data
- For: SaaS developers, GTM engineers, enterprise retailers, adtech pros

### OEM Partner Program
- Embed RB2B visitor identification into your own platform
- White-label solutions available
- Different billing: "cost per resolution" (not standard credits)
- OEM script and consumer RB2B script **cannot run on same page**
- Consumer account deactivated when joining OEM program
- Can maintain separate accounts for both

### Agency Program
- Manage multiple client accounts
- Tailored discounts available
- Separate access and reporting per client

---

## Service Updates

### Key Recent Changes (2025-2026)
- **Jan 2026**: New billing model — all visitors consume credits, credits doubled. New Starter plan ($79). Free plan limited to company-level. Pro+ launched with Premium Resolution. Month-to-month billing only.
- **Jan 2026**: Microsoft Teams integration launched
- **Jan 2026**: OEM Program launched
- **Dec 2025**: Make.com and Outplay integrations
- **Nov 2025**: Updated Terms & Conditions
- **Oct 2025**: Account deletion feature, webhook updates
- **Aug 2025**: Multiple Domains feature, Sendspark integration
- **Jul 2025**: n8n integration, Warmly integration, manual Hot Leads tagging
- **Jun 2025**: Domain Exclusion List, CSV export updates
- **May 2025**: Email Validation tags, URL Restrictions update
- **Apr 2025**: Email Validation launched, company-level ID rollout
- **Mar 2025**: Salesforge and Highperformr integrations
- **Nov 2024**: SOC 2 Type II certification
- **Sep 2024**: SOC 2 Type I, data broker registration (Oregon)
- **Aug 2024**: Data broker registration (CA, TX, VT)

### Feature Requests
- Submit via feedback portal: https://support.rb2b.com/en/articles/11012656-feature-requests
- Can upvote existing requests

---

## Quick Reference

### Important URLs
- **Dashboard**: https://app.rb2b.com
- **Login**: https://app.rb2b.com/login (magic link, no password)
- **Script Page**: https://app.rb2b.com/script
- **Profiles**: https://app.rb2b.com/profiles
- **CSV Exports**: https://app.rb2b.com/profiles/exports
- **Integrations**: https://app.rb2b.com/integrations
- **Subscription**: https://app.rb2b.com/subscription
- **Hot Leads**: https://app.rb2b.com/filtering/hot_leads
- **Hot Pages**: https://app.rb2b.com/filtering/hot_pages
- **Opt-out**: https://app.retention.com/optout
- **GDPR Opt-out**: https://www.rb2b.com/rb2b-gdpr-opt-out
- **API Sign-up**: https://ui.api.rb2b.com/signup
- **Trust Portal**: https://retention.securitypal.com/
- **Feature Requests**: https://support.rb2b.com/en/articles/11012656-feature-requests

### Key Limitations
- **US-only** person-level identification
- **No public API** for regular users (API Partner Program exists separately)
- **No automatic CSV delivery** to external systems
- **Max 30-day CSV export** range
- **One integration instance** per platform per account
- **Credits don't roll over**
- **Script cannot run in iframes**
- URL Restrictions apply across all domains/subdomains (no per-domain rules)
- Domain Exclusion is by domain only, not individual email
- Cannot exclude specific companies from using credits (only URL-level control)

# PI Vendor Intelligence System

**Domain:** personalinjuryvendors.com
**Purpose:** AI-powered vendor matching for PI attorneys
**Head Agent:** SCOUT (@scoutassstantdatabot on Telegram)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PI VENDOR INTELLIGENCE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   REDDIT    │    │   REVIEWS   │    │  LINKEDIN   │    │
│  │  Scraper    │    │  Scraper    │    │  Scraper    │    │
│  │ (4h cycle)  │    │ (24h cycle) │    │ (24h cycle) │    │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    │
│         │                  │                  │            │
│         └──────────────────┼──────────────────┘            │
│                           ▼                                │
│                  ┌─────────────────┐                       │
│                  │   SQLite DB     │                       │
│                  │  (raw + dedup)  │                       │
│                  └────────┬────────┘                       │
│                           │                                │
│                           ▼                                │
│                  ┌─────────────────┐                       │
│                  │  AI Extractor   │                       │
│                  │  (GPT-4o-mini)  │                       │
│                  └────────┬────────┘                       │
│                           │                                │
│              ┌────────────┴────────────┐                   │
│              ▼                         ▼                   │
│     ┌─────────────────┐      ┌─────────────────┐          │
│     │ Vendor Profiles │      │ Buyer Profiles  │          │
│     └────────┬────────┘      └────────┬────────┘          │
│              │                        │                    │
│              └────────────┬───────────┘                    │
│                           ▼                                │
│                  ┌─────────────────┐                       │
│                  │ Matching Engine │                       │
│                  │ (scoring algo)  │                       │
│                  └────────┬────────┘                       │
│                           │                                │
│                           ▼                                │
│                  ┌─────────────────┐                       │
│                  │  SCOUT Bot      │                       │
│                  │  (Telegram UI)  │                       │
│                  └─────────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Sources

### Social/Forums
| Source | Method | Frequency | Data Collected |
|--------|--------|-----------|----------------|
| Reddit (14 subs) | Playwright | 4 hours | Posts, comments, vendor mentions |
| LinkedIn | Google search + public pages | Daily | Company info, discussions |
| Twitter/X | TBD | TBD | Mentions, complaints |

### Review Sites
| Source | Method | Frequency | Data Collected |
|--------|--------|-----------|----------------|
| Trustpilot | Playwright | Daily | Ratings, reviews, complaints |
| G2 | Playwright | Daily | B2B reviews, pros/cons |
| Capterra | Playwright | Daily | Software reviews |
| BBB | Playwright | Daily | Ratings, complaints, accreditation |
| Google Reviews | Maps API | Daily | Ratings, review counts |
| Clutch | Playwright | Daily | Agency reviews |

### Other
| Source | Method | Frequency | Data Collected |
|--------|--------|-----------|----------------|
| Avvo Q&A | TBD | Weekly | Legal discussions |
| Google News | Search | Daily | Lawsuits, PR |

---

## Data Schemas

### Vendor Profile
```yaml
vendor_profile:
  basics:
    name, url, phone, email, founded_year
    headquarters: {city, state}
    employee_count, description
    
  services:
    types: [leads|intake|marketing|directory|software|answering]
    case_types: [mva|mass_tort|med_mal|slip_fall|all|...]
    pricing_models: [{model, details, price_range}]
    geography: [nationwide|regional|state_specific]
    states_served: [...]
    integrations: [Clio|Filevine|...]
    
  reputation:
    ratings: {platform: {score, count}}
    aggregate_score: 0-5
    total_reviews: N
    sentiment_breakdown: {positive, neutral, negative}
    
  mentions: [{source, url, date, sentiment, summary}]
  red_flags: [{type, description, source, severity}]
  differentiators: [...]
  marketing_claims: [...]
```

### Buyer Profile
```yaml
buyer_profile:
  firm_info:
    size: solo|small|mid|large
    location: {state, city}
    case_types: [...]
    volume_tier: low|mid|high
    years_in_practice: N
    
  signals:
    pain_points: [{category, description, intensity, quote}]
    budget_signals: [{type, value, quote}]
    trust_factors: [{builds_trust, breaks_trust}]
    current_vendors: [{name, sentiment, quote}]
    switching_triggers: [...]
    decision_style: data_driven|relationship|price_focused|quality
```

---

## Matching Algorithm

Weighted scoring (0-100 per dimension):

| Factor | Weight | How Scored |
|--------|--------|------------|
| Pain Point Fit | 25% | Differentiators ↔ pain points |
| Budget Fit | 20% | Pricing model ↔ budget signals |
| Reputation | 20% | Aggregate review score |
| Geography | 15% | Coverage overlap |
| Case Type Match | 10% | Service area overlap |
| Size Fit | 10% | Enterprise vs small firm |

---

## SCOUT Commands

| Command | Description |
|---------|-------------|
| `/status` | System status, uptime, pipeline health |
| `/stats` | Database statistics |
| `/vendors` | List all tracked vendors |
| `/vendor <name>` | Detailed vendor profile |
| `/rankings` | Vendor reputation leaderboard |
| `/search <query>` | Search raw data |
| `/report` | Generate daily intelligence report |
| `/scrape <source>` | Trigger manual scrape |

---

## File Structure

```
/home/ec2-user/clawd/projects/pi-vendors/
├── PROJECT.md           # This file
├── requirements.txt     # Python dependencies
├── agents/
│   ├── base_scraper.py      # Base class for all scrapers
│   ├── coordinator.py       # Main orchestrator (24/7)
│   ├── scout_bot.py         # Telegram bot interface
│   ├── profile_extractor.py # AI processing
│   ├── matching_engine.py   # Vendor-buyer matching
│   └── scrapers/
│       ├── reddit_scraper.py
│       ├── review_scraper.py
│       └── linkedin_scraper.py
├── config/
│   ├── sources.json     # Keywords, subreddits, vendors
│   └── schemas.json     # Data structure definitions
├── data/
│   ├── vendor_intel.db  # SQLite database
│   ├── raw/             # Raw scraped data (backup)
│   ├── processed/       # Processed data
│   └── profiles/
│       ├── vendors/     # Vendor JSON profiles
│       └── buyers/      # Buyer insight profiles
├── scripts/
│   ├── run_scout.sh     # Start SCOUT bot
│   └── run_coordinator.sh # Start 24/7 scraper
└── logs/
```

---

## Running the System

### Start SCOUT Bot
```bash
./scripts/run_scout.sh
```

### Start Coordinator (24/7 scraper)
```bash
./scripts/run_coordinator.sh
```

### Or run as systemd services (production)
```bash
sudo systemctl start pi-vendors-scout
sudo systemctl start pi-vendors-coordinator
```

---

## Roadmap

### Phase 1: Data Collection (Current)
- [x] Reddit scraper
- [x] Review site scrapers (Trustpilot, G2, BBB)
- [x] LinkedIn scraper
- [x] SQLite database
- [x] SCOUT bot basic commands

### Phase 2: AI Processing
- [x] Profile extraction (GPT-4o-mini)
- [x] Buyer/vendor classification
- [x] Matching engine

### Phase 3: Intelligence
- [ ] Sentiment analysis
- [ ] Trend detection
- [ ] Alert system (new red flags, reviews)
- [ ] Weekly digest reports

### Phase 4: Launch
- [ ] personalinjuryvendors.com frontend
- [ ] Public matching tool
- [ ] Monetization (affiliate, premium)

---

## Estimated Costs

| Component | Cost |
|-----------|------|
| Scraping | Free (no APIs) |
| AI Extraction | ~$0.02/doc → ~$200 initial, $20/mo ongoing |
| Hosting | EC2 (existing) |
| **Total** | **~$20-50/month** |

---

*Last Updated: 2026-01-31*

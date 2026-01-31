# Vendor Database - Cost & Time Projection

## Current Setup

**Location:** `/home/ec2-user/clawd/projects/vendor-db/`

**Agents Created:**
1. `reddit_scraper.py` - Scrapes 9 subreddits × 15 keywords
2. `vendor_scraper.py` - Researches 44 known vendors
3. `coordinator.py` - Runs 24/7, schedules scrapes

## Data Sources & Estimates

### Reddit Scraping
| Subreddit | Est. Relevant Posts | Comments |
|-----------|---------------------|----------|
| r/LawFirm | 500+ | 2,000+ |
| r/lawyers | 300+ | 1,500+ |
| r/Lawyertalk | 200+ | 1,000+ |
| r/personalinjury | 100+ | 500+ |
| r/Insurance | 200+ | 800+ |
| r/marketing | 300+ | 1,200+ |
| r/PPC | 200+ | 800+ |
| r/digitalmarketing | 200+ | 800+ |
| **Total** | **2,000+** | **8,600+** |

### Vendor Data
| Category | Vendors | Est. Reviews/Mentions |
|----------|---------|----------------------|
| Lead Gen | 15 | 500+ |
| Directories | 6 | 1,000+ |
| Marketing Agencies | 10 | 800+ |
| Intake Services | 10 | 600+ |
| Mass Tort | 5 | 400+ |
| **Total** | **46** | **3,300+** |

## Cost Breakdown

### Scraping (Free)
- Reddit API: Free (rate limited to ~60 req/min)
- Web scraping: Free (using requests)
- **Cost: $0**

### AI Processing (for extraction & matching)
- GPT-4o-mini for text processing
- ~10,000 documents × avg 1,000 tokens = 10M tokens
- GPT-4o-mini: $0.15/1M input + $0.60/1M output
- **Est. cost: $10-20 for initial processing**

### Storage
- JSON files: Negligible
- SQLite: Free
- **Cost: $0**

### Total Estimated Cost
| Phase | Cost | Time |
|-------|------|------|
| Initial scrape | $0 | 3-5 days |
| AI processing | $10-20 | 2-4 hours |
| Ongoing monitoring | $5-10/month | Continuous |
| **Total Initial** | **~$20-30** | **5-7 days** |

## Time Estimates

### Reddit Rate Limits
- ~60 requests/minute allowed
- 9 subreddits × 15 keywords = 135 search queries
- Plus ~500 comment fetches for top posts
- **Initial Reddit scrape: ~2-3 hours**

### Vendor Research
- 46 vendors × 4 search queries each = 184 queries
- Plus review site scraping
- **Initial vendor scrape: ~4-6 hours**

### 24/7 Schedule
- Reddit refresh: Every 4 hours
- Vendor refresh: Every 12 hours
- **Daily API calls: ~500-800**

## Running the Swarm

### Start 24/7 daemon:
```bash
cd /home/ec2-user/clawd/projects/vendor-db
nohup python3 agents/coordinator.py > coordinator.log 2>&1 &
```

### Check status:
```bash
cat coordinator_state.json
ls -la data/
tail -f coordinator.log
```

### Stop:
```bash
pkill -f coordinator.py
```

## What You'll Get

### Buyer Insights Database
- 5,000+ data points on PI attorney concerns
- Pain points categorized by:
  - Vendor type (leads vs intake)
  - Firm size
  - Geography
  - Budget level
  - Experience with specific vendors

### Vendor Profiles Database
- 50+ vendor profiles with:
  - Ratings aggregated from multiple sources
  - Common complaints
  - Pricing info where available
  - Strengths & weaknesses
  - Red flags

### Matching Algorithm
- Input: Firm's needs, budget, past experiences
- Output: Top 3-5 vendor recommendations with reasoning

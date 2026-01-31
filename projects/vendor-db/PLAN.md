# Vendor Database Project - Data Collection Plan

## Goal
Build vendors.kuriosbrand.com - AI-powered vendor matching for PI attorneys

## Two Data Collection Streams

### Stream 1: Buyer Profiles (PI Attorneys)
**Data points to gather:**
- Pain points with current vendors
- Frustrations & complaints
- What worked well
- Budget ranges mentioned
- Firm size indicators
- Geographic preferences
- Case volume expectations
- Conversion rate expectations
- Vendor switching triggers
- Trust factors
- Red flags they mention

**Sources:**
- Reddit: r/LawFirm, r/lawyers, r/Lawyertalk, r/personalinjury, r/legal
- Avvo Q&A forums
- Legal marketing Facebook groups
- Twitter/X discussions
- Quora legal marketing threads
- Legal industry forums
- Review site comments
- LinkedIn discussions

### Stream 2: Vendor Profiles
**Data points to gather:**
- Company name, URL, contact
- Services offered (leads, intake, both)
- Pricing models mentioned
- Geographic coverage
- Case types handled
- Reviews & ratings
- Complaints & lawsuits
- Years in business
- Client testimonials
- Red flags
- Unique selling points
- Integration capabilities

**Sources:**
- Google search results
- Trustpilot, G2, Capterra reviews
- BBB profiles & complaints
- Reddit mentions
- Legal directories
- Clutch.co
- LinkedIn company pages
- Glassdoor (employee insights)
- Court records (lawsuits)
- News articles

## Agent Swarm Architecture

### Coordinator Agent (Queen)
- Assigns tasks to worker agents
- Aggregates results
- Deduplicates data
- Manages rate limits

### Worker Agents
1. **Reddit Scraper** - Monitors legal subreddits
2. **Review Scraper** - G2, Trustpilot, Capterra
3. **Search Agent** - Google searches for vendors
4. **Forum Scraper** - Avvo, legal forums
5. **Social Scraper** - Twitter/LinkedIn mentions
6. **Aggregator** - Combines & structures data

## Cost Projections

### API Costs (Estimated)
- Web scraping: Free (using requests/beautifulsoup)
- OpenAI for extraction: ~$0.01-0.03 per page processed
- Storage: Minimal (JSON/SQLite)

### Volume Estimates
- Reddit: ~5,000 relevant posts/comments
- Reviews: ~2,000 vendor reviews
- Forum posts: ~3,000 discussions
- Vendor profiles: ~500 companies

### Processing Cost Estimate
- 10,000 documents × $0.02 avg = **~$200 total**
- Running 24/7 for initial scrape: ~3-5 days
- Ongoing monitoring: ~$10-20/month

## Data Storage
- SQLite for structured data
- JSON files for raw scrapes
- Vector embeddings for semantic search

## Output
- vendors.json - All vendor profiles
- buyer_insights.json - Aggregated buyer data
- matches.json - Vendor-buyer matching rules

# MVA Dual Visibility Calculator Spec

## Overview
Two scores for PI lawyers:
1. **AI Visibility Score** (0-100) - How visible in ChatGPT, Perplexity, Google AI Overviews
2. **Local Visibility Score** (0-100) - How visible in Google Maps/Local Pack

---

## AI VISIBILITY SCORE (Based on GEO/AEO Research)

### Sources:
- Jacky Chou AI SEO/GEO Course (EP744)
- ChatBeat AI SEO Guide
- Onely 12-Step GEO Checklist
- Rankshift GEO Checklist
- Ahrefs AI Overview Brand Correlation Study

### Key Findings:
- Web mentions correlate **3x more** with AI visibility than backlinks (0.664 vs 0.218)
- AI-sourced visitors convert at **27%** vs 2.1% from traditional search (12x better)
- 60% of queries now end in zero-click answers
- Top quartile brands get **10x more** AI citations than others

### Scoring Criteria (10 categories, 10 points each = 100 total)

#### 1. CRAWLER ACCESS (10 pts)
- robots.txt allows AI crawlers (GPTBot, Anthropic, PerplexityBot) [3 pts]
- llms.txt file implemented [3 pts]
- Server-side rendering (not JS-only) [4 pts]

#### 2. STRUCTURED DATA (10 pts)
- FAQPage schema [3 pts]
- LocalBusiness/LegalService schema [3 pts]
- Author schema with credentials [2 pts]
- Organization schema [2 pts]

#### 3. CONTENT STRUCTURE (10 pts)
- Clear H2/H3 hierarchy [2 pts]
- Short paragraphs (2-4 sentences) [2 pts]
- Answer-first format under each heading [3 pts]
- Tables/lists for comparisons [3 pts]

#### 4. E-E-A-T SIGNALS (10 pts)
- Named attorney authors with bio pages [3 pts]
- Credentials displayed (bar #, years experience) [3 pts]
- Case results/settlements shown [2 pts]
- External validation (Avvo, Martindale ratings) [2 pts]

#### 5. BRAND MENTIONS (10 pts)
- Wikipedia/Wikidata presence [3 pts]
- Reddit mentions (positive, in relevant threads) [2 pts]
- Industry publications/PR mentions [3 pts]
- Review site presence (Avvo, Google, Yelp) [2 pts]

#### 6. CONTENT FRESHNESS (10 pts)
- datePublished/dateModified metadata [4 pts]
- Blog updated in last 30 days [3 pts]
- News/case updates section [3 pts]

#### 7. QUESTION-BASED CONTENT (10 pts)
- FAQ section with real questions [4 pts]
- Content mirrors how users query AI [3 pts]
- Process/HowTo content (what to do after accident) [3 pts]

#### 8. CITATIONS & SOURCES (10 pts)
- Content cites authoritative sources [3 pts]
- Statistics with attribution [3 pts]
- Links to government/legal sources [2 pts]
- Original data/research [2 pts]

#### 9. TECHNICAL PERFORMANCE (10 pts)
- Page load < 3 seconds [4 pts]
- Mobile-friendly [3 pts]
- Core Web Vitals passing [3 pts]

#### 10. AI PLATFORM PRESENCE (10 pts)
- YouTube channel with transcripts enabled for AI training [4 pts]
- Mentioned when querying ChatGPT about "[city] truck accident lawyer" [4 pts]
- Present in Google AI Overviews for relevant queries [2 pts]

---

## LOCAL VISIBILITY SCORE (Based on 65-Point Local SEO Checklist)

### Sources:
- Jacky Chou/LocalRank 65-Point Local SEO Checklist
- LocalRank.so Complete Guide
- LiftedWebsites Local SEO Guide

### Key Findings:
- 46% of all Google searches have local intent
- 42% of local searchers click on map pack results
- GBP, NAP consistency, and reviews are the top 3 factors
- Proximity + Relevance + Prominence = Local rankings

### Scoring Criteria (10 categories, 10 points each = 100 total)

#### 1. GOOGLE BUSINESS PROFILE BASICS (10 pts)
- Claimed and verified [2 pts]
- Business name accurate (no keyword stuffing) [2 pts]
- Complete address with correct ZIP [2 pts]
- Local phone number (not toll-free) [2 pts]
- Primary category = "Personal Injury Attorney" or similar [2 pts]

#### 2. GBP OPTIMIZATION (10 pts)
- Secondary categories added [2 pts]
- Detailed description with keywords [2 pts]
- High-quality photos (storefront, interior, team) [2 pts]
- Products/services listed [2 pts]
- Accurate business hours including holidays [2 pts]

#### 3. GBP ENGAGEMENT (10 pts)
- Regular posts (weekly/monthly) [3 pts]
- Messaging enabled [2 pts]
- Q&A section populated [2 pts]
- Attributes set (wheelchair accessible, etc.) [3 pts]

#### 4. WEBSITE LOCAL SIGNALS (10 pts)
- Mobile-friendly responsive design [2 pts]
- Page load < 3 seconds [2 pts]
- Local keywords in page titles [2 pts]
- City/state in meta descriptions [2 pts]
- LocalBusiness schema markup [2 pts]

#### 5. NAP CONSISTENCY (10 pts)
- NAP on every page (footer) [3 pts]
- Clickable phone number [2 pts]
- Embedded Google Map [2 pts]
- HTTPS secure [1 pt]
- Consistent NAP format everywhere [2 pts]

#### 6. LOCATION PAGES (10 pts)
- City-specific landing pages [4 pts]
- Local testimonials from that area [3 pts]
- Local content (mentions of highways, hospitals, courts) [3 pts]

#### 7. CITATIONS & DIRECTORIES (10 pts)
- Listed on major directories (Yelp, FindLaw, Avvo) [3 pts]
- NAP consistency across all citations [3 pts]
- Industry-specific directories [2 pts]
- Local chamber of commerce [2 pts]

#### 8. REVIEWS (10 pts)
- 20+ Google reviews [3 pts]
- 4.5+ average rating [3 pts]
- Reviews in last 30 days (velocity) [2 pts]
- Owner responds to reviews [2 pts]

#### 9. LOCAL CONTENT (10 pts)
- Blog posts about local events/news [3 pts]
- Content addressing local pain points [3 pts]
- Case studies of local clients [2 pts]
- Community involvement content [2 pts]

#### 10. LOCAL LINK BUILDING (10 pts)
- Backlinks from local news sites [3 pts]
- Sponsor local events [2 pts]
- Partner links from local businesses [2 pts]
- Local social media engagement [3 pts]

---

## CALCULATOR UX DESIGN

### Question Flow (Self-Assessment Version)
Each section has 2-3 yes/no or multiple choice questions

**AI Visibility Questions:**
1. Do you allow AI crawlers (GPTBot) in your robots.txt? (Yes/No/Don't know)
2. Do you have FAQ schema on your website? (Yes/No/Don't know)
3. When did you last update your blog? (This week/This month/3+ months/Never)
4. Does your content cite statistics with sources? (Yes/Rarely/No)
5. Do attorneys have bio pages with credentials? (Yes/No)
6. Have you checked if you're mentioned in ChatGPT responses? (Yes, we appear/Yes, we don't/No)
...etc (12-15 questions total)

**Local Visibility Questions:**
1. Is your Google Business Profile claimed and verified? (Yes/No/Don't know)
2. How many Google reviews do you have? (0-10/11-25/26-50/50+)
3. What's your average rating? (Below 4.0/4.0-4.4/4.5-4.9/5.0)
4. Do you have city-specific landing pages? (Yes, multiple/Yes, one/No)
5. When did you last post on GBP? (This week/This month/3+ months/Never)
...etc (12-15 questions total)

### Results Display
- Two gauges/scores side by side
- AI Score: X/100 | Local Score: X/100
- Combined "Total Visibility Score" X/200
- Breakdown by category
- Top 3 quick wins for each score
- CTA: "Get a Full Audit" / "Book a Strategy Call"

### PDF Report
- Executive summary
- Score breakdown
- Comparison to average PI law firm
- Specific recommendations
- Competitive analysis preview (teaser)

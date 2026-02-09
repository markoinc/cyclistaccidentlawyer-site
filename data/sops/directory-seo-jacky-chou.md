# Directory SEO SOP
## Based on Jacky Chou's YouTube Content & Industry Best Practices

**Source Videos:**
- "Create a Directory on ANY Niche Site" (BIP Day 18)
- "Uncovering an INSANE Directory ($50m/yr)" 
- "I created a directory on WP with no plugins" (BIP 393)
- "I created a directory in 5 minutes with AI" (BIP472)
- "My directory is FLYING, here's how I did it"
- "Getting DR90+ on my directory"
- "How I Built & Sold a $190K Directory With Facebook Ads" (BIP613)

**Last Updated:** February 2026

---

## Table of Contents
1. [Overview & Why Directories Work](#overview--why-directories-work)
2. [Step-by-Step Build Process](#step-by-step-build-process)
3. [Tech Stack](#tech-stack)
4. [Content Strategy](#content-strategy)
5. [SEO Tactics](#seo-tactics)
6. [Monetization Methods](#monetization-methods)
7. [Traffic Strategies](#traffic-strategies)
8. [Timeline Expectations](#timeline-expectations)
9. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
10. [Case Studies & Examples](#case-studies--examples)

---

## Overview & Why Directories Work

### What is a Directory Site?
A directory site is a curated database of listings within a specific niche (businesses, products, services, locations, tools, etc.) that provides value to users searching for specific solutions.

### Why Directories Are Powerful for SEO:
- **Programmatic SEO at scale** - Create thousands of pages targeting long-tail keywords
- **High indexation potential** - Each listing = potential ranking page
- **Natural link acquisition** - Businesses link back to their listings
- **Multiple monetization paths** - Ads, affiliates, paid listings, leads
- **Relatively low content cost** - Structured data vs. editorial content
- **Defensible moat** - First-mover advantage with comprehensive data

### Jacky Chou's Directory Philosophy:
> "The key is finding niches where people are actively searching for lists/directories of things. Then you build the most comprehensive, useful resource."

---

## Step-by-Step Build Process

### Phase 1: Niche Selection & Validation (Week 1)

#### 1.1 Find Directory Opportunities
Look for search patterns like:
- "[Industry] directory"
- "Best [service] in [location]"
- "List of [products/companies]"
- "[Category] near me"
- "Top [X] [industry] companies"

**Tools to use:**
- Ahrefs/SEMrush keyword explorer
- Google autocomplete suggestions
- AnswerThePublic
- AlsoAsked.com

#### 1.2 Validate the Niche
✅ Check for:
- Search volume for directory-style queries (aim for 1K+ monthly searches)
- Existing directories (weak competition = opportunity)
- Businesses willing to pay for exposure
- Affiliate programs in the space
- Data availability for initial population

❌ Avoid:
- Heavily regulated industries (legal/medical unless you have expertise)
- Niches with no clear monetization
- Markets too small to scale

#### 1.3 Competitive Analysis
Analyze top 5 existing directories for:
- Domain Rating (DR) / Domain Authority (DA)
- Number of pages indexed
- Monetization methods
- Content structure
- User experience gaps you can exploit

### Phase 2: Technical Setup (Week 2)

#### 2.1 Domain Selection
- Exact match domains (EMDs) still work for directories
- Brandable domains if building long-term
- Consider expired domains with existing authority
- Check domain history via Wayback Machine

#### 2.2 Hosting Setup
```
Recommended: Cloudways (managed cloud hosting)
- Starting at ~$14/month
- Vultr or DigitalOcean servers
- Built-in CDN options
- Automatic backups
- Server-level caching
```

#### 2.3 WordPress Installation
```
1. Install WordPress via Cloudways
2. Remove default content/plugins
3. Set up SSL (Let's Encrypt - free)
4. Configure permalinks: /%postname%/
5. Install core plugins (see Tech Stack)
```

### Phase 3: Design & Structure (Week 2-3)

#### 3.1 Site Architecture
```
Homepage
├── Category Pages (e.g., /restaurants/)
│   ├── Location Pages (e.g., /restaurants/new-york/)
│   │   └── Individual Listings
│   └── Subcategory Pages
├── Location Landing Pages
├── About/Contact
└── Blog (for editorial SEO support)
```

#### 3.2 Template Creation
Build templates for:
1. **Homepage** - Search bar, featured categories, featured listings
2. **Category Archive** - Filterable list of listings
3. **Location Pages** - Listings filtered by geography
4. **Single Listing Page** - Business details, reviews, contact info
5. **Comparison Pages** - "Best X vs Y" style content

### Phase 4: Content Population (Week 3-4)

#### 4.1 Initial Data Collection
Sources for directory data:
- Government databases (business registrations)
- Industry associations
- Existing directories (scrape ethically)
- Public APIs
- LinkedIn company data
- Google Maps business listings
- Crunchbase/AngelList for tech niches

#### 4.2 Data Structure
Create a spreadsheet/database with:
```csv
name,category,subcategory,city,state,country,address,phone,website,description,logo_url,features,pricing_tier
```

#### 4.3 AI Content Generation
Use AI to enhance listings:
- Generate unique descriptions for each listing
- Create category overview content
- Build location-specific landing page content
- Generate comparison content

**Jacky's approach:** 
> "Use AI to generate the variable content at scale, but make sure it's based on real data and addresses actual user needs."

### Phase 5: Launch & Index (Week 4-5)

#### 5.1 Pre-Launch Checklist
- [ ] All pages loading correctly
- [ ] Mobile responsive
- [ ] Core Web Vitals passing
- [ ] XML sitemap generated
- [ ] Robots.txt configured
- [ ] Internal linking in place
- [ ] Schema markup implemented

#### 5.2 Indexing Strategy
```
1. Submit sitemap to Google Search Console
2. Submit to Bing Webmaster Tools
3. Use IndexNow for faster indexing
4. Request indexing for key pages manually
5. Build initial backlinks to encourage crawling
```

---

## Tech Stack

### Recommended by Jacky Chou & Industry Best Practices

#### Core Theme
| Option | Cost | Best For |
|--------|------|----------|
| **Kadence** (Jacky's choice) | Free / $149 Pro | Speed, flexibility, Gutenberg-native |
| GeneratePress | Free / $59 Pro | Lightweight, fast, developer-friendly |
| Astra | Free / $59 Pro | Largest theme library |

#### Essential Plugins

**Directory Functionality:**
| Plugin | Purpose | Cost |
|--------|---------|------|
| GeoDirectory | Full directory features | Free / $199+ |
| Business Directory Plugin | Simple directories | Free / $199 |
| WP All Import | Bulk data import | $99 |
| Multiple Pages Generator (MPG) | Programmatic pages | Free / $99 |
| ACF (Advanced Custom Fields) | Custom listing fields | Free / $49 |

**SEO & Performance:**
| Plugin | Purpose | Cost |
|--------|---------|------|
| RankMath | SEO optimization | Free / $59 |
| WPRocket | Caching & speed | $59/year |
| ShortPixel | Image optimization | Pay-per-use |
| Cloudflare | CDN & security | Free |

**Functionality:**
| Plugin | Purpose | Cost |
|--------|---------|------|
| Link Whisper | Internal linking | $77/year |
| TablePress/NinjaTables | Data tables | Free / $49 |
| Wordfence | Security | Free |
| ManageWP | Site management | $0-2/site |

### No-Plugin Directory Approach
Jacky demonstrates building directories using only:
- Kadence Theme + Kadence Blocks
- Custom post types (via code or ACF)
- Simple taxonomies for categories/locations
- CSS Grid for layouts

**Benefits:** Faster load times, fewer plugin conflicts, easier maintenance

### Tech Stack for Scale
For larger directories (10K+ listings):
```
- Static site generator (Hugo/11ty) + headless CMS
- OR WordPress with:
  - Redis object caching
  - Dedicated database server
  - Cloudflare Enterprise
  - Custom REST API for listings
```

---

## Content Strategy

### The Programmatic SEO Approach

#### Page Types to Create

**1. Listing Pages (80% of pages)**
Each business/item gets its own page with:
- Name, description, contact info
- Category & location tags
- User reviews/ratings
- Related listings
- Schema markup

**2. Category Pages (15% of pages)**
```
/web-design-agencies/
├── Unique intro content (200-500 words)
├── Filterable listing grid
├── FAQ section
├── Related categories
└── Internal links to subcategories
```

**3. Location Pages (Geographic targeting)**
```
/web-design-agencies/new-york/
├── Location-specific intro
├── Filtered listings for that location
├── Local statistics/data
├── Related locations
```

**4. Comparison & Editorial Pages (5% of pages)**
- "Best [X] in [Location]"
- "[Business A] vs [Business B]"
- "How to choose a [category]"
- Industry guides & resources

### Content Quality Guidelines

#### Avoid Thin Content
Each page must have:
- **Unique title** with target keyword
- **Unique meta description**
- **At least 150-300 words** of unique content
- **Structured data** relevant to the listing
- **Internal links** to related pages

#### AI Content Best Practices
```
✅ DO:
- Use AI to generate descriptions based on real data
- Create variable content that changes per listing
- Include factual information (hours, services, features)
- Add user-generated content (reviews, ratings)

❌ DON'T:
- Generate generic filler content
- Create duplicate descriptions across listings
- Use AI content without human review
- Ignore E-E-A-T signals
```

### Content Velocity

**Initial Launch:**
- Aim for 500-1,000 listings minimum
- All major categories covered
- 10-20 editorial/supporting pages

**Scaling Phase:**
- Add 100-500 new listings per week
- Create location pages as you expand
- Publish 2-4 editorial pieces per month

---

## SEO Tactics

### On-Page SEO

#### Title Tag Formula
```
[Business Name] - [Category] in [Location] | [Site Name]
OR
[Category] in [Location] - Find the Best [X] | [Site Name]
```

#### URL Structure
```
Good: /category/location/business-name/
Good: /category/business-name/
Avoid: /listing/id=12345/
```

#### Schema Markup (Critical!)
Implement for each listing:
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "City",
    "addressRegion": "State"
  },
  "telephone": "+1-555-555-5555",
  "url": "https://business-website.com",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.5",
    "reviewCount": "47"
  }
}
```

Also implement:
- BreadcrumbList schema
- FAQ schema on category pages
- Article schema on blog posts

#### Internal Linking Strategy
```
Homepage → Category pages (clear navigation)
Category pages → Subcategories + top listings
Listing pages → Related listings in same category
Location pages → Nearby location pages
All pages → Relevant category pages via breadcrumbs
```

**Use Link Whisper** to automate internal link suggestions.

### Off-Page SEO / Link Building

#### Strategies That Work for Directories

**1. Digital PR & Data Studies**
- Create annual "State of [Industry]" reports
- Publish local market statistics
- Share unique data insights with journalists

**2. HARO (Help A Reporter Out)**
- Respond to journalist queries as an industry expert
- Provide data/statistics from your directory
- Aim for links from DR50+ publications

**3. Guest Posting**
- Target industry blogs and publications
- Write about trends, not your directory directly
- Link naturally to relevant category pages

**4. Niche Edits (Paid Link Insertions)**
- Identify relevant existing content
- Pay for contextual link placements
- Focus on niche-relevant sites over pure DR

**5. Business Outreach**
- Notify listed businesses of their listings
- Many will link back voluntarily
- Offer enhanced listings for backlinks

**6. Resource Page Link Building**
- Find "resources" pages in your industry
- Pitch your directory as a useful resource
- Focus on .edu and .gov opportunities

#### Building DR/DA (Domain Rating)

**Jacky's DR90+ Strategy:**
1. **Foundation links** - Branded citations, profiles, directories
2. **Quality guest posts** - 5-10 per month from DR40+ sites
3. **Digital PR wins** - 1-2 major publications per quarter
4. **HARO responses** - Consistent weekly submissions
5. **Natural links** - From businesses you list

**Timeline to DR60+:** 6-12 months with consistent effort

### Technical SEO

#### Site Speed
- Target < 3 second load time
- Use lazy loading for images
- Implement proper caching
- Minimize JavaScript
- Use a CDN (Cloudflare)

#### Crawlability
```
robots.txt:
User-agent: *
Allow: /
Sitemap: https://yourdirectory.com/sitemap_index.xml

# Block low-value pages
Disallow: /search/
Disallow: /*?sort=
Disallow: /*?filter=
```

#### Handling Pagination
- Use rel="next" and rel="prev" (though Google claims to ignore)
- Implement proper canonical tags
- Consider infinite scroll with SEO fallback

---

## Monetization Methods

### 1. Display Advertising
**Best for:** High-traffic directories (50K+ monthly visitors)

| Network | Requirements | RPM Range |
|---------|--------------|-----------|
| Google AdSense | None | $1-5 |
| Mediavine | 50K sessions/month | $10-25 |
| AdThrive | 100K pageviews/month | $15-30 |
| Ezoic | 10K pageviews/month | $5-15 |

**Placement strategy:**
- Sidebar ads on listing pages
- In-content ads on category pages
- Sticky footer on mobile

### 2. Paid/Featured Listings
**Best for:** B2B directories, competitive niches

**Pricing Models:**
```
Freemium:
- Free: Basic listing
- $49/month: Enhanced listing (photos, video, priority)
- $99/month: Featured listing (top of category)
- $199/month: Premium (featured + homepage + blog mention)

OR One-time:
- $199: Lifetime enhanced listing
- $499: Annual featured placement
```

**What to include in paid tiers:**
- Priority/top placement
- Additional images/video
- Expanded description
- Direct contact form
- Analytics/insights
- Badge/verification

### 3. Affiliate Marketing
**Best for:** Product/service directories

**Opportunities:**
- Link listings to affiliate programs
- Create "best of" comparison pages
- Tool/software recommendations
- Service provider referrals

**Example:** SaaS directory with affiliate links to software trials

### 4. Lead Generation
**Best for:** Service directories (lawyers, contractors, etc.)

**Models:**
- **Pay per lead:** $10-100+ depending on industry
- **Exclusive leads:** Premium pricing for exclusive referrals
- **Subscription:** Businesses pay monthly for all leads in their area

**Implementation:**
- Contact forms on listing pages
- Quote request functionality
- Call tracking numbers

### 5. Sponsored Content
- Sponsored category takeovers
- Sponsored blog posts/guides
- Newsletter sponsorships
- Social media promotions

### Revenue Expectations
```
Year 1: $0-5,000/month (building traffic & authority)
Year 2: $5,000-20,000/month (multiple revenue streams)
Year 3+: $20,000-100,000+/month (scaled & optimized)
```

**Jacky's $190K directory sale:** Built primarily with paid traffic (Facebook Ads) to prove revenue model, then sold for ~3x annual revenue.

---

## Traffic Strategies

### SEO Traffic (Long-term focus)

**Expectations:**
- Month 1-3: Minimal traffic (indexing phase)
- Month 4-6: Early wins on long-tail keywords
- Month 6-12: Compounding growth
- Year 2+: Significant organic traffic

**Tactics:**
1. Target long-tail keywords first
2. Build topical authority through categories
3. Create supporting editorial content
4. Build backlinks consistently
5. Optimize based on Search Console data

### Paid Traffic (Acceleration)

#### Facebook Ads
From Jacky's $190K directory case study:
```
Strategy:
1. Create free listings for businesses
2. Run ads promoting directory to business owners
3. Offer free listing → upsell to premium
4. Retarget visitors with premium offers

Budget: Start with $20-50/day testing
Target: Business owners in your niche
Creative: Show value of being listed
```

#### Google Ads
- Target branded searches (competitors)
- Run ads for "best [category] in [location]"
- Promote premium listings to businesses

### The Directory Flywheel

```
Step 1: Create directory with quality listings
    ↓
Step 2: Run paid ads to drive initial traffic
    ↓
Step 3: Convert visitors to sign up (free listings)
    ↓
Step 4: Upsell to premium listings
    ↓
Step 5: Reinvest revenue into more ads & SEO
    ↓
Step 6: Growing traffic makes SEO easier (authority)
    ↓
Return to Step 2 with more budget
```

### Content Marketing
- Industry blog posts (drives organic + referrals)
- Annual reports/studies (linkable assets)
- Email newsletter (retention + monetization)
- Social media presence (brand + traffic)

### Community Building
- Create a community around the directory
- User-generated reviews and content
- Business owner forums/groups
- Events and webinars

---

## Timeline Expectations

### Realistic Milestones

| Phase | Timeframe | What to Expect |
|-------|-----------|----------------|
| Setup | Week 1-2 | Domain, hosting, theme, plugins installed |
| Build | Week 3-4 | 500-1,000 listings populated |
| Launch | Month 1 | Site live, submitted to search engines |
| Indexing | Month 2-3 | Pages getting indexed, minimal traffic |
| Early Wins | Month 4-6 | Long-tail rankings, 1K-5K visitors/month |
| Growth | Month 7-12 | Compounding traffic, first revenue |
| Scale | Year 2 | 10K-50K+ visitors/month, diversified revenue |
| Mature | Year 3+ | 100K+ visitors, acquisition target |

### Investment Required

**Time:**
- Setup: 40-80 hours
- Content population: 20-40 hours
- Ongoing maintenance: 5-10 hours/week
- Link building: 5-10 hours/week

**Money:**
| Item | One-time | Monthly |
|------|----------|---------|
| Domain | $10-50 | - |
| Hosting | - | $14-50 |
| Theme | $50-150 | - |
| Plugins | $200-500 | - |
| Link building | - | $500-2,000 |
| Content/VA | - | $500-1,500 |
| **Total** | **$260-700** | **$1,000-3,500** |

**Minimum Viable Investment:** ~$500 upfront + $500/month

---

## Common Mistakes to Avoid

### 1. Thin/Duplicate Content
❌ **Problem:** Same description template for all listings
✅ **Solution:** Generate unique descriptions with AI, include unique data points

### 2. Poor Internal Linking
❌ **Problem:** Orphaned pages with no links
✅ **Solution:** Use Link Whisper, create hub-and-spoke structure

### 3. Ignoring User Experience
❌ **Problem:** Slow site, poor mobile experience, hard to navigate
✅ **Solution:** Prioritize Core Web Vitals, mobile-first design

### 4. Keyword Cannibalization
❌ **Problem:** Multiple pages targeting same keyword
✅ **Solution:** Clear URL structure, canonical tags, distinct page purposes

### 5. Trying to Monetize Too Early
❌ **Problem:** Aggressive ads/popups before traffic
✅ **Solution:** Build value and traffic first, monetize at 10K+ visitors

### 6. Neglecting Backlinks
❌ **Problem:** Building pages but no link building
✅ **Solution:** Consistent link building from day 1 (5-10 links/week minimum)

### 7. Not Claiming Business Buy-In
❌ **Problem:** Businesses don't know they're listed
✅ **Solution:** Outreach to listed businesses, encourage them to claim/enhance listings

### 8. Overcomplicating Tech Stack
❌ **Problem:** 30+ plugins, custom code everywhere
✅ **Solution:** Keep it simple - Kadence/GP + minimal plugins

### 9. Giving Up Too Early
❌ **Problem:** Expecting results in 30 days
✅ **Solution:** Commit to 12+ months before evaluating success

### 10. Not Differentiating
❌ **Problem:** Another generic directory
✅ **Solution:** Best data, unique features, superior UX, proprietary insights

---

## Case Studies & Examples

### Successful Directory Models

**Clutch.co** (~$50M/year directory)
- B2B service provider directory
- Lead generation model
- Reviews and ratings focus
- DR90+ authority site

**Yelp**
- Local business directory
- Ad-based revenue model
- User reviews as moat
- Programmatic SEO at massive scale

**G2/Capterra**
- Software review directories
- Lead gen + affiliate model
- User reviews critical

**Jacky Chou's Sold Directory** ($190K sale)
- Built with Facebook ads
- Freemium listing model
- Sold at ~3x annual revenue
- Proof of concept for paid traffic → directory sale

### Niche Directory Opportunities (2026)

High-potential niches:
- AI tools directory
- Remote work services
- Sustainable/eco businesses
- Healthcare providers (telemedicine)
- Home services by location
- SaaS alternatives
- Creator economy tools
- Local food/farm directories

---

## Quick Start Checklist

### Week 1
- [ ] Validate niche and keyword opportunity
- [ ] Purchase domain
- [ ] Set up Cloudways hosting
- [ ] Install WordPress + Kadence theme
- [ ] Install essential plugins

### Week 2
- [ ] Create site structure and categories
- [ ] Build page templates (homepage, category, listing)
- [ ] Collect initial listing data (500+ listings)
- [ ] Set up schema markup

### Week 3-4
- [ ] Import listings via WP All Import or MPG
- [ ] Generate unique content for listings
- [ ] Create category landing pages
- [ ] Implement internal linking

### Month 1 Post-Launch
- [ ] Submit to Google Search Console & Bing
- [ ] Begin link building campaign
- [ ] Outreach to listed businesses
- [ ] Monitor indexing progress

### Ongoing Monthly
- [ ] Add 100-500 new listings
- [ ] Build 20-40 backlinks
- [ ] Publish 2-4 editorial pieces
- [ ] Analyze and optimize top pages
- [ ] Test monetization methods

---

## Resources

### Jacky Chou's Resources
- YouTube: Jacky Chou from Indexsy
- Newsletter: MarketingLetter.com
- Community: Advise.so
- Tools: LocalRank.so, Trackings.ai

### Recommended Tools
- **SEO:** Ahrefs, SEMrush, RankMath
- **Hosting:** Cloudways
- **Theme:** Kadence, GeneratePress
- **Plugins:** WP All Import, MPG, GeoDirectory
- **Link Building:** HARO, Indexsy services

### Further Reading
- Building in Public (BIP) show notes: marketingletter.com/bip-sheet
- Niche Pursuits podcast interviews
- Indexsy blog: indexsy.com

---

*This SOP is a living document. Update as strategies evolve and new techniques emerge.*

**Version:** 1.0  
**Created:** February 2026  
**Author:** Research compiled from Jacky Chou's YouTube content and industry best practices

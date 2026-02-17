# Super Agent: Concrete Site Full Optimization

## Overview
This agent runs a complete 5-audit optimization process on any concrete contractor website, fixing all issues automatically.

## Input Required
- `SITE_PATH`: Path to the site directory (e.g., ~/clawd/sites/sitename/)
- `BUSINESS_NAME`: Full business name
- `PHONE`: Phone number in (XXX) XXX-XXXX format
- `ADDRESS`: Full street address
- `CITY`: City name
- `STATE`: State abbreviation
- `GBP_URL`: Google Business Profile URL
- `GBP_MAP_EMBED`: Google Maps embed iframe code
- `GHL_FORM_URL`: GoHighLevel form embed URL
- `REVIEWS`: Array of real customer reviews with names and dates
- `CLOUDFLARE_TOKEN`: Cloudflare API token for deployment
- `CF_PROJECT_NAME`: Cloudflare Pages project name

## Audit Process (Run in Order)

### 1. DESIGN AUDIT
Checklist:
- [ ] Visual consistency across all pages (colors, fonts, spacing)
- [ ] Header/footer identical on all pages
- [ ] Mobile responsiveness on all pages
- [ ] Image optimization (alt tags, sizes, lazy loading)
- [ ] Typography hierarchy (H1, H2, H3 proper usage)
- [ ] Button/CTA styling consistency
- [ ] Form styling consistency
- [ ] Card/component design consistency
- [ ] Whitespace and padding consistency
- [ ] Color contrast accessibility
- [ ] Google Fonts on all pages
- [ ] Mobile menu JS on all pages
- [ ] Sticky mobile CTA on all pages
- [ ] Privacy/Terms links in footer

### 2. LOCAL SEO AUDIT
Reference: ~/clawd/data/jacky-brain/local-seo-sops.md

Checklist:
- [ ] LocalBusiness schema on EVERY page (not just homepage)
- [ ] NAP consistency everywhere
- [ ] GeoCoordinates on location pages
- [ ] City + keyword in title tags
- [ ] City mentions in H1, H2 headings
- [ ] Local keywords in meta descriptions
- [ ] Service area mentions
- [ ] Google Map embed present
- [ ] Driving directions link on all pages
- [ ] GBP link present on all pages
- [ ] Local phone format consistent
- [ ] Full address in footer on all pages
- [ ] Location pages have unique content
- [ ] Internal linking between location pages
- [ ] sameAs with GBP URL in schema

### 3. CRO AUDIT
Checklist:
- [ ] Form above fold on key pages (home, contact, service pages)
- [ ] Phone number click-to-call on ALL pages
- [ ] CTA buttons prominent and consistent
- [ ] Trust signals visible (Licensed, Insured, Years Experience)
- [ ] Social proof (reviews, testimonials, counter)
- [ ] Urgency elements where appropriate
- [ ] Clear value proposition on each page
- [ ] Mobile CTA sticky bar working
- [ ] Exit intent popup on all pages
- [ ] Form fields minimal (reduce friction)
- [ ] Thank you page has next steps + referral incentive
- [ ] Multiple conversion paths (call, form)
- [ ] Testimonials on service pages
- [ ] Forms on ALL location pages

### 4. AI SEO / GEO AUDIT
Reference: ~/clawd/data/jacky-brain/ai-seo-sops.md

Checklist:
- [ ] FAQ schema with 15+ questions
- [ ] "Best X in [City]" content structure
- [ ] Clear entity definition (business name, what it does)
- [ ] Consistent NAP for entity recognition
- [ ] Listicle-style content sections
- [ ] Statistics and data points
- [ ] Comparison content ("vs" sections)
- [ ] Question-style headings (How much, What is, etc.)
- [ ] Authoritative outbound links
- [ ] Schema markup complete
- [ ] Clear service definitions
- [ ] Location + service combinations
- [ ] Expert positioning content
- [ ] foundingDate in schema
- [ ] Visible FAQ accordion on homepage

### 5. TECHNICAL SEO AUDIT
Checklist:
- [ ] robots.txt exists and correct
- [ ] sitemap.xml exists with all pages
- [ ] Canonical tags on ALL pages
- [ ] Meta titles <60 chars, unique
- [ ] Meta descriptions <160 chars, unique
- [ ] H1 tags - one per page, unique
- [ ] Image alt tags on ALL images
- [ ] Image sizes optimized (<200KB each)
- [ ] No broken internal/external links
- [ ] HTTPS URLs everywhere
- [ ] Mobile viewport meta tag
- [ ] Proper HTML5 structure
- [ ] No duplicate content
- [ ] Lazy loading on images
- [ ] 404 page exists
- [ ] Favicon present
- [ ] OG tags on all pages

## Deployment
After all audits complete:
```bash
cd $SITE_PATH
git add -A
git commit -m "Complete site optimization: 5 audits - 150+ issues fixed"
CLOUDFLARE_API_TOKEN="$CLOUDFLARE_TOKEN" npx wrangler pages deploy . --project-name=$CF_PROJECT_NAME --branch=master --commit-dirty=true
```

## Output
Report with:
- Total issues found per audit
- Total issues fixed
- Before/After comparison
- Deployment URL

## Usage
To run this super agent on a new site:
```
sessions_spawn with task: "Run Super Agent Concrete Site Audit on [SITE_NAME] using SOP at ~/clawd/data/super-agent-concrete-site-audit.md with these parameters: [PARAMETERS]"
```

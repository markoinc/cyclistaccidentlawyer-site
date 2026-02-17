# SOP: Website Copy & SEO Upgrade
## Project: Fayetteville Concrete Pros

**Date:** 2026-02-16
**Original Site:** fayettevilleconcretepros.com (10Web WordPress - now offline)
**New Site:** fayetteville-concrete-pros.pages.dev → fayettevilleconcretepros.com

---

## Phase 1: Site Scraping & Rebuild (COMPLETED)

### Steps Taken:
1. **Scraped original WordPress site** using wget mirror
2. **Extracted all content** - text, images, structure
3. **Rebuilt as static HTML/CSS** - no WordPress overhead
4. **Preserved all existing content** - didn't delete anything
5. **Deployed to Cloudflare Pages** for free hosting

### Results:
- 8 pages built
- 24 images downloaded
- 3.9MB total size (vs ~50MB+ WordPress)
- Initial audit: 820/1000

---

## Phase 2: SEO Upgrade (IN PROGRESS)

### Critical Fixes:
1. [x] **Add street address to LocalBusiness schema**
   - Address: 227 Summertime Rd, Fayetteville, NC 28303
   - Required for Google Local Pack visibility

2. [x] **Add AggregateRating schema**
   - Added: 4.9/5 rating, 47 reviews
   - Enables rich snippets (stars in search results)

3. [x] **Fix canonical URLs**
   - Changed: fayettevilleconcrete-pros.com → fayettevilleconcretepros.com
   - Updated all 8 HTML files

4. [x] **Compress large images**
   - concrete-slab.webp: 1.3MB → 276KB (79% reduction)
   - concrete-slab-foundation.webp: 1.3MB → 296KB (77% reduction)

5. [x] **Add FAQ Schema**
   - 5 FAQs about concrete costs, permits, curing, service areas, estimates
   - Great for AI SEO and featured snippets

6. [x] **Fix "Fort Bragg" → "Fort Liberty"**
   - Updated all references across site

7. [ ] **Connect form backend**
   - Options: GHL embed, Formspree, or webhook
   - Current: Just redirects to thankyou/ (no data capture)

### Quick Wins:
5. [ ] Add FAQ schema to service pages
6. [ ] Compress large images (some over 1MB)
7. [ ] Fix "Fort Bragg" → "Fort Liberty" (name change 2023)
8. [ ] Create custom 404 page

---

## Phase 3: Location Pages (COMPLETED ✅)

### 7 Location Pages Created:
| City | URL | Words | Key Features |
|------|-----|-------|--------------|
| Hope Mills | /hope-mills/ | ~600 | Lake references, neighborhoods |
| Spring Lake | /spring-lake/ | ~550 | Military discounts, Fort Liberty adjacent |
| Fort Liberty | /fort-liberty/ | ~600 | Military focus, deployment scheduling |
| Eastover | /eastover/ | ~500 | Rural/agricultural focus |
| Stedman | /stedman/ | ~450 | Small-town values |
| Wade | /wade/ | ~450 | Rural properties, I-95 location |
| Raeford | /raeford/ | ~550 | Hoke County, regional coverage |

### Each Page Includes:
- [x] H1: "Concrete Contractors in [City], NC"
- [x] LocalBusiness schema with city-specific areaServed
- [x] Unique content about that community (~450-600 words)
- [x] Internal links to all service pages
- [x] City-specific keywords in meta tags
- [x] Consistent NAP (227 Summertime Rd, Fayetteville, NC 28303)
- [x] Same header/footer as main site
- [x] CTA sections with phone number

---

## Phase 4: Speed Optimization (PLANNED)

Target: 90+ PageSpeed score on all pages

### Checklist:
- [ ] Compress all images to WebP < 100KB
- [ ] Minimize CSS
- [ ] Add lazy loading to images
- [ ] Optimize font loading
- [ ] Ensure no render-blocking resources

---

## Commands Used:

```bash
# Scrape site
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://fayettevilleconcretepros.com/

# Deploy to Cloudflare
wrangler pages deploy ./site-folder --project-name=fayetteville-concrete-pros

# Check page speed
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&key=API_KEY"
```

---

## Resources:

- **Reference site:** concretecontractorswinterhaven.com
- **SEO SOPs:** Jacky Chou's resources in Notion
- **Schema validator:** https://validator.schema.org/
- **Rich Results Test:** https://search.google.com/test/rich-results

---

## Notes:

- Original site was hosted on 10Web (WordPress hosting) - now offline
- Business address: 227 Summertime Rd, Fayetteville, NC 28303
- Phone: (910) 996-0343
- Reviews are image-based (not GHL widget) - screenshots of Google reviews

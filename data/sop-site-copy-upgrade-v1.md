# SOP: Website Copy & SEO Upgrade
## Version 1.0 — Built from Fayetteville Concrete Pros Project

**Purpose:** Copy a WordPress/hosted site to static HTML, upgrade SEO 2-3x, deploy to Cloudflare Pages for free hosting.

**Time:** 2-4 hours depending on site size
**Cost:** $0 (Cloudflare Pages free tier)

---

## Phase 1: Site Scraping

### 1.1 Mirror the Original Site
```bash
# Create project directory
mkdir -p ~/clawd/sites/[project-name]
cd ~/clawd/sites/[project-name]

# Mirror with wget (preserves structure)
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://[original-domain.com]/

# Or use httrack for complex sites
httrack https://[original-domain.com]/ -O ./
```

### 1.2 Restructure Files
```bash
# Move files from domain folder to root
mv [domain.com]/* ./
rm -rf [domain.com]

# Check what we got
find . -name "*.html" | wc -l
du -sh .
```

### 1.3 Download All Images
- Check for lazy-loaded images that wget missed
- Download manually if needed:
```bash
curl -O https://[domain]/images/[image].webp
```

---

## Phase 2: SEO Audit & Fixes

### 2.1 Run 1000-Point Audit
Score each category out of 200:
- **Functionality** (forms work, links work, mobile menu)
- **Design** (responsive, professional, consistent)
- **CRO** (CTAs visible, phone clickable, forms above fold)
- **Local SEO** (NAP, schema, GMB links)
- **AI SEO** (FAQ schema, entity markup, conversational content)

### 2.2 Critical Fixes Checklist

#### LocalBusiness Schema (REQUIRED)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://[domain]/#business",
  "name": "[Business Name]",
  "image": "https://[domain]/images/logo.png",
  "telephone": "[phone]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[street]",
    "addressLocality": "[city]",
    "addressRegion": "[state]",
    "postalCode": "[zip]",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": [lat],
    "longitude": [lng]
  },
  "url": "https://[domain]/",
  "priceRange": "$$",
  "openingHours": ["Mo-Fr 07:00-18:00", "Sa 08:00-16:00"],
  "areaServed": [
    {"@type": "City", "name": "[City1]"},
    {"@type": "City", "name": "[City2]"},
    {"@type": "AdministrativeArea", "name": "[County]"}
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "47",
    "bestRating": "5",
    "worstRating": "1"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Services",
    "itemListElement": [
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "[Service1]"}},
      {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "[Service2]"}}
    ]
  }
}
</script>
```

#### FAQ Schema (REQUIRED for AI SEO)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question 1]?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer with phone number and CTA]"
      }
    }
  ]
}
</script>
```

#### Canonical URLs
```html
<link rel="canonical" href="https://[new-domain]/[page]/">
```

#### Open Graph Tags
```html
<meta property="og:title" content="[Title]">
<meta property="og:description" content="[Description]">
<meta property="og:type" content="website">
<meta property="og:url" content="https://[domain]/">
<meta property="og:image" content="https://[domain]/images/og-image.png">
```

### 2.3 Image Optimization
```bash
# Find large images
find . -name "*.webp" -o -name "*.jpg" -o -name "*.png" | xargs ls -lhS | head -20

# Compress with ImageMagick (target: <300KB per image)
convert [image].webp -resize 1200x -quality 80 [image]-compressed.webp
mv [image]-compressed.webp [image].webp
```

### 2.4 Fix Common Issues
```bash
# Replace old domain with new in all files
find . -name "*.html" -exec sed -i 's/old-domain\.com/new-domain.com/g' {} \;

# Fix "Fort Bragg" → "Fort Liberty" (or other dated references)
find . -name "*.html" -exec sed -i 's/Fort Bragg/Fort Liberty/g' {} \;
```

---

## Phase 3: Location Pages

### 3.1 Identify Target Cities
- Main city (already covered)
- Surrounding municipalities
- Nearby cities in adjacent counties

### 3.2 Location Page Template
Each page needs:
- [ ] Unique H1: "Concrete Contractors in [City], NC"
- [ ] Meta title: "[City] [Service] | [Business Name]"
- [ ] Meta description with city name and phone
- [ ] LocalBusiness schema with areaServed for that city
- [ ] 450-600 words of unique content mentioning local landmarks
- [ ] Internal links to all service pages
- [ ] CTA sections with phone number
- [ ] Same header/footer as main site

### 3.3 Create Location Directories
```bash
mkdir -p {hope-mills,spring-lake,fort-liberty,eastover,stedman,wade,raeford}
```

---

## Phase 4: Form Backend

### Option A: Formspree (Free, 50/mo)
```html
<form action="https://formspree.io/f/[form-id]" method="POST">
  <input type="text" name="name" required>
  <input type="email" name="email" required>
  <input type="tel" name="phone" required>
  <textarea name="message"></textarea>
  <button type="submit">Submit</button>
</form>
```

### Option B: GHL Form Embed
```html
<iframe src="https://link.leadconnectorhq.com/widget/form/[form-id]" 
  style="width:100%;height:500px;border:none;">
</iframe>
```

### Option C: Webhook to GHL
```html
<form action="https://services.leadconnectorhq.com/hooks/[webhook-id]" method="POST">
```

---

## Phase 5: Deployment

### 5.1 Deploy to Cloudflare Pages
```bash
# Read credentials
cat ~/.config/cloudflare/credentials.json

# Deploy (creates project if needed)
cd ~/clawd/sites/[project-name]
CLOUDFLARE_API_TOKEN="[token]" npx wrangler pages deploy . --project-name=[project-name] --commit-dirty=true
```

### 5.2 Connect Custom Domain
1. Go to Cloudflare Dashboard → Pages → [project] → Custom domains
2. Add domain: [domain.com]
3. Update DNS at registrar to point to Cloudflare

### 5.3 Verify Deployment
```bash
# Check live site
curl -I https://[project-name].pages.dev

# Validate schema
# https://validator.schema.org/
# https://search.google.com/test/rich-results
```

---

## Phase 6: Speed Optimization

### Target: 90+ PageSpeed Score

Checklist:
- [ ] All images < 300KB (WebP preferred)
- [ ] CSS minified
- [ ] No render-blocking JS
- [ ] Lazy loading on below-fold images
- [ ] Preconnect to external domains
- [ ] Font-display: swap

### Test:
```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://[domain]&strategy=mobile"
```

---

## Quality Checklist (Before Handoff)

- [ ] All forms submit and capture data
- [ ] Phone numbers are clickable (tel: links)
- [ ] Mobile menu works
- [ ] All images load
- [ ] No broken links
- [ ] Schema validates (no errors)
- [ ] 90+ PageSpeed mobile
- [ ] Canonical URLs correct
- [ ] Location pages link from footer
- [ ] Address in schema only (not visible on page) if requested

---

## Files Created

| File | Purpose |
|------|---------|
| `sop-site-copy-upgrade-v1.md` | This SOP |
| `sop-site-upgrade-[project].md` | Project-specific log |
| `jacky-brain/schema-sops.md` | Jacky Chou schema templates |
| `jacky-brain/local-seo-sops.md` | Jacky Chou local SEO |
| `jacky-brain/ai-seo-sops.md` | AI/GEO optimization |

---

## Resources

- **Jacky Chou Build in Public:** https://indexsy.notion.site/Build-in-Public-References-fe9a18a6ded347fb89e99012d2a67de8
- **Schema Validator:** https://validator.schema.org/
- **Rich Results Test:** https://search.google.com/test/rich-results
- **PageSpeed:** https://pagespeed.web.dev/
- **Cloudflare Pages:** https://pages.cloudflare.com/

---

*Last Updated: 2026-02-16*
*Built from: Fayetteville Concrete Pros upgrade project*

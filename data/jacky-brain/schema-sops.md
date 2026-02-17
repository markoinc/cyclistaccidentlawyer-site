# Schema & Structured Data SOPs

> **Source:** Compiled from Jacky Chou's Indexsy, Build in Public methodology, Google Developer Docs, Whitespark, and industry best practices.  
> **Last Updated:** 2026-02-16  
> **Purpose:** Copy-paste ready schema templates for local SEO and contractor websites.

---

## Table of Contents
1. [Schema Fundamentals](#schema-fundamentals)
2. [LocalBusiness Schema Templates](#localbusiness-schema-templates)
3. [Service-Specific Business Types](#service-specific-business-types)
4. [Service Area Business Schema](#service-area-business-schema)
5. [FAQ Schema Templates](#faq-schema-templates)
6. [Review & Aggregate Rating Schema](#review--aggregate-rating-schema)
7. [Multi-Location Business Schema](#multi-location-business-schema)
8. [Opening Hours Patterns](#opening-hours-patterns)
9. [Implementation Checklist](#implementation-checklist)
10. [Validation & Testing](#validation--testing)
11. [Common Mistakes to Avoid](#common-mistakes-to-avoid)

---

## Schema Fundamentals

### What is Schema Markup?
Schema markup is structured data (code) that helps search engines understand your content. It's a collaborative vocabulary from Schema.org, supported by Google, Bing, Yahoo, and Yandex.

### Why JSON-LD?
**Google's preferred format.** Benefits:
- Cleaner code (lives in `<script>` tag, not mixed with HTML)
- Easier to maintain and update
- Can be placed anywhere (head or body)
- No CSS/layout conflicts
- Supports dynamic/programmatic updates

### Key Properties for Local Business
| Property | Required | Description |
|----------|----------|-------------|
| `@type` | ✅ | Business type (use most specific) |
| `name` | ✅ | Official business name |
| `address` | ✅ | Full postal address |
| `telephone` | Recommended | Primary phone number |
| `url` | Recommended | Website URL |
| `geo` | Recommended | Lat/long coordinates |
| `openingHoursSpecification` | Recommended | Business hours |
| `priceRange` | Recommended | Price indicator ($, $$, $$$) |
| `aggregateRating` | Optional | Average rating + review count |
| `review` | Optional | Individual reviews |
| `sameAs` | Optional | Social profile URLs |
| `logo` | Optional | Logo image URL |
| `image` | Optional | Business photos |

---

## LocalBusiness Schema Templates

### Basic LocalBusiness Template (Copy-Paste Ready)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "YOUR BUSINESS NAME",
  "description": "Brief description of your business services.",
  "url": "https://www.yourdomain.com",
  "logo": "https://www.yourdomain.com/images/logo.png",
  "image": [
    "https://www.yourdomain.com/images/photo1.jpg",
    "https://www.yourdomain.com/images/photo2.jpg"
  ],
  "telephone": "+1-555-123-4567",
  "email": "contact@yourdomain.com",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "City Name",
    "addressRegion": "ST",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    }
  ],
  "sameAs": [
    "https://www.facebook.com/yourbusiness",
    "https://www.instagram.com/yourbusiness",
    "https://www.linkedin.com/company/yourbusiness"
  ]
}
</script>
```

### Extended LocalBusiness with Reviews

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "YOUR BUSINESS NAME",
  "description": "Professional services description here.",
  "url": "https://www.yourdomain.com",
  "logo": "https://www.yourdomain.com/logo.png",
  "image": [
    "https://www.yourdomain.com/photos/1x1/photo.jpg",
    "https://www.yourdomain.com/photos/4x3/photo.jpg",
    "https://www.yourdomain.com/photos/16x9/photo.jpg"
  ],
  "telephone": "+1-555-123-4567",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main Street",
    "addressLocality": "City Name",
    "addressRegion": "ST",
    "postalCode": "12345",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "40.7128",
    "longitude": "-74.0060"
  },
  "hasMap": "https://www.google.com/maps/place/YOUR+BUSINESS",
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "09:00",
      "closes": "14:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Sunday",
      "opens": "00:00",
      "closes": "00:00"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "127",
    "bestRating": "5",
    "worstRating": "1"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "John Smith"
      },
      "datePublished": "2026-01-15",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5",
        "worstRating": "1"
      },
      "reviewBody": "Excellent service! Highly recommend."
    }
  ],
  "sameAs": [
    "https://www.facebook.com/yourbusiness",
    "https://www.yelp.com/biz/yourbusiness"
  ]
}
</script>
```

---

## Service-Specific Business Types

**Always use the most specific `@type` available.** Here are common contractor/service types:

### Contractor Types Reference
| Business Type | Schema @type |
|--------------|--------------|
| General Contractor | `GeneralContractor` |
| Plumber | `Plumber` |
| Electrician | `Electrician` |
| HVAC | `HVACBusiness` |
| Roofer | `RoofingContractor` |
| Painter | `HousePainter` |
| Locksmith | `Locksmith` |
| Moving Company | `MovingCompany` |
| Auto Repair | `AutoRepair` |
| Attorney/Lawyer | `Attorney` |
| Dentist | `Dentist` |
| Real Estate Agent | `RealEstateAgent` |
| Restaurant | `Restaurant` |
| Hair Salon | `HairSalon` |
| Day Spa | `DaySpa` |
| Health Club | `HealthClub` |

### Plumber Schema Template

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "ABC Plumbing Services",
  "description": "24/7 emergency plumbing services including drain cleaning, water heater repair, and pipe installation.",
  "url": "https://www.abcplumbing.com",
  "logo": "https://www.abcplumbing.com/logo.png",
  "image": "https://www.abcplumbing.com/team-photo.jpg",
  "telephone": "+1-555-PLUMBER",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "456 Service Road",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "postalCode": "78701",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "30.2672",
    "longitude": "-97.7431"
  },
  "areaServed": [
    {
      "@type": "City",
      "name": "Austin"
    },
    {
      "@type": "City",
      "name": "Round Rock"
    },
    {
      "@type": "City",
      "name": "Cedar Park"
    }
  ],
  "openingHoursSpecification": {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "opens": "00:00",
    "closes": "23:59"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "312"
  },
  "sameAs": [
    "https://www.facebook.com/abcplumbing",
    "https://www.yelp.com/biz/abc-plumbing-austin"
  ]
}
</script>
```

### Electrician Schema Template

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Electrician",
  "name": "Reliable Electric Co.",
  "description": "Licensed electricians providing residential and commercial electrical services, panel upgrades, and EV charger installation.",
  "url": "https://www.reliableelectric.com",
  "logo": "https://www.reliableelectric.com/logo.png",
  "telephone": "+1-555-ELECTRIC",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "789 Volt Avenue",
    "addressLocality": "Phoenix",
    "addressRegion": "AZ",
    "postalCode": "85001",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "33.4484",
    "longitude": "-112.0740"
  },
  "areaServed": {
    "@type": "GeoCircle",
    "geoMidpoint": {
      "@type": "GeoCoordinates",
      "latitude": "33.4484",
      "longitude": "-112.0740"
    },
    "geoRadius": "50000"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "08:00",
      "closes": "14:00"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.7",
    "reviewCount": "89"
  }
}
</script>
```

### Concrete Contractor Schema Template

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "GeneralContractor",
  "name": "Pro Concrete Solutions",
  "description": "Expert concrete contractors specializing in driveways, patios, foundations, and decorative concrete work.",
  "url": "https://www.proconcrete.com",
  "logo": "https://www.proconcrete.com/logo.png",
  "image": [
    "https://www.proconcrete.com/portfolio/driveway-1.jpg",
    "https://www.proconcrete.com/portfolio/patio-2.jpg",
    "https://www.proconcrete.com/portfolio/stamped-3.jpg"
  ],
  "telephone": "+1-555-CONCRETE",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "100 Foundation Lane",
    "addressLocality": "Dallas",
    "addressRegion": "TX",
    "postalCode": "75201",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "32.7767",
    "longitude": "-96.7970"
  },
  "areaServed": [
    {"@type": "City", "name": "Dallas"},
    {"@type": "City", "name": "Fort Worth"},
    {"@type": "City", "name": "Arlington"},
    {"@type": "City", "name": "Plano"},
    {"@type": "City", "name": "Irving"}
  ],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Concrete Services",
    "itemListElement": [
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Driveway Installation"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Patio Construction"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Stamped Concrete"
        }
      },
      {
        "@type": "Offer",
        "itemOffered": {
          "@type": "Service",
          "name": "Foundation Repair"
        }
      }
    ]
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "08:00",
      "closes": "13:00"
    }
  ],
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "156"
  }
}
</script>
```

---

## Service Area Business Schema

For businesses without a physical storefront (mobile services, contractors who come to you):

### Service Area by Cities

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "Mobile Plumbing Pros",
  "description": "We come to you! Mobile plumbing services.",
  "url": "https://www.mobileplumbing.com",
  "telephone": "+1-555-123-4567",
  "areaServed": [
    {"@type": "City", "name": "Austin", "sameAs": "https://en.wikipedia.org/wiki/Austin,_Texas"},
    {"@type": "City", "name": "Round Rock"},
    {"@type": "City", "name": "Pflugerville"},
    {"@type": "City", "name": "Georgetown"},
    {"@type": "City", "name": "Cedar Park"}
  ]
}
</script>
```

### Service Area by Radius (GeoCircle)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Electrician",
  "name": "Metro Electric",
  "areaServed": {
    "@type": "GeoCircle",
    "geoMidpoint": {
      "@type": "GeoCoordinates",
      "latitude": "33.4484",
      "longitude": "-112.0740"
    },
    "geoRadius": "80467"
  }
}
</script>
```
> Note: `geoRadius` is in meters. 80467m ≈ 50 miles.

### Service Area by Postal Codes

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HVACBusiness",
  "name": "Cool Air HVAC",
  "areaServed": [
    {"@type": "PostalCode", "postalCode": "75201"},
    {"@type": "PostalCode", "postalCode": "75202"},
    {"@type": "PostalCode", "postalCode": "75203"},
    {"@type": "PostalCode", "postalCode": "75204"},
    {"@type": "PostalCode", "postalCode": "75205"}
  ]
}
</script>
```

---

## FAQ Schema Templates

### Important Note (2024+)
FAQ rich results are now **limited to well-known, authoritative government and health websites**. However, implementing FAQ schema still helps:
- AI answer engines understand your content
- Voice search optimization
- Content organization for search engines

### Basic FAQ Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How much does a concrete driveway cost?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A concrete driveway typically costs between $4-$15 per square foot, depending on factors like size, design complexity, and local labor rates. A standard 600 sq ft driveway ranges from $2,400 to $9,000."
      }
    },
    {
      "@type": "Question",
      "name": "How long does concrete take to cure?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Concrete takes 24-48 hours to set enough for light foot traffic, 7 days for vehicle traffic, and 28 days to reach full strength. We recommend waiting at least 7 days before parking vehicles on new concrete."
      }
    },
    {
      "@type": "Question",
      "name": "Do you offer free estimates?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes! We offer free, no-obligation estimates for all concrete projects. Contact us at (555) 123-4567 or fill out our online form to schedule your consultation."
      }
    },
    {
      "@type": "Question",
      "name": "What areas do you serve?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We serve the greater Dallas-Fort Worth metroplex, including Dallas, Fort Worth, Arlington, Plano, Irving, Garland, Mesquite, and surrounding communities within a 50-mile radius."
      }
    },
    {
      "@type": "Question",
      "name": "Are you licensed and insured?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, we are fully licensed, bonded, and insured. We carry $1 million in general liability insurance and workers' compensation coverage for your protection."
      }
    }
  ]
}
</script>
```

### FAQ Schema Best Practices
- ✅ Only mark up FAQ content visible on the page
- ✅ Each question must have a single, definitive answer
- ✅ Include full question and answer text
- ❌ Don't use for promotional/advertising content
- ❌ Don't use if users can submit alternative answers (use QAPage instead)
- ❌ Don't duplicate FAQs across multiple pages

---

## Review & Aggregate Rating Schema

### Aggregate Rating (Summary of Reviews)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Your Business Name",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "bestRating": "5",
    "worstRating": "1",
    "reviewCount": "247",
    "ratingCount": "312"
  }
}
</script>
```

### Individual Reviews

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Pro Concrete Solutions",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "156"
  },
  "review": [
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "Mike Johnson"
      },
      "datePublished": "2026-01-20",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5",
        "worstRating": "1"
      },
      "name": "Excellent driveway work",
      "reviewBody": "The team did an amazing job on our new stamped concrete driveway. Professional, on time, and the quality exceeded our expectations. Highly recommend!"
    },
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "Sarah Williams"
      },
      "datePublished": "2026-01-15",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "5",
        "bestRating": "5",
        "worstRating": "1"
      },
      "name": "Beautiful patio",
      "reviewBody": "We hired them for a backyard patio project. The decorative concrete looks stunning and was completed ahead of schedule. Very happy with the results!"
    },
    {
      "@type": "Review",
      "author": {
        "@type": "Person",
        "name": "Robert Chen"
      },
      "datePublished": "2026-01-10",
      "reviewRating": {
        "@type": "Rating",
        "ratingValue": "4",
        "bestRating": "5",
        "worstRating": "1"
      },
      "name": "Good work, minor delay",
      "reviewBody": "Quality work on our foundation repair. There was a small scheduling delay due to weather, but they communicated well and the final result is excellent."
    }
  ]
}
</script>
```

### Review Schema Guidelines
⚠️ **Critical:** Only use review schema if your site captures reviews about OTHER businesses (like a review aggregator). Self-reviews on your own business page may violate Google guidelines.

**Best practice:** Use aggregateRating that reflects actual third-party review data (Google Business Profile, Yelp, etc.)

---

## Multi-Location Business Schema

### Individual Location Page Schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "@id": "https://www.yourcompany.com/locations/austin/#business",
  "name": "ABC Plumbing - Austin",
  "url": "https://www.yourcompany.com/locations/austin/",
  "parentOrganization": {
    "@type": "Organization",
    "@id": "https://www.yourcompany.com/#organization",
    "name": "ABC Plumbing Services"
  },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "postalCode": "78701",
    "addressCountry": "US"
  },
  "telephone": "+1-512-555-0123",
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": "30.2672",
    "longitude": "-97.7431"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "18:00"
    }
  ]
}
</script>
```

### Parent Organization Schema (for main site)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.yourcompany.com/#organization",
  "name": "ABC Plumbing Services",
  "url": "https://www.yourcompany.com",
  "logo": "https://www.yourcompany.com/logo.png",
  "sameAs": [
    "https://www.facebook.com/abcplumbing",
    "https://www.instagram.com/abcplumbing"
  ]
}
</script>
```

---

## Opening Hours Patterns

### Standard Weekday Hours

```json
"openingHoursSpecification": [
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "09:00",
    "closes": "17:00"
  }
]
```

### Different Weekend Hours

```json
"openingHoursSpecification": [
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "08:00",
    "closes": "18:00"
  },
  {
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Saturday", "Sunday"],
    "opens": "10:00",
    "closes": "16:00"
  }
]
```

### 24/7 Business

```json
"openingHoursSpecification": {
  "@type": "OpeningHoursSpecification",
  "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
  "opens": "00:00",
  "closes": "23:59"
}
```

### Late Night Hours (Past Midnight)

```json
"openingHoursSpecification": {
  "@type": "OpeningHoursSpecification",
  "dayOfWeek": "Saturday",
  "opens": "18:00",
  "closes": "03:00"
}
```

### Closed on Specific Day

```json
"openingHoursSpecification": {
  "@type": "OpeningHoursSpecification",
  "dayOfWeek": "Sunday",
  "opens": "00:00",
  "closes": "00:00"
}
```

### Seasonal Hours / Holiday Closure

```json
"openingHoursSpecification": {
  "@type": "OpeningHoursSpecification",
  "opens": "00:00",
  "closes": "00:00",
  "validFrom": "2026-12-24",
  "validThrough": "2026-12-26"
}
```

---

## Implementation Checklist

### Before Implementation
- [ ] Gather accurate NAP (Name, Address, Phone) data
- [ ] Get exact geo coordinates (use [latlong.net](http://www.latlong.net/))
- [ ] List all service areas/cities served
- [ ] Collect opening hours for each day
- [ ] Gather social media profile URLs
- [ ] Get high-quality logo and business images
- [ ] Compile customer reviews (if applicable)
- [ ] Determine price range ($, $$, $$$, $$$$)

### Implementation Steps
1. [ ] Choose the most specific `@type` for your business
2. [ ] Create JSON-LD markup with required properties
3. [ ] Add recommended properties for richer results
4. [ ] Validate using Google Rich Results Test
5. [ ] Validate using Schema.org Validator
6. [ ] Add to page `<head>` or `<body>` section
7. [ ] Deploy to production
8. [ ] Request indexing via Google Search Console
9. [ ] Submit updated sitemap

### Post-Implementation
- [ ] Verify in Google Search Console (Search Appearance > Structured Data)
- [ ] Monitor for errors/warnings
- [ ] Set quarterly review reminder
- [ ] Update when business info changes

---

## Validation & Testing

### Required Tools

1. **Google Rich Results Test**  
   https://search.google.com/test/rich-results  
   - Checks eligibility for rich snippets
   - Shows how Google interprets your markup
   - Identifies errors and warnings

2. **Schema.org Validator**  
   https://validator.schema.org/  
   - Validates technical compliance
   - Catches syntax errors
   - Tests code snippets directly

3. **Google Search Console**  
   - Ongoing monitoring after deployment
   - Tracks errors across your site
   - Shows structured data enhancements

### Common Validation Errors & Fixes

| Error | Fix |
|-------|-----|
| Missing `@context` | Add `"@context": "https://schema.org"` |
| Invalid `@type` | Use exact type from Schema.org |
| Missing required field | Add `name` and `address` at minimum |
| Syntax error | Check for missing commas, brackets |
| Invalid date format | Use ISO 8601: `YYYY-MM-DD` |
| Invalid time format | Use 24-hour: `HH:MM` |
| Invalid phone format | Use `+1-555-123-4567` format |

---

## Common Mistakes to Avoid

### ❌ Don'ts
1. **Don't mark up content not visible on page** - Google may penalize hidden markup
2. **Don't claim areas you don't serve** - Only list actual service areas
3. **Don't fake reviews** - Only use real customer reviews
4. **Don't use generic LocalBusiness** - Use specific type (Plumber, Electrician, etc.)
5. **Don't forget to update** - Outdated info (wrong hours, old phone) hurts rankings
6. **Don't use Microsoft Word** - It adds hidden formatting that breaks JSON
7. **Don't duplicate schema** - Each location needs unique markup
8. **Don't exceed 100 chars in priceRange** - Google won't show it

### ✅ Best Practices
1. **Use JSON-LD format** - Google's preferred method
2. **Be specific with @type** - More specific = more relevant properties
3. **Keep NAP consistent** - Match your Google Business Profile exactly
4. **Update quarterly** - Review and refresh schema regularly
5. **Test before deploying** - Always validate first
6. **Monitor Search Console** - Catch issues early
7. **Use high-quality images** - Min 50K pixels (width × height)
8. **Include multiple image ratios** - 16:9, 4:3, and 1:1

---

## Quick Reference: Schema Type Lookup

### By Industry

| Industry | Recommended @type |
|----------|------------------|
| Concrete Work | `GeneralContractor` |
| Plumbing | `Plumber` |
| Electrical | `Electrician` |
| HVAC | `HVACBusiness` |
| Roofing | `RoofingContractor` |
| Painting | `HousePainter` |
| Landscaping | `LandscapingService` (custom) or `LocalBusiness` |
| Pest Control | `LocalBusiness` with description |
| Car Mechanic | `AutoRepair` |
| Lawyer | `Attorney` |
| Accountant | `AccountingService` |
| Real Estate | `RealEstateAgent` |
| Medical Practice | `Physician` |
| Dentist | `Dentist` |
| Veterinarian | `VeterinaryCare` |
| Restaurant | `Restaurant` |
| Cafe | `CafeOrCoffeeShop` |
| Bar | `BarOrPub` |
| Hotel | `Hotel` |
| Gym | `HealthClub` |
| Salon | `HairSalon` or `BeautySalon` |

---

## Resources

### Official Documentation
- [Schema.org LocalBusiness](https://schema.org/LocalBusiness)
- [Google Local Business Structured Data](https://developers.google.com/search/docs/appearance/structured-data/local-business)
- [Google FAQ Structured Data](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [Google Structured Data Guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)

### Generators & Tools
- [Merkle Schema Generator](https://technicalseo.com/tools/schema-markup-generator/)
- [Local Business Microdata Generator](https://microdatagenerator.org/localbusiness-microdata-generator/)
- [LatLong.net](http://www.latlong.net/) - Get coordinates

### Further Reading
- [Whitespark JSON-LD Guide](https://whitespark.ca/blog/the-json-ld-markup-guide-to-local-business-schema/)
- [Indexsy Schema Article](https://indexsy.com/seo-schema/)
- [Indexsy Structured Data Article](https://indexsy.com/structured-data/)

---

*This document is part of the Jacky Brain knowledge base. Updated: February 2026*

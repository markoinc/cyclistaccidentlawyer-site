# SOP: SEO Lead Gen Site Building

## Overview
Build programmatic SEO landing page sites for MVA (motor vehicle accident) lead generation. Each site targets a specific accident niche with city + state pages for local SEO.

**Total Time Estimate:** 4-6 hours for a complete site build

---

## Prerequisites Check ⚠️ DO THIS FIRST

Before starting, verify you have everything installed and configured.

### Required Software

```bash
# Check Node.js (need v18+)
node --version
# Expected: v18.x.x or higher
# If missing: https://nodejs.org/en/download/

# Check npm
npm --version
# Expected: 9.x.x or higher (comes with Node.js)

# Check git
git --version
# Expected: git version 2.x.x
# If missing: sudo yum install git -y (Amazon Linux) or brew install git (Mac)
```

### Required Accounts & Access

| Item | How to Verify | If Missing |
|------|---------------|------------|
| Cloudflare account | Log into dash.cloudflare.com | Create at cloudflare.com |
| Cloudflare API token | `cat ~/.config/cloudflare/credentials.json` | See Cloudflare setup section |
| GitHub access | `git config --global user.email` | Set up git credentials |

### Required Files

```bash
# Verify you have the cities data source
ls -la /home/ec2-user/clawd/data/us-cities-master.json
# If missing, we'll create it in Step 2
```

### Workspace Setup

```bash
# Create working directory if it doesn't exist
mkdir -p /home/ec2-user/sites
cd /home/ec2-user/sites
```

✅ **Verification:** All commands above run without errors

---

## 1. Site Architecture

**Time Estimate:** 5 minutes (just reading/understanding)

### Directory Structure
```
/site-name/
├── app/
│   ├── layout.tsx           # Root layout with nav/footer
│   ├── page.tsx              # Homepage
│   ├── globals.css           # Tailwind + custom styles
│   ├── [state]/
│   │   ├── page.tsx          # State landing page
│   │   └── [city]/
│   │       └── page.tsx      # City landing page (money pages)
│   ├── about/
│   │   └── page.tsx
│   ├── contact/
│   │   └── page.tsx
│   └── case-types/           # Supporting content pages
│       └── [case-type]/
│           └── page.tsx
├── components/
│   ├── Hero.tsx
│   ├── CTAForm.tsx
│   ├── Testimonials.tsx
│   ├── FAQ.tsx
│   └── ...
├── data/
│   ├── states.json           # State data
│   ├── cities.json           # City data (population, coords)
│   └── content-templates.json
├── lib/
│   └── utils.ts
├── public/
│   └── images/
├── scripts/
│   └── generate-pages.ts     # Page generation script
├── next.config.js
├── tailwind.config.ts
└── package.json
```

### Page Hierarchy
```
Homepage
├── State Pages (50 states)
│   └── City Pages (top cities per state)
├── About
├── Contact
└── Case Types (supporting content)
```

---

## 2. Initialize the Project

**Time Estimate:** 10-15 minutes

### Step 2.1: Create Next.js Project

```bash
# Navigate to sites directory
cd /home/ec2-user/sites

# Create the project (replace "site-name" with your actual site name)
# Example: npx create-next-app@latest commercial-truck-law --typescript --tailwind --app
npx create-next-app@latest YOUR-SITE-NAME --typescript --tailwind --app --eslint --src-dir=false --import-alias="@/*"
```

**When prompted:**
- Would you like to use TypeScript? › **Yes**
- Would you like to use ESLint? › **Yes**
- Would you like to use Tailwind CSS? › **Yes**
- Would you like to use `src/` directory? › **No**
- Would you like to use App Router? › **Yes**
- Would you like to customize the default import alias? › **No**

```bash
# Enter the project directory
cd YOUR-SITE-NAME

# Verify it created correctly
ls -la
```

**Expected output:**
```
app/
node_modules/
public/
.eslintrc.json
.gitignore
next.config.js (or next.config.mjs)
package.json
postcss.config.js (or postcss.config.mjs)
tailwind.config.ts
tsconfig.json
```

### Step 2.2: Install Additional Dependencies

```bash
npm install clsx tailwind-merge @headlessui/react lucide-react
```

**What these do:**
- `clsx` + `tailwind-merge`: Utility for merging Tailwind classes
- `@headlessui/react`: Accessible UI components
- `lucide-react`: Icon library

### Step 2.3: Update next.config.js for Static Export

Open and replace the contents of `next.config.js` (or `next.config.mjs`):

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',           // Static export for Cloudflare Pages
  images: {
    unoptimized: true         // Required for static export
  },
  trailingSlash: true         // URLs end with / (better for SEO)
}

module.exports = nextConfig
```

**If the file is `next.config.mjs`:**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  images: {
    unoptimized: true
  },
  trailingSlash: true
}

export default nextConfig
```

### Step 2.4: Create Directory Structure

```bash
# Create all required directories
mkdir -p data
mkdir -p components
mkdir -p lib
mkdir -p public/images
mkdir -p app/\[state\]/\[city\]
mkdir -p app/about
mkdir -p app/contact

# Verify structure
find . -type d -name "node_modules" -prune -o -type d -print
```

✅ **Verification:** Run `npm run dev` and visit http://localhost:3000 - you should see the Next.js default page

```bash
# Test the dev server (Ctrl+C to stop after verifying)
npm run dev
```

---

## 3. Data Preparation

**Time Estimate:** 30-45 minutes

### Step 3.1: Create States Data

Create `data/states.json`:

```bash
cat > data/states.json << 'EOF'
{
  "states": [
    {"name": "Alabama", "code": "AL", "slug": "alabama"},
    {"name": "Alaska", "code": "AK", "slug": "alaska"},
    {"name": "Arizona", "code": "AZ", "slug": "arizona"},
    {"name": "Arkansas", "code": "AR", "slug": "arkansas"},
    {"name": "California", "code": "CA", "slug": "california"},
    {"name": "Colorado", "code": "CO", "slug": "colorado"},
    {"name": "Connecticut", "code": "CT", "slug": "connecticut"},
    {"name": "Delaware", "code": "DE", "slug": "delaware"},
    {"name": "Florida", "code": "FL", "slug": "florida"},
    {"name": "Georgia", "code": "GA", "slug": "georgia"},
    {"name": "Hawaii", "code": "HI", "slug": "hawaii"},
    {"name": "Idaho", "code": "ID", "slug": "idaho"},
    {"name": "Illinois", "code": "IL", "slug": "illinois"},
    {"name": "Indiana", "code": "IN", "slug": "indiana"},
    {"name": "Iowa", "code": "IA", "slug": "iowa"},
    {"name": "Kansas", "code": "KS", "slug": "kansas"},
    {"name": "Kentucky", "code": "KY", "slug": "kentucky"},
    {"name": "Louisiana", "code": "LA", "slug": "louisiana"},
    {"name": "Maine", "code": "ME", "slug": "maine"},
    {"name": "Maryland", "code": "MD", "slug": "maryland"},
    {"name": "Massachusetts", "code": "MA", "slug": "massachusetts"},
    {"name": "Michigan", "code": "MI", "slug": "michigan"},
    {"name": "Minnesota", "code": "MN", "slug": "minnesota"},
    {"name": "Mississippi", "code": "MS", "slug": "mississippi"},
    {"name": "Missouri", "code": "MO", "slug": "missouri"},
    {"name": "Montana", "code": "MT", "slug": "montana"},
    {"name": "Nebraska", "code": "NE", "slug": "nebraska"},
    {"name": "Nevada", "code": "NV", "slug": "nevada"},
    {"name": "New Hampshire", "code": "NH", "slug": "new-hampshire"},
    {"name": "New Jersey", "code": "NJ", "slug": "new-jersey"},
    {"name": "New Mexico", "code": "NM", "slug": "new-mexico"},
    {"name": "New York", "code": "NY", "slug": "new-york"},
    {"name": "North Carolina", "code": "NC", "slug": "north-carolina"},
    {"name": "North Dakota", "code": "ND", "slug": "north-dakota"},
    {"name": "Ohio", "code": "OH", "slug": "ohio"},
    {"name": "Oklahoma", "code": "OK", "slug": "oklahoma"},
    {"name": "Oregon", "code": "OR", "slug": "oregon"},
    {"name": "Pennsylvania", "code": "PA", "slug": "pennsylvania"},
    {"name": "Rhode Island", "code": "RI", "slug": "rhode-island"},
    {"name": "South Carolina", "code": "SC", "slug": "south-carolina"},
    {"name": "South Dakota", "code": "SD", "slug": "south-dakota"},
    {"name": "Tennessee", "code": "TN", "slug": "tennessee"},
    {"name": "Texas", "code": "TX", "slug": "texas"},
    {"name": "Utah", "code": "UT", "slug": "utah"},
    {"name": "Vermont", "code": "VT", "slug": "vermont"},
    {"name": "Virginia", "code": "VA", "slug": "virginia"},
    {"name": "Washington", "code": "WA", "slug": "washington"},
    {"name": "West Virginia", "code": "WV", "slug": "west-virginia"},
    {"name": "Wisconsin", "code": "WI", "slug": "wisconsin"},
    {"name": "Wyoming", "code": "WY", "slug": "wyoming"}
  ]
}
EOF
```

### Step 3.2: Create Cities Data

You have two options:

**Option A: Use Existing Master Data (Recommended)**

```bash
# Copy from master cities file if it exists
cp /home/ec2-user/clawd/data/us-cities-master.json data/cities.json 2>/dev/null || echo "Master file not found, use Option B"
```

**Option B: Create Minimal Starter Data**

Create `data/cities.json` with top cities (you'll expand this later):

```bash
cat > data/cities.json << 'EOF'
{
  "cities": [
    {"city": "New York", "state": "New York", "stateCode": "NY", "slug": "new-york", "population": 8336817, "lat": 40.7128, "lng": -74.0060},
    {"city": "Los Angeles", "state": "California", "stateCode": "CA", "slug": "los-angeles", "population": 3979576, "lat": 34.0522, "lng": -118.2437},
    {"city": "Chicago", "state": "Illinois", "stateCode": "IL", "slug": "chicago", "population": 2693976, "lat": 41.8781, "lng": -87.6298},
    {"city": "Houston", "state": "Texas", "stateCode": "TX", "slug": "houston", "population": 2320268, "lat": 29.7604, "lng": -95.3698},
    {"city": "Phoenix", "state": "Arizona", "stateCode": "AZ", "slug": "phoenix", "population": 1680992, "lat": 33.4484, "lng": -112.0740},
    {"city": "Philadelphia", "state": "Pennsylvania", "stateCode": "PA", "slug": "philadelphia", "population": 1584064, "lat": 39.9526, "lng": -75.1652},
    {"city": "San Antonio", "state": "Texas", "stateCode": "TX", "slug": "san-antonio", "population": 1547253, "lat": 29.4241, "lng": -98.4936},
    {"city": "San Diego", "state": "California", "stateCode": "CA", "slug": "san-diego", "population": 1423851, "lat": 32.7157, "lng": -117.1611},
    {"city": "Dallas", "state": "Texas", "stateCode": "TX", "slug": "dallas", "population": 1343573, "lat": 32.7767, "lng": -96.7970},
    {"city": "San Jose", "state": "California", "stateCode": "CA", "slug": "san-jose", "population": 1021795, "lat": 37.3382, "lng": -121.8863},
    {"city": "Austin", "state": "Texas", "stateCode": "TX", "slug": "austin", "population": 978908, "lat": 30.2672, "lng": -97.7431},
    {"city": "Jacksonville", "state": "Florida", "stateCode": "FL", "slug": "jacksonville", "population": 911507, "lat": 30.3322, "lng": -81.6557},
    {"city": "Fort Worth", "state": "Texas", "stateCode": "TX", "slug": "fort-worth", "population": 909585, "lat": 32.7555, "lng": -97.3308},
    {"city": "Columbus", "state": "Ohio", "stateCode": "OH", "slug": "columbus", "population": 898553, "lat": 39.9612, "lng": -82.9988},
    {"city": "Charlotte", "state": "North Carolina", "stateCode": "NC", "slug": "charlotte", "population": 885708, "lat": 35.2271, "lng": -80.8431},
    {"city": "San Francisco", "state": "California", "stateCode": "CA", "slug": "san-francisco", "population": 881549, "lat": 37.7749, "lng": -122.4194},
    {"city": "Indianapolis", "state": "Indiana", "stateCode": "IN", "slug": "indianapolis", "population": 876384, "lat": 39.7684, "lng": -86.1581},
    {"city": "Seattle", "state": "Washington", "stateCode": "WA", "slug": "seattle", "population": 753675, "lat": 47.6062, "lng": -122.3321},
    {"city": "Denver", "state": "Colorado", "stateCode": "CO", "slug": "denver", "population": 727211, "lat": 39.7392, "lng": -104.9903},
    {"city": "Washington", "state": "District of Columbia", "stateCode": "DC", "slug": "washington-dc", "population": 689545, "lat": 38.9072, "lng": -77.0369},
    {"city": "Boston", "state": "Massachusetts", "stateCode": "MA", "slug": "boston", "population": 692600, "lat": 42.3601, "lng": -71.0589},
    {"city": "Nashville", "state": "Tennessee", "stateCode": "TN", "slug": "nashville", "population": 689447, "lat": 36.1627, "lng": -86.7816},
    {"city": "El Paso", "state": "Texas", "stateCode": "TX", "slug": "el-paso", "population": 681728, "lat": 31.7619, "lng": -106.4850},
    {"city": "Detroit", "state": "Michigan", "stateCode": "MI", "slug": "detroit", "population": 670031, "lat": 42.3314, "lng": -83.0458},
    {"city": "Portland", "state": "Oregon", "stateCode": "OR", "slug": "portland", "population": 654741, "lat": 45.5152, "lng": -122.6784},
    {"city": "Memphis", "state": "Tennessee", "stateCode": "TN", "slug": "memphis", "population": 651073, "lat": 35.1495, "lng": -90.0490},
    {"city": "Oklahoma City", "state": "Oklahoma", "stateCode": "OK", "slug": "oklahoma-city", "population": 649021, "lat": 35.4676, "lng": -97.5164},
    {"city": "Las Vegas", "state": "Nevada", "stateCode": "NV", "slug": "las-vegas", "population": 644644, "lat": 36.1699, "lng": -115.1398},
    {"city": "Louisville", "state": "Kentucky", "stateCode": "KY", "slug": "louisville", "population": 617638, "lat": 38.2527, "lng": -85.7585},
    {"city": "Baltimore", "state": "Maryland", "stateCode": "MD", "slug": "baltimore", "population": 585708, "lat": 39.2904, "lng": -76.6122},
    {"city": "Milwaukee", "state": "Wisconsin", "stateCode": "WI", "slug": "milwaukee", "population": 577222, "lat": 43.0389, "lng": -87.9065},
    {"city": "Albuquerque", "state": "New Mexico", "stateCode": "NM", "slug": "albuquerque", "population": 564559, "lat": 35.0844, "lng": -106.6504},
    {"city": "Tucson", "state": "Arizona", "stateCode": "AZ", "slug": "tucson", "population": 548073, "lat": 32.2226, "lng": -110.9747},
    {"city": "Fresno", "state": "California", "stateCode": "CA", "slug": "fresno", "population": 542107, "lat": 36.7378, "lng": -119.7871},
    {"city": "Sacramento", "state": "California", "stateCode": "CA", "slug": "sacramento", "population": 513624, "lat": 38.5816, "lng": -121.4944},
    {"city": "Atlanta", "state": "Georgia", "stateCode": "GA", "slug": "atlanta", "population": 498715, "lat": 33.7490, "lng": -84.3880},
    {"city": "Kansas City", "state": "Missouri", "stateCode": "MO", "slug": "kansas-city", "population": 495327, "lat": 39.0997, "lng": -94.5786},
    {"city": "Miami", "state": "Florida", "stateCode": "FL", "slug": "miami", "population": 467963, "lat": 25.7617, "lng": -80.1918},
    {"city": "Raleigh", "state": "North Carolina", "stateCode": "NC", "slug": "raleigh", "population": 467665, "lat": 35.7796, "lng": -78.6382},
    {"city": "Omaha", "state": "Nebraska", "stateCode": "NE", "slug": "omaha", "population": 478192, "lat": 41.2565, "lng": -95.9345},
    {"city": "Minneapolis", "state": "Minnesota", "stateCode": "MN", "slug": "minneapolis", "population": 429954, "lat": 44.9778, "lng": -93.2650},
    {"city": "Cleveland", "state": "Ohio", "stateCode": "OH", "slug": "cleveland", "population": 381009, "lat": 41.4993, "lng": -81.6944},
    {"city": "Tampa", "state": "Florida", "stateCode": "FL", "slug": "tampa", "population": 399700, "lat": 27.9506, "lng": -82.4572},
    {"city": "New Orleans", "state": "Louisiana", "stateCode": "LA", "slug": "new-orleans", "population": 391006, "lat": 29.9511, "lng": -90.0715},
    {"city": "Pittsburgh", "state": "Pennsylvania", "stateCode": "PA", "slug": "pittsburgh", "population": 302971, "lat": 40.4406, "lng": -79.9959},
    {"city": "Cincinnati", "state": "Ohio", "stateCode": "OH", "slug": "cincinnati", "population": 309317, "lat": 39.1031, "lng": -84.5120},
    {"city": "Orlando", "state": "Florida", "stateCode": "FL", "slug": "orlando", "population": 307573, "lat": 28.5383, "lng": -81.3792},
    {"city": "St. Louis", "state": "Missouri", "stateCode": "MO", "slug": "st-louis", "population": 301578, "lat": 38.6270, "lng": -90.1994},
    {"city": "Birmingham", "state": "Alabama", "stateCode": "AL", "slug": "birmingham", "population": 200733, "lat": 33.5207, "lng": -86.8025},
    {"city": "Salt Lake City", "state": "Utah", "stateCode": "UT", "slug": "salt-lake-city", "population": 199723, "lat": 40.7608, "lng": -111.8910}
  ]
}
EOF
```

### Step 3.3: Verify Data Files

```bash
# Check states.json is valid JSON
cat data/states.json | python3 -m json.tool > /dev/null && echo "✅ states.json is valid" || echo "❌ states.json has errors"

# Check cities.json is valid JSON
cat data/cities.json | python3 -m json.tool > /dev/null && echo "✅ cities.json is valid" || echo "❌ cities.json has errors"

# Count entries
echo "States: $(cat data/states.json | python3 -c 'import sys,json; print(len(json.load(sys.stdin)["states"]))')"
echo "Cities: $(cat data/cities.json | python3 -c 'import sys,json; print(len(json.load(sys.stdin)["cities"]))')"
```

**Expected output:**
```
✅ states.json is valid
✅ cities.json is valid
States: 50
Cities: 50 (or more if using full data)
```

### City Selection Criteria (For Full Sites)

When building a comprehensive site, include:

- **Tier 1:** Top 100 US cities by population (always include)
- **Tier 2:** Cities 50k+ population in target states
- **Tier 3:** County seats and regional centers

### Target Page Counts

| Site Type | States | Cities | Total Pages |
|-----------|--------|--------|-------------|
| Starter | 50 | 50 | ~100 |
| Standard | 50 | 250-350 | 300-400 |
| Comprehensive | 50 | 500+ | 550-600 |

---

## 4. Create Site Configuration

**Time Estimate:** 10 minutes

### Step 4.1: Create Site Config File

Create `data/site-config.json` with your site-specific settings:

```bash
cat > data/site-config.json << 'EOF'
{
  "siteName": "Commercial Truck Law",
  "domain": "commercialtrucklaw.com",
  "accidentType": "Commercial Truck Accident",
  "accidentTypePlural": "Commercial Truck Accidents",
  "tagline": "Fighting for Victims of Commercial Truck Accidents",
  "phone": "1-800-XXX-XXXX",
  "email": "contact@commercialtrucklaw.com",
  "webhookUrl": "https://webhook.kuriosbrand.com/leads/commercial-truck-law",
  "colors": {
    "primary": "#1e40af",
    "secondary": "#3b82f6",
    "accent": "#f59e0b"
  },
  "seo": {
    "titleTemplate": "%s | Commercial Truck Law",
    "defaultDescription": "Injured in a commercial truck accident? Our experienced attorneys fight for maximum compensation. Free consultation available 24/7."
  }
}
EOF
```

**⚠️ IMPORTANT: Update the following values for YOUR site:**
- `siteName` - Your brand name
- `domain` - Your actual domain
- `accidentType` - The type of accident (e.g., "Motorcycle Accident", "Pedestrian Accident")
- `phone` - Your phone number
- `email` - Your contact email
- `webhookUrl` - Your lead webhook endpoint

### Step 4.2: Create Utility Functions

Create `lib/utils.ts`:

```bash
cat > lib/utils.ts << 'EOF'
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

export function formatPhone(phone: string): string {
  const cleaned = phone.replace(/\D/g, '')
  const match = cleaned.match(/^(\d{1})(\d{3})(\d{3})(\d{4})$/)
  if (match) {
    return `${match[1]}-${match[2]}-${match[3]}-${match[4]}`
  }
  return phone
}

export function formatNumber(num: number): string {
  return new Intl.NumberFormat('en-US').format(num)
}
EOF
```

✅ **Verification:** Files exist and are valid

```bash
ls -la data/site-config.json lib/utils.ts
```

---

## 5. Create Components

**Time Estimate:** 45-60 minutes

### Step 5.1: Create Hero Component

Create `components/Hero.tsx`:

```bash
cat > components/Hero.tsx << 'EOF'
import CTAForm from './CTAForm'

interface HeroProps {
  title: string
  subtitle: string
  city?: string
  state?: string
}

export default function Hero({ title, subtitle, city, state }: HeroProps) {
  return (
    <section className="bg-gradient-to-br from-blue-900 to-blue-700 text-white py-16 md:py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              {title}
            </h1>
            <p className="text-xl text-blue-100 mb-8">
              {subtitle}
            </p>
            <ul className="space-y-3 mb-8">
              <li className="flex items-center gap-3">
                <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Free Consultation - No Fees Unless We Win</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Available 24/7 - Call Now</span>
              </li>
              <li className="flex items-center gap-3">
                <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span>Millions Recovered for Our Clients</span>
              </li>
            </ul>
          </div>
          <div className="bg-white rounded-lg p-6 md:p-8 shadow-2xl">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Get Your Free Case Review
            </h2>
            <CTAForm city={city} state={state} />
          </div>
        </div>
      </div>
    </section>
  )
}
EOF
```

### Step 5.2: Create CTA Form Component

Create `components/CTAForm.tsx`:

```bash
cat > components/CTAForm.tsx << 'EOF'
'use client'

import { useState, FormEvent } from 'react'

interface CTAFormProps {
  city?: string
  state?: string
}

export default function CTAForm({ city, state }: CTAFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setIsSubmitting(true)
    setError('')

    const formData = new FormData(e.currentTarget)
    const data = {
      name: formData.get('name'),
      phone: formData.get('phone'),
      email: formData.get('email'),
      accidentDate: formData.get('accidentDate'),
      description: formData.get('description'),
      city: city || 'Unknown',
      state: state || 'Unknown',
      source: typeof window !== 'undefined' ? window.location.hostname : '',
      page: typeof window !== 'undefined' ? window.location.pathname : '',
      timestamp: new Date().toISOString()
    }

    try {
      // Replace with your actual webhook URL
      const response = await fetch('https://webhook.kuriosbrand.com/leads/your-site', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })

      if (!response.ok) throw new Error('Failed to submit')
      
      setIsSubmitted(true)
    } catch (err) {
      setError('Something went wrong. Please call us directly.')
    } finally {
      setIsSubmitting(false)
    }
  }

  if (isSubmitted) {
    return (
      <div className="text-center py-8">
        <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-gray-900 mb-2">Thank You!</h3>
        <p className="text-gray-600">We&apos;ll contact you within 24 hours.</p>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
          Full Name *
        </label>
        <input
          type="text"
          id="name"
          name="name"
          required
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          placeholder="John Smith"
        />
      </div>
      
      <div>
        <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
          Phone Number *
        </label>
        <input
          type="tel"
          id="phone"
          name="phone"
          required
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          placeholder="(555) 123-4567"
        />
      </div>
      
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
          Email Address *
        </label>
        <input
          type="email"
          id="email"
          name="email"
          required
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          placeholder="john@example.com"
        />
      </div>
      
      <div>
        <label htmlFor="accidentDate" className="block text-sm font-medium text-gray-700 mb-1">
          Date of Accident *
        </label>
        <input
          type="date"
          id="accidentDate"
          name="accidentDate"
          required
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
        />
      </div>
      
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Brief Description (Optional)
        </label>
        <textarea
          id="description"
          name="description"
          rows={3}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          placeholder="Tell us what happened..."
        />
      </div>

      {error && (
        <div className="bg-red-50 text-red-700 p-3 rounded-lg text-sm">
          {error}
        </div>
      )}
      
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-orange-500 hover:bg-orange-600 text-white font-bold py-4 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? 'Submitting...' : 'Get My Free Consultation'}
      </button>
      
      <p className="text-xs text-gray-500 text-center">
        By submitting, you agree to our privacy policy. We&apos;ll never share your information.
      </p>
    </form>
  )
}
EOF
```

### Step 5.3: Create FAQ Component

Create `components/FAQ.tsx`:

```bash
cat > components/FAQ.tsx << 'EOF'
'use client'

import { useState } from 'react'

interface FAQItem {
  question: string
  answer: string
}

interface FAQProps {
  items: FAQItem[]
  city?: string
  state?: string
}

export default function FAQ({ items, city, state }: FAQProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(0)

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Frequently Asked Questions
          {city && ` About ${city} Accident Cases`}
        </h2>
        
        <div className="space-y-4">
          {items.map((item, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-sm border border-gray-200"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full px-6 py-4 text-left flex justify-between items-center"
              >
                <span className="font-semibold text-gray-900">{item.question}</span>
                <svg
                  className={`w-5 h-5 text-gray-500 transition-transform ${
                    openIndex === index ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {openIndex === index && (
                <div className="px-6 pb-4">
                  <p className="text-gray-600">{item.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* FAQ Schema for SEO */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@type": "FAQPage",
              "mainEntity": items.map(item => ({
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {
                  "@type": "Answer",
                  "text": item.answer
                }
              }))
            })
          }}
        />
      </div>
    </section>
  )
}
EOF
```

### Step 5.4: Create Testimonials Component

Create `components/Testimonials.tsx`:

```bash
cat > components/Testimonials.tsx << 'EOF'
interface Testimonial {
  name: string
  location: string
  quote: string
  rating: number
}

interface TestimonialsProps {
  items?: Testimonial[]
}

const defaultTestimonials: Testimonial[] = [
  {
    name: "Michael R.",
    location: "Texas",
    quote: "After my accident, I didn't know where to turn. This team fought for me and got me the compensation I deserved. Highly recommend!",
    rating: 5
  },
  {
    name: "Sarah T.",
    location: "California",
    quote: "Professional, compassionate, and effective. They handled everything while I focused on recovery. Thank you!",
    rating: 5
  },
  {
    name: "David M.",
    location: "Florida",
    quote: "I was skeptical at first, but they exceeded all expectations. The settlement was more than I ever expected.",
    rating: 5
  }
]

export default function Testimonials({ items = defaultTestimonials }: TestimonialsProps) {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          What Our Clients Say
        </h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          {items.map((testimonial, index) => (
            <div
              key={index}
              className="bg-gray-50 rounded-lg p-6 shadow-sm"
            >
              <div className="flex mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <svg
                    key={i}
                    className="w-5 h-5 text-yellow-400"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              
              <p className="text-gray-600 mb-4 italic">
                &ldquo;{testimonial.quote}&rdquo;
              </p>
              
              <div className="font-semibold text-gray-900">
                {testimonial.name}
              </div>
              <div className="text-sm text-gray-500">
                {testimonial.location}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
EOF
```

### Step 5.5: Create CityList Component

Create `components/CityList.tsx`:

```bash
cat > components/CityList.tsx << 'EOF'
import Link from 'next/link'

interface City {
  city: string
  slug: string
  stateCode: string
  population: number
}

interface CityListProps {
  cities: City[]
  stateCode?: string
  title?: string
}

export default function CityList({ cities, stateCode, title }: CityListProps) {
  const filteredCities = stateCode 
    ? cities.filter(c => c.stateCode === stateCode)
    : cities

  const sortedCities = [...filteredCities].sort((a, b) => b.population - a.population)

  return (
    <section className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {title && (
          <h2 className="text-2xl font-bold text-gray-900 mb-8">{title}</h2>
        )}
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {sortedCities.map((city) => (
            <Link
              key={`${city.slug}-${city.stateCode}`}
              href={`/${city.stateCode.toLowerCase()}/${city.slug}/`}
              className="p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
            >
              <div className="font-semibold text-gray-900">{city.city}</div>
              <div className="text-sm text-gray-500">{city.stateCode}</div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
}
EOF
```

### Step 5.6: Create Navigation Component

Create `components/Navigation.tsx`:

```bash
cat > components/Navigation.tsx << 'EOF'
'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-blue-900">
              {/* Replace with your site name */}
              Commercial Truck Law
            </Link>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/" className="text-gray-700 hover:text-blue-600">
              Home
            </Link>
            <Link href="/about/" className="text-gray-700 hover:text-blue-600">
              About Us
            </Link>
            <Link href="/contact/" className="text-gray-700 hover:text-blue-600">
              Contact
            </Link>
            <a
              href="tel:1-800-XXX-XXXX"
              className="bg-orange-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
            >
              Call Now
            </a>
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-700 p-2"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      {/* Mobile Navigation */}
      {isOpen && (
        <div className="md:hidden border-t">
          <div className="px-4 py-4 space-y-3">
            <Link href="/" className="block text-gray-700 hover:text-blue-600">
              Home
            </Link>
            <Link href="/about/" className="block text-gray-700 hover:text-blue-600">
              About Us
            </Link>
            <Link href="/contact/" className="block text-gray-700 hover:text-blue-600">
              Contact
            </Link>
            <a
              href="tel:1-800-XXX-XXXX"
              className="block bg-orange-500 text-white px-4 py-2 rounded-lg font-semibold text-center"
            >
              Call Now
            </a>
          </div>
        </div>
      )}
    </nav>
  )
}
EOF
```

### Step 5.7: Create Footer Component

Create `components/Footer.tsx`:

```bash
cat > components/Footer.tsx << 'EOF'
import Link from 'next/link'

export default function Footer() {
  const currentYear = new Date().getFullYear()
  
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <div className="text-xl font-bold mb-4">Commercial Truck Law</div>
            <p className="text-gray-400 text-sm">
              Dedicated to helping accident victims get the compensation they deserve.
            </p>
          </div>
          
          {/* Quick Links */}
          <div>
            <h3 className="font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link href="/" className="hover:text-white">Home</Link></li>
              <li><Link href="/about/" className="hover:text-white">About Us</Link></li>
              <li><Link href="/contact/" className="hover:text-white">Contact</Link></li>
            </ul>
          </div>
          
          {/* Contact */}
          <div>
            <h3 className="font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li>
                <a href="tel:1-800-XXX-XXXX" className="hover:text-white">
                  1-800-XXX-XXXX
                </a>
              </li>
              <li>
                <a href="mailto:contact@example.com" className="hover:text-white">
                  contact@example.com
                </a>
              </li>
            </ul>
          </div>
          
          {/* Legal */}
          <div>
            <h3 className="font-semibold mb-4">Legal</h3>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link href="/privacy/" className="hover:text-white">Privacy Policy</Link></li>
              <li><Link href="/terms/" className="hover:text-white">Terms of Service</Link></li>
              <li><Link href="/disclaimer/" className="hover:text-white">Disclaimer</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; {currentYear} Commercial Truck Law. All rights reserved.</p>
          <p className="mt-2">
            This is attorney advertising. Past results do not guarantee future outcomes.
          </p>
        </div>
      </div>
    </footer>
  )
}
EOF
```

### Step 5.8: Verify All Components

```bash
# List all components
ls -la components/

# Expected:
# Hero.tsx
# CTAForm.tsx
# FAQ.tsx
# Testimonials.tsx
# CityList.tsx
# Navigation.tsx
# Footer.tsx
```

✅ **Verification:** All 7 component files exist

---

## 6. Create Page Templates

**Time Estimate:** 30-45 minutes

### Step 6.1: Update Root Layout

Replace `app/layout.tsx`:

```bash
cat > app/layout.tsx << 'EOF'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navigation from '@/components/Navigation'
import Footer from '@/components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Commercial Truck Accident Lawyers | Free Consultation',
  description: 'Injured in a commercial truck accident? Our experienced attorneys fight for maximum compensation. Free consultation available 24/7.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navigation />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  )
}
EOF
```

### Step 6.2: Create Homepage

Replace `app/page.tsx`:

```bash
cat > app/page.tsx << 'EOF'
import Hero from '@/components/Hero'
import Testimonials from '@/components/Testimonials'
import FAQ from '@/components/FAQ'
import CityList from '@/components/CityList'
import citiesData from '@/data/cities.json'

const faqs = [
  {
    question: "How much does it cost to hire a truck accident lawyer?",
    answer: "We work on a contingency fee basis, meaning you pay nothing unless we win your case. There are no upfront costs or hourly fees."
  },
  {
    question: "How long do I have to file a truck accident claim?",
    answer: "The statute of limitations varies by state, typically 2-3 years from the date of the accident. However, it's crucial to act quickly to preserve evidence and protect your rights."
  },
  {
    question: "What compensation can I receive for my injuries?",
    answer: "You may be entitled to compensation for medical expenses, lost wages, pain and suffering, property damage, and in some cases, punitive damages."
  },
  {
    question: "What should I do immediately after a truck accident?",
    answer: "Seek medical attention first. Then, document the scene if possible, exchange information with the other driver, report to police, and contact an attorney before speaking with insurance companies."
  },
  {
    question: "Why are truck accident cases different from car accidents?",
    answer: "Truck accidents often involve multiple liable parties (driver, trucking company, manufacturers), federal regulations, larger insurance policies, and more severe injuries requiring specialized legal expertise."
  }
]

export default function Home() {
  return (
    <>
      <Hero
        title="Injured in a Truck Accident? We Fight for You."
        subtitle="Our experienced attorneys have recovered millions for truck accident victims. Get your free consultation today."
      />
      
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Why Choose Our Truck Accident Lawyers?
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">💰</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">No Win, No Fee</h3>
              <p className="text-gray-600">You pay nothing unless we recover compensation for you.</p>
            </div>
            
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">⚖️</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Proven Results</h3>
              <p className="text-gray-600">Millions recovered for truck accident victims nationwide.</p>
            </div>
            
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-3xl">📞</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">24/7 Availability</h3>
              <p className="text-gray-600">We&apos;re here when you need us, day or night.</p>
            </div>
          </div>
        </div>
      </section>
      
      <Testimonials />
      
      <FAQ items={faqs} />
      
      <CityList 
        cities={citiesData.cities}
        title="We Serve Clients Nationwide"
      />
    </>
  )
}
EOF
```

### Step 6.3: Create State Page Template

Create `app/[state]/page.tsx`:

```bash
cat > 'app/[state]/page.tsx' << 'EOF'
import { notFound } from 'next/navigation'
import Hero from '@/components/Hero'
import FAQ from '@/components/FAQ'
import CityList from '@/components/CityList'
import statesData from '@/data/states.json'
import citiesData from '@/data/cities.json'

interface Props {
  params: { state: string }
}

export async function generateStaticParams() {
  return statesData.states.map((state) => ({
    state: state.slug
  }))
}

export async function generateMetadata({ params }: Props) {
  const state = statesData.states.find(s => s.slug === params.state)
  if (!state) return {}
  
  return {
    title: `Commercial Truck Accident Lawyers in ${state.name} | Free Consultation`,
    description: `Injured in a truck accident in ${state.name}? Our experienced attorneys fight for maximum compensation. Free consultation available 24/7.`
  }
}

export default function StatePage({ params }: Props) {
  const state = statesData.states.find(s => s.slug === params.state)
  
  if (!state) {
    notFound()
  }
  
  const stateCities = citiesData.cities.filter(c => c.stateCode === state.code)
  
  const faqs = [
    {
      question: `How long do I have to file a truck accident lawsuit in ${state.name}?`,
      answer: `In ${state.name}, the statute of limitations for personal injury claims is typically 2-3 years, but this can vary. Contact us immediately to ensure you don't miss important deadlines.`
    },
    {
      question: `What are common causes of truck accidents in ${state.name}?`,
      answer: `Common causes include driver fatigue, speeding, improper maintenance, distracted driving, and violations of federal trucking regulations. ${state.name}'s highways see significant commercial truck traffic.`
    },
    {
      question: `How much is my ${state.name} truck accident case worth?`,
      answer: `Case values depend on injury severity, medical costs, lost wages, and other factors. Our ${state.name} truck accident lawyers provide free case evaluations to help you understand potential compensation.`
    }
  ]
  
  return (
    <>
      <Hero
        title={`Truck Accident Lawyers in ${state.name}`}
        subtitle={`Fighting for truck accident victims across ${state.name}. Get the compensation you deserve with our experienced legal team.`}
        state={state.name}
      />
      
      <section className="py-12 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Truck Accident Laws in {state.name}
          </h2>
          <div className="prose prose-lg text-gray-600">
            <p>
              If you&apos;ve been injured in a commercial truck accident in {state.name}, 
              you need experienced legal representation to navigate the complex laws 
              and regulations that govern these cases. Our {state.name} truck accident 
              lawyers understand both federal trucking regulations and {state.name} state law.
            </p>
            <p>
              Commercial truck accidents often result in serious injuries due to the 
              size and weight difference between trucks and passenger vehicles. In {state.name}, 
              victims may be entitled to compensation for medical expenses, lost wages, 
              pain and suffering, and more.
            </p>
          </div>
        </div>
      </section>
      
      <FAQ items={faqs} state={state.name} />
      
      {stateCities.length > 0 && (
        <CityList 
          cities={stateCities}
          title={`Cities We Serve in ${state.name}`}
        />
      )}

      {/* LocalBusiness Schema */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "LegalService",
            "name": `Commercial Truck Accident Lawyers in ${state.name}`,
            "description": `Experienced truck accident attorneys serving ${state.name}`,
            "areaServed": {
              "@type": "State",
              "name": state.name
            },
            "serviceType": "Truck Accident Legal Services"
          })
        }}
      />
    </>
  )
}
EOF
```

### Step 6.4: Create City Page Template (Money Pages)

Create `app/[state]/[city]/page.tsx`:

```bash
cat > 'app/[state]/[city]/page.tsx' << 'EOF'
import { notFound } from 'next/navigation'
import Hero from '@/components/Hero'
import FAQ from '@/components/FAQ'
import CityList from '@/components/CityList'
import statesData from '@/data/states.json'
import citiesData from '@/data/cities.json'

interface Props {
  params: { state: string; city: string }
}

export async function generateStaticParams() {
  return citiesData.cities.map((city) => {
    const state = statesData.states.find(s => s.code === city.stateCode)
    return {
      state: state?.slug || city.stateCode.toLowerCase(),
      city: city.slug
    }
  })
}

export async function generateMetadata({ params }: Props) {
  const state = statesData.states.find(s => s.slug === params.state)
  const city = citiesData.cities.find(
    c => c.slug === params.city && c.stateCode === state?.code
  )
  
  if (!state || !city) return {}
  
  return {
    title: `Commercial Truck Accident Lawyer in ${city.city}, ${state.name} | Free Consultation`,
    description: `Injured in a truck accident in ${city.city}, ${state.code}? Our local attorneys fight for maximum compensation. Serving ${city.city} and surrounding areas. Free consultation.`
  }
}

export default function CityPage({ params }: Props) {
  const state = statesData.states.find(s => s.slug === params.state)
  const city = citiesData.cities.find(
    c => c.slug === params.city && c.stateCode === state?.code
  )
  
  if (!state || !city) {
    notFound()
  }

  // Get nearby cities (same state, excluding current)
  const nearbyCities = citiesData.cities
    .filter(c => c.stateCode === state.code && c.slug !== city.slug)
    .slice(0, 8)

  const faqs = [
    {
      question: `How do I find a good truck accident lawyer in ${city.city}?`,
      answer: `Look for attorneys with specific experience in truck accident cases, a track record of successful settlements, and knowledge of ${city.city} and ${state.name} courts. Our team has represented numerous clients in the ${city.city} area.`
    },
    {
      question: `What should I do after a truck accident in ${city.city}?`,
      answer: `First, seek medical attention. Then document the scene, get the truck driver's information, report to ${city.city} police, and contact a truck accident lawyer before speaking with insurance companies.`
    },
    {
      question: `How much does a ${city.city} truck accident lawyer cost?`,
      answer: `We work on contingency in ${city.city}, meaning you pay nothing upfront and no fees unless we win your case. Our payment comes from the settlement or verdict we obtain for you.`
    },
    {
      question: `What compensation can I get for a truck accident in ${city.city}, ${state.code}?`,
      answer: `${city.city} truck accident victims may recover medical expenses, lost wages, pain and suffering, property damage, and potentially punitive damages depending on the circumstances of your case.`
    }
  ]

  const populationText = city.population > 1000000 
    ? `${(city.population / 1000000).toFixed(1)} million`
    : city.population > 100000
    ? `${Math.round(city.population / 1000)}K`
    : city.population.toLocaleString()
  
  return (
    <>
      <Hero
        title={`Truck Accident Lawyer in ${city.city}, ${state.code}`}
        subtitle={`Local attorneys fighting for truck accident victims in ${city.city}. We know the roads, the courts, and how to win your case.`}
        city={city.city}
        state={state.name}
      />
      
      <section className="py-12 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Truck Accident Attorneys Serving {city.city}, {state.name}
          </h2>
          <div className="prose prose-lg text-gray-600">
            <p>
              {city.city}, with a population of {populationText} residents, sees significant 
              commercial truck traffic daily. When accidents happen on {city.city}&apos;s roads 
              and highways, the results can be devastating. Our experienced truck accident 
              lawyers are here to help {city.city} residents get the compensation they deserve.
            </p>
            <p>
              As local {city.city} attorneys, we understand the unique challenges of truck 
              accident cases in this area. From major highways to local roads, we know where 
              accidents happen and how to build strong cases for our clients.
            </p>
            <h3>Why Hire a Local {city.city} Truck Accident Lawyer?</h3>
            <ul>
              <li>Knowledge of local courts and legal procedures</li>
              <li>Understanding of {city.city} traffic patterns and accident hotspots</li>
              <li>Established relationships with local experts and investigators</li>
              <li>Convenient for in-person meetings when needed</li>
            </ul>
          </div>
        </div>
      </section>
      
      <FAQ items={faqs} city={city.city} state={state.name} />
      
      {nearbyCities.length > 0 && (
        <CityList 
          cities={nearbyCities}
          title={`Also Serving Nearby ${state.name} Cities`}
        />
      )}

      {/* LocalBusiness Schema with geo */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            "@context": "https://schema.org",
            "@type": "LegalService",
            "name": `Commercial Truck Accident Lawyer in ${city.city}, ${state.code}`,
            "description": `Experienced truck accident attorneys serving ${city.city}, ${state.name}`,
            "areaServed": {
              "@type": "City",
              "name": city.city,
              "containedInPlace": {
                "@type": "State",
                "name": state.name
              }
            },
            "geo": {
              "@type": "GeoCoordinates",
              "latitude": city.lat,
              "longitude": city.lng
            },
            "serviceType": "Truck Accident Legal Services"
          })
        }}
      />
    </>
  )
}
EOF
```

### Step 6.5: Create About Page

Create `app/about/page.tsx`:

```bash
cat > app/about/page.tsx << 'EOF'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Our Truck Accident Law Firm | Experienced Attorneys',
  description: 'Learn about our experienced team of truck accident lawyers dedicated to fighting for victims of commercial truck accidents nationwide.'
}

export default function AboutPage() {
  return (
    <>
      <section className="bg-blue-900 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold mb-4">About Our Firm</h1>
          <p className="text-xl text-blue-100">
            Dedicated advocates for truck accident victims
          </p>
        </div>
      </section>
      
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="prose prose-lg max-w-none">
            <h2>Our Mission</h2>
            <p>
              We founded this firm with a single purpose: to help victims of commercial 
              truck accidents get the justice and compensation they deserve. Truck accidents 
              are among the most devastating types of vehicle collisions, often resulting in 
              life-changing injuries or death.
            </p>
            
            <h2>Why We Focus on Truck Accidents</h2>
            <p>
              Truck accident cases are fundamentally different from car accident cases. They 
              involve complex federal regulations, multiple potentially liable parties 
              (including drivers, trucking companies, and manufacturers), and large insurance 
              policies with teams of lawyers fighting against victims.
            </p>
            <p>
              Our team has dedicated years to understanding the intricacies of trucking 
              regulations, industry practices, and the tactics insurance companies use to 
              minimize payouts. This specialized knowledge allows us to build stronger cases 
              and achieve better results for our clients.
            </p>
            
            <h2>Our Approach</h2>
            <ul>
              <li>
                <strong>Thorough Investigation:</strong> We work with accident reconstruction 
                experts, review driver logs, and analyze black box data to build compelling cases.
              </li>
              <li>
                <strong>Aggressive Negotiation:</strong> We don&apos;t settle for lowball offers. 
                We fight for the full compensation our clients deserve.
              </li>
              <li>
                <strong>Trial Ready:</strong> While most cases settle, we prepare every case 
                as if it&apos;s going to trial. This preparation often leads to better settlements.
              </li>
            </ul>
            
            <h2>No Win, No Fee</h2>
            <p>
              We believe everyone deserves access to quality legal representation, regardless 
              of their financial situation. That&apos;s why we work on a contingency fee basis. 
              You pay nothing unless we win your case.
            </p>
          </div>
        </div>
      </section>
    </>
  )
}
EOF
```

### Step 6.6: Create Contact Page

Create `app/contact/page.tsx`:

```bash
cat > app/contact/page.tsx << 'EOF'
import type { Metadata } from 'next'
import CTAForm from '@/components/CTAForm'

export const metadata: Metadata = {
  title: 'Contact Our Truck Accident Lawyers | Free Consultation',
  description: 'Contact our experienced truck accident attorneys for a free consultation. Available 24/7. Call now or fill out our online form.'
}

export default function ContactPage() {
  return (
    <>
      <section className="bg-blue-900 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
          <p className="text-xl text-blue-100">
            Get your free consultation today
          </p>
        </div>
      </section>
      
      <section className="py-16 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Get in Touch
              </h2>
              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Phone</h3>
                    <a href="tel:1-800-XXX-XXXX" className="text-blue-600 hover:text-blue-700">
                      1-800-XXX-XXXX
                    </a>
                    <p className="text-sm text-gray-500">Available 24/7</p>
                  </div>
                </div>
                
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Email</h3>
                    <a href="mailto:contact@example.com" className="text-blue-600 hover:text-blue-700">
                      contact@example.com
                    </a>
                    <p className="text-sm text-gray-500">We respond within 24 hours</p>
                  </div>
                </div>
              </div>
              
              <div className="mt-8 p-6 bg-white rounded-lg shadow-sm">
                <h3 className="font-semibold text-gray-900 mb-2">
                  Why Contact Us?
                </h3>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Free, no-obligation consultation
                  </li>
                  <li className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    No fees unless we win your case
                  </li>
                  <li className="flex items-center gap-2">
                    <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Experienced truck accident attorneys
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Request Free Consultation
              </h2>
              <CTAForm />
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
EOF
```

### Step 6.7: Create robots.txt and sitemap

Create `app/robots.ts`:

```bash
cat > app/robots.ts << 'EOF'
import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
    },
    sitemap: 'https://yoursite.com/sitemap.xml',
  }
}
EOF
```

Create `app/sitemap.ts`:

```bash
cat > app/sitemap.ts << 'EOF'
import { MetadataRoute } from 'next'
import statesData from '@/data/states.json'
import citiesData from '@/data/cities.json'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://yoursite.com'
  
  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${baseUrl}/about/`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/contact/`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
  ]

  // State pages
  const statePages: MetadataRoute.Sitemap = statesData.states.map((state) => ({
    url: `${baseUrl}/${state.slug}/`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.9,
  }))

  // City pages
  const cityPages: MetadataRoute.Sitemap = citiesData.cities.map((city) => {
    const state = statesData.states.find(s => s.code === city.stateCode)
    return {
      url: `${baseUrl}/${state?.slug || city.stateCode.toLowerCase()}/${city.slug}/`,
      lastModified: new Date(),
      changeFrequency: 'weekly' as const,
      priority: 0.8,
    }
  })

  return [...staticPages, ...statePages, ...cityPages]
}
EOF
```

### Step 6.8: Verify All Pages

```bash
# List all page files
find app -name "page.tsx" -o -name "layout.tsx" | sort

# Expected output:
# app/[state]/[city]/page.tsx
# app/[state]/page.tsx
# app/about/page.tsx
# app/contact/page.tsx
# app/layout.tsx
# app/page.tsx
```

✅ **Verification:** All page files exist

---

## 7. Build and Test Locally

**Time Estimate:** 15-20 minutes

### Step 7.1: Run Development Server

```bash
# Start the dev server
npm run dev
```

**Open browser to:** http://localhost:3000

**Check these pages:**
- [ ] Homepage loads: http://localhost:3000
- [ ] State page loads: http://localhost:3000/texas/
- [ ] City page loads: http://localhost:3000/texas/houston/
- [ ] About page loads: http://localhost:3000/about/
- [ ] Contact page loads: http://localhost:3000/contact/

Press `Ctrl+C` to stop the dev server.

### Step 7.2: Build Static Site

```bash
# Build the static site
npm run build
```

**Expected output:**
```
Route (app)                              Size     First Load JS
┌ ○ /                                    ...
├ ○ /[state]                             ...
├ ○ /[state]/[city]                      ...
├ ○ /about                               ...
├ ○ /contact                             ...
└ ...

○  (Static)   prerendered as static content
```

**If you get errors:**
- Read the error message carefully
- Common issues:
  - TypeScript errors: Check component files for typos
  - JSON errors: Validate your data files
  - Import errors: Check file paths

### Step 7.3: Verify Build Output

```bash
# Check output directory exists
ls -la out/

# Count generated HTML files
find out -name "*.html" | wc -l
# Expected: 100+ files (depends on your cities data)

# Check a specific page
head -50 out/texas/houston/index.html
```

**What to look for in the HTML:**
- Proper title tag
- Meta description
- Content renders (not blank)
- Schema markup present

### Step 7.4: Test Static Build Locally

```bash
# Install a simple HTTP server if needed
npm install -g serve

# Serve the static files
serve out
```

Open http://localhost:3000 and test navigation between pages.

✅ **Verification:** 
- All pages load correctly
- Navigation works
- Forms render (won't submit without a real webhook)

---

## 8. Deployment to Cloudflare Pages

**Time Estimate:** 15-20 minutes

### Step 8.1: Verify Cloudflare Credentials

```bash
# Check credentials exist
cat ~/.config/cloudflare/credentials.json

# Expected format:
# {"api_token": "your-token-here", "account_id": "your-account-id"}
```

**If missing, create the credentials:**
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Create Token → Custom Token
3. Permissions: Cloudflare Pages (Edit)
4. Save token to `~/.config/cloudflare/credentials.json`

### Step 8.2: Install Wrangler (If Needed)

```bash
# Check if wrangler is installed
npx wrangler --version

# If not installed, it will auto-install on first use
```

### Step 8.3: Deploy to Cloudflare Pages

```bash
# Read token from credentials
CLOUDFLARE_API_TOKEN=$(cat ~/.config/cloudflare/credentials.json | python3 -c "import sys,json; print(json.load(sys.stdin)['api_token'])")

# Deploy (replace YOUR-PROJECT-NAME with your project name, e.g., commercial-truck-law)
CLOUDFLARE_API_TOKEN=$CLOUDFLARE_API_TOKEN npx wrangler pages deploy ./out --project-name=YOUR-PROJECT-NAME
```

**First deployment will:**
- Create the Pages project if it doesn't exist
- Upload all files from `./out`
- Return a URL like: `https://YOUR-PROJECT-NAME.pages.dev`

### Step 8.4: Verify Deployment

```bash
# Visit your deployed site
echo "Visit: https://YOUR-PROJECT-NAME.pages.dev"
```

**Check:**
- [ ] Homepage loads
- [ ] State pages work
- [ ] City pages work
- [ ] Mobile responsive
- [ ] Navigation works

### Step 8.5: Add Custom Domain (Optional)

1. Go to Cloudflare Dashboard → Pages → Your Project → Custom domains
2. Click "Set up a custom domain"
3. Enter your domain (e.g., `commercialtrucklaw.com`)
4. If domain is already on Cloudflare:
   - DNS records are added automatically
5. If domain is elsewhere:
   - Add the provided CNAME record to your DNS

**Wait 5-10 minutes for DNS propagation**

✅ **Verification:** Site loads on custom domain with HTTPS

---

## 9. Post-Deployment Setup

**Time Estimate:** 30-45 minutes

### Step 9.1: Google Search Console Setup

1. Go to https://search.google.com/search-console
2. Click "Add property"
3. Choose "URL prefix" method
4. Enter your domain: `https://yoursite.com`
5. Verify using one of:
   - **HTML file (recommended):** Download, add to `/out`, redeploy
   - **DNS TXT record:** Add to Cloudflare DNS
   - **HTML tag:** Add to layout.tsx head

**After verification:**
```
1. Click "Sitemaps" in left menu
2. Enter: sitemap.xml
3. Click "Submit"
4. Wait for Google to process (can take days)
```

### Step 9.2: Bing Webmaster Tools Setup

1. Go to https://www.bing.com/webmasters
2. Sign in with Microsoft account
3. Add your site URL
4. Import from Google Search Console (easiest) OR verify manually
5. Submit sitemap: `https://yoursite.com/sitemap.xml`

### Step 9.3: Update Webhook URL

**IMPORTANT:** The form won't work until you configure the webhook.

1. Edit `components/CTAForm.tsx`
2. Find this line:
```typescript
const response = await fetch('https://webhook.kuriosbrand.com/leads/your-site', {
```
3. Replace with your actual webhook URL
4. Rebuild and redeploy

### Step 9.4: Test Form Submission

1. Go to a city page on your live site
2. Fill out the form with test data
3. Submit
4. Verify:
   - [ ] Form shows success message
   - [ ] Webhook receives the data
   - [ ] Lead appears in your CRM/GHL

---

## 10. Quality Audit Checklist

**Time Estimate:** 20-30 minutes

### Pre-Launch Checklist

Run through this checklist before considering the site "done":

```
□ All pages generate without errors (npm run build succeeds)
□ Homepage loads and looks correct
□ At least 5 random state pages checked
□ At least 10 random city pages checked
□ Navigation works on all pages
□ Forms render correctly
□ Forms submit successfully (test submission)
□ Mobile responsive (test on phone or browser dev tools)
□ No console errors (check browser dev tools)
□ Page speed > 90 (test on https://pagespeed.web.dev/)
□ Sitemap generates and is accessible
□ robots.txt is correct
□ Schema markup validates (https://validator.schema.org/)
□ Custom domain working (if applicable)
□ HTTPS working
□ Search Console property added
□ Sitemap submitted to Search Console
```

### Content Quality Score (/100)

| Item | Points | Check |
|------|--------|-------|
| Unique H1 on all pages | 10 | `grep -r "<h1" out/ \| wc -l` matches page count |
| Unique meta descriptions | 10 | Spot check 5 random pages |
| No broken internal links | 10 | Click around, no 404s |
| Images have alt text | 10 | Inspect images in dev tools |
| Schema markup on all pages | 10 | Check page source |
| Mobile responsive | 10 | Test at 375px width |
| Page speed > 90 | 10 | Test on PageSpeed Insights |
| Forms working | 10 | Test submission |
| Sitemap complete | 10 | Check `/sitemap.xml` |
| No console errors | 10 | Check browser dev tools |

**Scoring:**
- 90-100: ✅ Ship it!
- 80-89: Minor fixes, then ship
- < 80: Needs work before launch

---

## 11. Troubleshooting Guide

### Build Errors

**Error: "Cannot find module '@/data/cities.json'"**
```bash
# Fix: Ensure the file exists
ls data/cities.json
# If missing, create it (see Step 3)
```

**Error: "Type error: Property 'X' does not exist"**
```bash
# Fix: Check TypeScript types match your data structure
# Ensure JSON files have correct field names
```

**Error: "Export encountered an error"**
```bash
# Fix: Check for dynamic imports or server-side code
# All pages must be static for `output: 'export'`
```

### Deployment Errors

**Error: "Authentication error" when deploying**
```bash
# Fix: Verify your API token
cat ~/.config/cloudflare/credentials.json
# Ensure token has Pages Edit permission
```

**Error: "Project not found"**
```bash
# Fix: Create the project first via Cloudflare dashboard
# Or let wrangler create it (first deploy creates it)
```

### Form Not Working

**Form submits but no leads received:**
1. Check browser Network tab for the POST request
2. Verify webhook URL is correct
3. Check webhook endpoint is receiving requests
4. Check for CORS errors in console

**CORS Error:**
```
# Your webhook must allow cross-origin requests
# Add these headers to webhook response:
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Methods: POST
```

### Pages Not Generating

**Only a few pages generate:**
```bash
# Check your data files have entries
cat data/cities.json | python3 -c "import sys,json; print(len(json.load(sys.stdin)['cities']))"

# Check generateStaticParams returns all entries
```

---

## 12. Reference: Sites Built

| Domain | Niche | Pages | Status |
|--------|-------|-------|--------|
| commercialtrucklaw.com | Commercial trucks | 355 | ✅ Deployed |
| motorcyclewrecklaw.com | Motorcycles | 355 | ✅ Deployed |
| pedestrianaccidentlawyer.net | Pedestrians | 400 | ✅ Deployed |
| cyclistaccidentlawyer.com | Cyclists | 619 | ✅ Deployed |
| uberlawyersnearme.com | Uber | 302 | ✅ Deployed |
| ridesharelawyersnearme.com | Rideshare | 301 | ✅ Deployed |
| lyftcrashlaw.com | Lyft | 302 | ✅ Deployed |
| hitandrunlawyer.net | Hit & run | 300+ | ✅ Deployed |
| deliverytruckaccident.com | Delivery trucks | 307 | ✅ Deployed |

---

## 13. Quick Reference Commands

```bash
# Start development server
npm run dev

# Build static site
npm run build

# Count generated pages
find out -name "*.html" | wc -l

# Deploy to Cloudflare
CLOUDFLARE_API_TOKEN=$(cat ~/.config/cloudflare/credentials.json | python3 -c "import sys,json; print(json.load(sys.stdin)['api_token'])") npx wrangler pages deploy ./out --project-name=YOUR-PROJECT

# Validate JSON files
cat data/cities.json | python3 -m json.tool > /dev/null && echo "Valid" || echo "Invalid"

# Check for TypeScript errors
npx tsc --noEmit
```

---

## Appendix A: Expanding Cities Data

To add more cities to your site:

### Option 1: Find City Data Online
- SimpleMaps US Cities Database (free tier)
- US Census Bureau data
- Wikipedia lists

### Option 2: Generate Programmatically
```bash
# Use a script to fetch and format city data
# Example sources:
# - SimpleMaps: https://simplemaps.com/data/us-cities
# - GeoDB Cities API
```

### Required Fields Per City
```json
{
  "city": "City Name",
  "state": "Full State Name", 
  "stateCode": "XX",
  "slug": "city-name-slugified",
  "population": 123456,
  "lat": 12.3456,
  "lng": -12.3456
}
```

---

*Version 2.0 | Updated: 2026-02-12*
*For: Kurios Brand / MVA Lead Gen*
*Changes: Added prerequisites, detailed commands, troubleshooting, verification steps*

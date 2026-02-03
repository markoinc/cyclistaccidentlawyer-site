# RB2B Setup for Kurios Sites

## Sites to Add
1. kuriosbrand.com
2. leads.kuriosbrand.com

## RB2B Free Tier
- 150 credits/month (free forever after 7-day trial)
- LinkedIn profiles + company data
- Sends to Slack in real-time
- US visitors only (GDPR compliant)

## Setup Steps

### 1. Create RB2B Account
Go to: https://app.rb2b.com/signup
Use: mark@kuriosbrand.com

### 2. Get Script
After signup, you'll get a tracking script like:
```html
<script>
!function(){var e=window.RB2B=window.RB2B||[];if(!e.invoked){e.invoked=!0;e.methods=["identify","track","page"];e.factory=function(t){return function(){var n=Array.prototype.slice.call(arguments);n.unshift(t);e.push(n);return e}};for(var t=0;t<e.methods.length;t++){var n=e.methods[t];e[n]=e.factory(n)}e.load=function(e){var t=document.createElement("script");t.type="text/javascript";t.async=!0;t.src="https://tracking.rb2b.com/script.js";var n=document.getElementsByTagName("script")[0];n.parentNode.insertBefore(t,n)};e.SNIPPET_VERSION="1.0.1";e.load("YOUR_SITE_ID")}}();
</script>
```

### 3. Add to Sites
Add script to `<head>` section of:
- kuriosbrand.com (main site)
- leads.kuriosbrand.com (landing page)

### 4. Connect Slack
- In RB2B dashboard → Integrations → Slack
- Connect your workspace
- Choose channel for notifications

### 5. What You'll See
When a US visitor lands on your site:
- Their LinkedIn profile
- Company name
- Job title
- Email (on paid plans)
- Pages viewed

## Cheaper Alternatives
If you need more credits:

1. **Leadfeeder by Dealfront** - Company-level only, $99/mo
2. **Snitcher** - €99/mo, unlimited storage
3. **Warmly** - Similar to RB2B, $700/mo (more expensive)
4. **Clearbit Reveal** - Enterprise pricing

## Recommendation
Start with RB2B free tier (150/month). If you get more than 150 identified visitors, upgrade to $149/mo.

## Integration Ideas
- Send hot leads to Telegram via Zapier
- Auto-add to GHL/CRM
- Trigger outreach sequence

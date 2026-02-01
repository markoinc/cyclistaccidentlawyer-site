# Sierra Command Center

Modern dashboard for KuriosBrand business operations.

## Features

- 🎯 **Daily Action Items** - What needs to happen TODAY
- 🔥 **Sales Pipeline** - With close probabilities
- ⚡ **Opportunities** - Cost savings and growth potential
- 📈 **Growth Tracking** - Initiative progress
- 💰 **Unit Economics** - MVA funnel metrics
- 🤖 **Agent Status** - Sierra & SCOUT monitoring
- 🔒 **Simple Auth** - Password gate (or Cloudflare Access)

## Access Codes

- `sierra2026` - Primary access code
- `kurios` - Alternate access code

## Deployment to Cloudflare Pages

### Option 1: Direct Upload

1. Go to [Cloudflare Pages](https://dash.cloudflare.com/?to=/:account/pages)
2. Click "Create a project" → "Direct Upload"
3. Upload the contents of this folder
4. Your dashboard will be live at `https://your-project.pages.dev`

### Option 2: Git Integration

1. Push this folder to a GitHub/GitLab repo
2. Connect the repo to Cloudflare Pages
3. Set build output directory to `/` (root)
4. No build command needed (static files)

### Option 3: Wrangler CLI

```bash
# Install wrangler if needed
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
cd dashboard-app
wrangler pages deploy . --project-name sierra-dashboard
```

## Adding Cloudflare Access (Recommended)

For production use, enable Cloudflare Access:

1. Go to Cloudflare Zero Trust → Access → Applications
2. Create new application "Self-hosted"
3. Set application domain to your Pages URL
4. Add authentication policy (email OTP, Google, etc.)

This provides:
- Zero-trust authentication
- SSO integration
- Audit logging
- No password in code

## Updating Data

The dashboard loads from `data.json`. Update this file with:
- New pipeline leads
- Action items
- Growth progress
- Opportunities

## File Structure

```
dashboard-app/
├── index.html      # Main dashboard HTML
├── app.js          # Dashboard logic
├── data.json       # Business data
├── calendar.json   # Calendar events (optional)
├── _headers        # Security headers
├── _redirects      # Cloudflare redirects
└── README.md       # This file
```

## Customization

### Change Access Code
Edit `app.js` and modify the authentication check in `checkAuth()`:

```javascript
if (password === 'your-new-code') {
```

### Add More Sections
The dashboard is modular. Add new sections in `index.html` and corresponding render functions in `app.js`.

### Theme Colors
Colors are defined in the Tailwind config in `index.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                dark: { ... },
                brand: { ... }
            }
        }
    }
}
```

## Mobile Support

The dashboard is fully responsive:
- Desktop: Full 3-column layout
- Tablet: 2-column layout
- Mobile: Single column, touch-friendly

---

Built with ❤️ by Sierra for KuriosBrand

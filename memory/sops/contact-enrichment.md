# Contact Enrichment for Agreements SOP

**Created:** 2026-02-03
**Last Updated:** 2026-02-03

## Purpose
Enrich prospect contacts from Google Sheets with all info needed to fill out lead generation agreements.

---

## Data Sources

### Primary: Google Sheets
- **Kurios MVA Appointments**: `1iu8lHRKAt_eDoHr6SreDktQhwT8l0R-VFpfvObKHtMQ`
- Contains: Name, Phone, Email, Firm Website, Status, Needs, Notes

### Secondary: Web Enrichment
- Firm websites (address, legal entity name)
- State bar lookups (bar numbers, license verification)
- Yelp/Google/SuperLawyers (addresses)
- LinkedIn (background verification)

---

## Required Fields for Agreement

### Must Have
- [ ] Client legal entity name (LLC, PC, PLLC, etc.)
- [ ] Full business address (street, city, state, ZIP)
- [ ] Primary contact full name
- [ ] Primary contact phone
- [ ] Primary contact email
- [ ] States/jurisdictions for campaign
- [ ] Budget amount
- [ ] Payment method

### Nice to Have
- [ ] State bar number(s)
- [ ] Firm website
- [ ] Intake contact (if different from primary)
- [ ] Special requirements/qualifiers

---

## Enrichment Process

### Step 1: Pull from Google Sheets
```python
sheet_id = '1iu8lHRKAt_eDoHr6SreDktQhwT8l0R-VFpfvObKHtMQ'
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A:Z'
```

### Step 2: Web Scrape Firm Websites
- Look for: Contact page, About page, Footer
- Extract: Address, legal entity name, phone

### Step 3: Search for Missing Data
- Use web_search for "[Firm Name] [City] address"
- Check Yelp, SuperLawyers, state bar directories

### Step 4: Compile into JSON
Save to: `/home/ec2-user/clawd/data/contacts-enriched-for-agreements.json`

---

## State Bar Lookup Resources

| State | Directory |
|-------|-----------|
| Texas | texasbar.com |
| California | apps.calbar.ca.gov |
| Michigan | sbm.reliaguide.com |
| Nevada | nvbar.org |
| Virginia | vsb.org |
| Georgia | gabar.org |

---

## Output Format

```json
{
  "name": {"first": "", "last": "", "full": ""},
  "firm": {"name": "", "legal_entity": "", "website": ""},
  "contact": {"phone": "", "email": ""},
  "address": {"street": "", "city": "", "state": "", "zip": ""},
  "states_licensed": [],
  "bar_number": "",
  "deal": {"budget": "", "states": [], "model": "", "target_cpa": ""},
  "agreement_fields_needed": [],
  "ghl_contact_id": ""
}
```

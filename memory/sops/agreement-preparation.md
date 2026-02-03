# Agreement Preparation SOP

**Created:** 2026-02-03
**Source:** Agreement templates + contact enrichment work

---

## Agreement Types

Located at `/home/ec2-user/clawd/data/agreements/`:
- `lead-gen-agreement-raw-leads.md` — Form fill leads
- `lead-gen-agreement-live-transfers.md` — Transfers
- `lead-gen-agreement-signed-cases.md` — Full-service signed cases

---

## Required Fields for Agreement

### Must Have (Contact Enrichment)
- [ ] Client legal entity name (LLC, PC, PLLC, etc.)
- [ ] Full business address (street, city, state, ZIP)
- [ ] Primary contact full name
- [ ] Primary contact phone
- [ ] Primary contact email
- [ ] State bar number(s)
- [ ] States/jurisdictions for campaign
- [ ] Budget amount

### Deal-Specific
- [ ] Service tier (leads/transfers/cases)
- [ ] Guaranteed quantities (if $30K+)
- [ ] Case qualification criteria (treatment gap, liability threshold)
- [ ] Delivery method (email, CRM, API)
- [ ] Payment terms

---

## Contact Enrichment Process

1. **Pull from Google Sheets**
   - Sheet: `Kurios MVA Appointments` (ID: `1iu8lHRKAt_eDoHr6SreDktQhwT8l0R-VFpfvObKHtMQ`)
   - Has: Name, phone, email, firm website, status, needs

2. **Web Scrape Firm Websites**
   - Look for: Contact page, About page, Footer
   - Extract: Address, legal entity name, additional phone

3. **State Bar Lookups**
   | State | Directory |
   |-------|-----------|
   | Texas | texasbar.com |
   | California | apps.calbar.ca.gov |
   | Michigan | sbm.reliaguide.com |
   | Nevada | nvbar.org |
   | Virginia | vsb.org |
   | Georgia | gabar.org |

4. **Save to**
   - `/home/ec2-user/clawd/data/contacts-enriched-for-agreements.json`

---

## Agreement Workflow

1. **After positive sales call:**
   - Identify which agreement template to use
   - Check if contact data is complete for agreement

2. **If data missing:**
   - Run contact enrichment
   - Or ask client directly in follow-up email

3. **Fill agreement:**
   - Use merge fields from enriched contact data
   - Customize case criteria based on call notes

4. **Send for signature:**
   - Use GHL or DocuSign
   - CC sierra@kuriosbrand.com and carlos@kuriosbrand.com

---

## Case Qualification Defaults

| Criteria | Standard |
|----------|----------|
| Liability | <50% comparative fault |
| Treatment | Within 21 days of accident |
| Representation | Not currently represented OR switching |
| Injury | Physical injury requiring treatment |
| Insurance | Confirmed coverage |
| Recency | Accident within past 2-3 months |
| Age | 18+ or guardian signing |

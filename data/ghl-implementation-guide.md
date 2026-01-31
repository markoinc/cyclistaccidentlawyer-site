# Carlos Sales Flow - GoHighLevel Implementation Guide

**Created:** 2026-01-30  
**Purpose:** Complete technical implementation guide for building the Carlos Sales Flow in GoHighLevel

---

## Table of Contents
1. [Flow Overview](#flow-overview)
2. [GHL Triggers Required](#1-ghl-triggers-required)
3. [GHL Actions Required](#2-ghl-actions-required)
4. [Pipeline Stages](#3-pipeline-stages-required)
5. [Workflow Breakdown](#4-workflow-breakdown)
6. [Step-by-Step Implementation Checklist](#5-step-by-step-implementation-checklist)

---

## Flow Overview

```
LEAD FORM RECEIVED
        │
        ├─── [Booked Call = YES] ──→ PATH A (Appointment Flow)
        │
        └─── [Booked Call = NO] ───→ PATH B (Booking Nurture Flow)
```

### Path A - Booked Call "Yes"
1. Send Reminder Text 24, 3, and 1 hours prior
2. Send Email confirming appointment  
3. Send Video Explainer / Collateral
4. Create deal in Sales Pipeline + Automated Task
5. Sales Call Outcomes:
   - **No Show** → Rebook sequence (3 phone, 3 email) → If no rebook → Close Lost + Nurture
   - **Agrees to Test = Yes** → DocuSign → Follow-ups until signed → Closed Won + Welcome Pack + Invoice + Notify COD
   - **Agrees to Test = No** → Second call/info → If still No → Close Lost + Nurture

### Path B - Booked Call "No"  
1. Send email reminding to book call
2. If still No → 3 email, 3 text, 2 phone sequence
3. If Yes → Books call → Returns to Path A

---

## 1. GHL Triggers Required

### Primary Triggers

| # | Trigger | GHL Name | Filter/Condition | Used In |
|---|---------|----------|------------------|---------|
| T1 | Lead Form Submitted | `Form Submitted` | Filter by specific form name | WF1: Lead Intake |
| T2 | Appointment Booked | `Customer Booked Appointment` | Filter by Sales Call calendar | WF2: Appointment Confirmation |
| T3 | Appointment Status Changed | `Appointment Status` | Status = No-show | WF4: No-Show Rebook |
| T4 | Appointment Status Changed | `Appointment Status` | Status = Showed/Completed | WF5: Post-Call Handler |
| T5 | Pipeline Stage Changed | `Opportunity Stage Changed` | Stage = "Contract Sent" | WF6: DocuSign Follow-up |
| T6 | Document Signed | `Documents & Contracts` | Status = Signed/Completed | WF7: Closed Won |
| T7 | Tag Added | `Contact Tag` | Tag = "Agreed to Test" | WF6: DocuSign Send |
| T8 | Tag Added | `Contact Tag` | Tag = "Declined Test" | WF8: Second Chance |
| T9 | Tag Added | `Contact Tag` | Tag = "Close Lost" | WF9: Nurture Sequence |
| T10 | Stale Opportunity | `Stale Opportunities` | Days in stage > X | WF3: Booking Reminder |

### Trigger Configuration Details

**T1 - Form Submitted**
```
Trigger: Form Submitted
Filter: Form Name = "Carlos Lead Form"
```

**T2 - Customer Booked Appointment**
```
Trigger: Customer Booked Appointment
Filter: In Calendar = "Sales Call Calendar"
```

**T3/T4 - Appointment Status**
```
Trigger: Appointment Status
Filter: Appointment Status = [No-show | Showed]
Filter: In Calendar = "Sales Call Calendar"
```

**T5 - Pipeline Stage Changed**
```
Trigger: Opportunity Stage Changed
Filter: Pipeline = "Carlos Sales Pipeline"
Filter: Stage = "Contract Sent"
```

**T6 - Documents & Contracts**
```
Trigger: Documents & Contracts
Filter: Status = Signed/Completed
Filter: Template = "Carlos Service Agreement"
```

---

## 2. GHL Actions Required

### Communication Actions

| # | Action | GHL Name | Purpose |
|---|--------|----------|---------|
| A1 | Send SMS | `Send SMS` | Reminders at 24h, 3h, 1h |
| A2 | Send Email | `Send Email` | Confirmations, follow-ups, collateral |
| A3 | Voicemail Drop | `Call` (with voicemail) | Phone call attempts |
| A4 | Internal Notification | `Internal Notification` | Notify COD/team |

### CRM Actions

| # | Action | GHL Name | Purpose |
|---|--------|----------|---------|
| A5 | Create Opportunity | `Create Opportunity` | Create deal on form submit |
| A6 | Update Opportunity | `Update Opportunity` | Move stages, update status |
| A7 | Add Task | `Add Task` | Create follow-up tasks |
| A8 | Add/Remove Tag | `Add Contact Tag` / `Remove Contact Tag` | Track contact status |
| A9 | Add Note | `Add Note` | Log activity |

### Document Actions

| # | Action | GHL Name | Purpose |
|---|--------|----------|---------|
| A10 | Send Document | `Send Documents & Contracts` | Send DocuSign/Contract |
| A11 | Send Invoice | `Send Invoice` | Generate invoice on close |

### Flow Control Actions

| # | Action | GHL Name | Purpose |
|---|--------|----------|---------|
| A12 | Wait | `Wait` | Timing delays (24h, 3h, 1h) |
| A13 | If/Else | `If/Else` | Branch logic |
| A14 | Remove from Workflow | `Remove from Workflow` | Stop sequences |
| A15 | Go To | `Go To` | Chain workflows |

---

## 3. Pipeline Stages Required

### Carlos Sales Pipeline

| Stage # | Stage Name | Status | Entry Criteria | Exit Action |
|---------|------------|--------|----------------|-------------|
| 1 | **New Lead** | Open | Form submitted, no booking | Auto-create on form submit |
| 2 | **Call Scheduled** | Open | Appointment booked | Move when booking confirmed |
| 3 | **Call Completed** | Open | Appointment showed | Move when call marked complete |
| 4 | **Proposal/Test Offered** | Open | Discussed test during call | Manual move by rep |
| 5 | **Contract Sent** | Open | Agreed to test, contract sent | Auto-move when DocuSign sent |
| 6 | **Contract Signed** | Open | DocuSign completed | Auto-move when signed |
| 7 | **Closed Won** | Won | Fully executed + invoiced | Auto-move on signature |
| 8 | **Closed Lost** | Lost | Declined after all attempts | Manual or auto after nurture |
| 9 | **Nurture** | Abandoned | Not ready, needs warming | Auto-move after decline |

### Pipeline Configuration
```
Pipeline Name: Carlos Sales Pipeline
Allow Multiple Opportunities: No (one deal per contact)
Default Stage: New Lead
```

### Custom Fields for Opportunities
| Field Name | Type | Options |
|------------|------|---------|
| Call Outcome | Dropdown | Showed, No-Show, Cancelled, Rescheduled |
| Test Decision | Dropdown | Agreed, Declined, Needs Second Call |
| Contract Status | Dropdown | Not Sent, Sent, Viewed, Signed |
| No-Show Count | Number | (auto-increment) |
| Rebook Attempts | Number | (auto-increment) |

---

## 4. Workflow Breakdown

### WF1: Lead Intake & Initial Routing
**Trigger:** Form Submitted (Carlos Lead Form)

```
START
  │
  ├─→ Create Contact (if new)
  ├─→ Create Opportunity (Stage: New Lead)
  ├─→ Add Tag: "New Lead"
  ├─→ Add Task: "Review new lead" (assigned to sales rep)
  │
  └─→ IF/ELSE: Did they book a call?
          │
          ├─→ [YES - has appointment] → Add Tag: "Call Booked"
          │                           → Remove from Workflow
          │                           (WF2 will trigger)
          │
          └─→ [NO - no appointment] → Add Tag: "Needs Booking"
                                    → Send Email: "Book Your Call"
                                    → Wait 24 hours
                                    → Send SMS: "Quick reminder to book"
                                    (WF3 takes over)
END
```

---

### WF2: Appointment Confirmation & Reminders
**Trigger:** Customer Booked Appointment (Sales Call Calendar)

```
START
  │
  ├─→ Update Opportunity Stage → "Call Scheduled"
  ├─→ Add Tag: "Call Booked"
  ├─→ Remove Tag: "Needs Booking"
  │
  ├─→ Send Email: "Appointment Confirmed"
  │     └─→ Include: Date, time, Zoom link, what to expect
  │
  ├─→ Send Email: "Video Explainer & Collateral"
  │     └─→ Attach: Intro video, case studies, FAQ
  │
  ├─→ Add Task: "Prep for sales call with {{contact.name}}"
  │
  ├─→ Wait Until: 24 hours before appointment
  ├─→ Send SMS: "Reminder: Call tomorrow at {{appointment.start_time}}"
  ├─→ Send Email: "Call Tomorrow - Here's What We'll Cover"
  │
  ├─→ Wait Until: 3 hours before appointment
  ├─→ Send SMS: "Your call is in 3 hours! Zoom link: [link]"
  │
  ├─→ Wait Until: 1 hour before appointment
  ├─→ Send SMS: "See you in 1 hour! Click to join: [link]"
  │
END
```

**Wait Configuration:**
```
Wait Until: Event Start Time
Offset: -24 hours / -3 hours / -1 hour
```

---

### WF3: Booking Nurture Sequence (No Booking Path B)
**Trigger:** Tag Added = "Needs Booking" (from WF1)

```
START
  │
  ├─→ Wait 2 days
  ├─→ IF/ELSE: Has Tag "Call Booked"?
  │     ├─→ [YES] → Remove from Workflow (they booked!)
  │     └─→ [NO] → Continue...
  │
  ├─→ Send Email #1: "Still interested? Book your call"
  ├─→ Wait 2 days
  │
  ├─→ Send SMS #1: "Hey {{first_name}}, ready to chat? [booking link]"
  ├─→ Wait 2 days
  │
  ├─→ IF/ELSE: Has Tag "Call Booked"?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Continue...
  │
  ├─→ Send Email #2: "Let's find a time that works"
  ├─→ Wait 2 days
  │
  ├─→ Send SMS #2: "{{first_name}}, quick 15-min call? [link]"
  ├─→ Wait 2 days
  │
  ├─→ Voicemail Drop #1: [Pre-recorded booking reminder]
  ├─→ Wait 3 days
  │
  ├─→ IF/ELSE: Has Tag "Call Booked"?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Continue...
  │
  ├─→ Send Email #3: "Last chance to connect"
  ├─→ Wait 2 days
  │
  ├─→ Send SMS #3: "Final reminder - shall I close your file?"
  ├─→ Wait 3 days
  │
  ├─→ Voicemail Drop #2: [Final attempt voicemail]
  ├─→ Wait 3 days
  │
  ├─→ IF/ELSE: Has Tag "Call Booked"?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Add Tag: "Close Lost - No Booking"
  │              → Update Opportunity Status: Lost
  │              → Add Tag: "Nurture Sequence"
  │              (WF9 takes over)
END
```

**Sequence Summary:**
- 3 Emails (Days 2, 6, 12)
- 3 SMS (Days 4, 8, 14)
- 2 Phone/Voicemail (Days 10, 17)
- Total: 20 days before Close Lost

---

### WF4: No-Show Rebook Sequence
**Trigger:** Appointment Status = No-show

```
START
  │
  ├─→ Add Tag: "No Show"
  ├─→ Update Opportunity Custom Field: No-Show Count +1
  ├─→ Add Note: "No-show on {{appointment.date}}"
  │
  ├─→ Wait 1 hour
  ├─→ Send SMS: "Sorry we missed you! Ready to reschedule? [link]"
  ├─→ Send Email: "We missed you - let's reschedule"
  │
  ├─→ Wait 24 hours
  ├─→ IF/ELSE: Has new appointment?
  │     ├─→ [YES] → Remove Tag: "No Show"
  │     │         → Remove from Workflow
  │     └─→ [NO] → Continue...
  │
  ├─→ Voicemail Drop #1: "Hey, we missed our call..."
  ├─→ Send Email #2: "Second attempt - let's reconnect"
  │
  ├─→ Wait 48 hours
  ├─→ IF/ELSE: Has new appointment?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Continue...
  │
  ├─→ Send SMS #2: "{{first_name}}, one more try?"
  ├─→ Voicemail Drop #2: "Following up on our missed call..."
  │
  ├─→ Wait 48 hours
  ├─→ IF/ELSE: Has new appointment?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Continue...
  │
  ├─→ Send Email #3: "Final attempt to reschedule"
  ├─→ Voicemail Drop #3: "Last attempt to reach you..."
  │
  ├─→ Wait 72 hours
  ├─→ IF/ELSE: Has new appointment?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Add Tag: "Close Lost - No Show"
  │              → Update Opportunity Status: Lost
  │              → Add Tag: "Nurture Sequence"
  │              (WF9 takes over)
END
```

**Sequence Summary:**
- 3 Emails (1h, 24h, 5 days)
- 2 SMS (1h, 3 days)  
- 3 Phone/Voicemail (24h, 3 days, 5 days)
- Total: ~8 days before Close Lost

---

### WF5: Post-Call Handler (Call Completed)
**Trigger:** Appointment Status = Showed/Completed

```
START
  │
  ├─→ Update Opportunity Stage → "Call Completed"
  ├─→ Remove Tag: "Call Booked"
  ├─→ Add Note: "Sales call completed {{appointment.date}}"
  ├─→ Add Task: "Log call outcome for {{contact.name}}"
  │
  ├─→ Send Email: "Great speaking with you!"
  │     └─→ Include: Recap, next steps, contact info
  │
  ├─→ [MANUAL STEP: Sales rep updates Test Decision field]
  │
END

Note: This workflow ends and waits for manual input.
Sales rep must update "Test Decision" custom field to:
- "Agreed" → Triggers WF6 (DocuSign)
- "Declined" → Triggers WF8 (Second Chance)
- "Needs Second Call" → Triggers separate booking flow
```

**Alternative: Tag-Based Routing**
Rep adds tag manually after call:
- `Agreed to Test` → WF6
- `Declined Test` → WF8
- `Needs Second Call` → Custom WF

---

### WF6: DocuSign/Contract Sequence
**Trigger:** Tag Added = "Agreed to Test" OR Stage Changed to "Contract Sent"

```
START
  │
  ├─→ Update Opportunity Stage → "Contract Sent"
  ├─→ Add Tag: "Contract Pending"
  │
  ├─→ Send Documents & Contracts
  │     └─→ Template: "Carlos Service Agreement"
  │     └─→ Send via: Email + SMS notification
  │
  ├─→ Internal Notification: "Contract sent to {{contact.name}}"
  │
  ├─→ Wait 24 hours
  ├─→ IF/ELSE: Document Status = Signed?
  │     ├─→ [YES] → Remove from Workflow (WF7 handles)
  │     └─→ [NO] → Continue...
  │
  ├─→ Send SMS: "Did you get a chance to review the agreement?"
  ├─→ Send Email: "Quick reminder: Agreement awaiting signature"
  │
  ├─→ Wait 48 hours
  ├─→ IF/ELSE: Document Status = Signed?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Continue...
  │
  ├─→ Send Email: "Any questions about the agreement?"
  │
  ├─→ Wait 48 hours
  ├─→ IF/ELSE: Document Status = Signed?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Continue...
  │
  ├─→ Voicemail Drop: "Following up on the agreement..."
  ├─→ Send SMS: "Ready to move forward? [signing link]"
  │
  ├─→ Wait 72 hours
  ├─→ IF/ELSE: Document Status = Signed?
  │     ├─→ [YES] → Remove from Workflow
  │     └─→ [NO] → Internal Notification: "Contract stale - manual follow-up needed"
  │              → Add Task: "Manual follow-up: unsigned contract"
END
```

**Follow-up Cadence:**
- Day 1: Contract sent
- Day 2: SMS + Email reminder
- Day 4: Email check-in
- Day 6: Voicemail + SMS
- Day 9: Escalate to manual

---

### WF7: Closed Won Sequence
**Trigger:** Documents & Contracts Status = Signed/Completed

```
START
  │
  ├─→ Update Opportunity Stage → "Closed Won"
  ├─→ Update Opportunity Status → "Won"
  ├─→ Remove Tag: "Contract Pending"
  ├─→ Add Tag: "Customer"
  │
  ├─→ Internal Notification: "🎉 DEAL WON: {{contact.name}} signed!"
  │     └─→ Send to: COD, Sales Manager
  │
  ├─→ Send Email: "Welcome Pack"
  │     └─→ Include: Onboarding docs, what to expect, contacts
  │
  ├─→ Send Invoice
  │     └─→ Template: "Carlos Service Invoice"
  │     └─→ Amount: {{opportunity.value}}
  │
  ├─→ Add Task: "Onboarding kickoff with {{contact.name}}"
  │     └─→ Due: 3 business days
  │     └─→ Assign: Onboarding team
  │
  ├─→ Wait 1 day
  ├─→ Send SMS: "Welcome aboard! Check your email for next steps."
  │
  ├─→ Add Note: "Contract signed {{date}}. Invoice sent."
  │
END
```

---

### WF8: Second Chance / Declined Handler
**Trigger:** Tag Added = "Declined Test"

```
START
  │
  ├─→ Update Opportunity Stage → "Proposal/Test Offered"
  ├─→ Add Task: "Follow up: {{contact.name}} declined initially"
  │
  ├─→ Wait 2 days
  ├─→ Send Email: "More information about the test"
  │     └─→ Include: Case studies, FAQ, objection handling
  │
  ├─→ Wait 3 days
  ├─→ Send SMS: "Happy to answer any questions - call me anytime"
  │
  ├─→ Wait 5 days
  ├─→ Send Email: "Second call offer"
  │     └─→ Include: Booking link for follow-up call
  │
  ├─→ Wait 7 days
  ├─→ IF/ELSE: Has Tag "Agreed to Test" OR new appointment?
  │     ├─→ [YES] → Remove from Workflow (back to main flow)
  │     └─→ [NO] → Continue...
  │
  ├─→ Voicemail Drop: "Checking in one more time..."
  │
  ├─→ Wait 5 days
  ├─→ IF/ELSE: Any engagement?
  │     ├─→ [YES] → Add Task: "Re-engage {{contact.name}}"
  │     └─→ [NO] → Add Tag: "Close Lost - Declined"
  │              → Update Opportunity Status: Lost
  │              → Add Tag: "Nurture Sequence"
  │              (WF9 takes over)
END
```

---

### WF9: Long-Term Nurture Sequence
**Trigger:** Tag Added = "Nurture Sequence"

```
START
  │
  ├─→ Update Opportunity Stage → "Nurture"
  ├─→ Remove Tags: "Close Lost - No Booking", "Close Lost - No Show", etc.
  │
  ├─→ Wait 7 days
  ├─→ Send Email: "Valuable content #1" (no sales pitch)
  │
  ├─→ Wait 14 days
  ├─→ Send Email: "Case study / success story"
  │
  ├─→ Wait 14 days
  ├─→ Send Email: "Industry insights"
  │
  ├─→ Wait 14 days
  ├─→ Send SMS: "Quick update - would you like to reconnect?"
  │
  ├─→ Wait 14 days
  ├─→ Send Email: "New offering / update announcement"
  │
  ├─→ Wait 30 days
  ├─→ Send Email: "Quarterly check-in"
  │     └─→ Include booking link
  │
  ├─→ [Loop continues quarterly with value content]
  │
END
```

**Nurture Cadence:**
- Week 1: Value email
- Week 3: Case study
- Week 5: Insights
- Week 7: SMS check-in
- Week 9: Announcement
- Monthly: Quarterly check-ins

---

## 5. Step-by-Step Implementation Checklist

### Phase 1: Foundation Setup (Day 1)

- [ ] **1.1 Create Pipeline**
  - Go to: Opportunities → Pipelines
  - Create "Carlos Sales Pipeline"
  - Add stages in order:
    1. New Lead
    2. Call Scheduled
    3. Call Completed
    4. Proposal/Test Offered
    5. Contract Sent
    6. Contract Signed
    7. Closed Won
    8. Closed Lost
    9. Nurture

- [ ] **1.2 Create Custom Fields (Opportunities)**
  - Go to: Settings → Custom Fields → Opportunities
  - Add:
    - Call Outcome (Dropdown)
    - Test Decision (Dropdown)
    - Contract Status (Dropdown)
    - No-Show Count (Number)
    - Rebook Attempts (Number)

- [ ] **1.3 Create Contact Tags**
  - New Lead
  - Needs Booking
  - Call Booked
  - No Show
  - Agreed to Test
  - Declined Test
  - Contract Pending
  - Close Lost - No Booking
  - Close Lost - No Show
  - Close Lost - Declined
  - Nurture Sequence
  - Customer

- [ ] **1.4 Set Up Calendar**
  - Go to: Calendars → Add Calendar
  - Name: "Sales Call Calendar"
  - Duration: 30/45/60 min (as needed)
  - Availability: Set business hours
  - Generate booking link

---

### Phase 2: Documents & Templates (Day 2)

- [ ] **2.1 Create Contract Template**
  - Go to: Payments → Documents & Contracts → Templates
  - Create: "Carlos Service Agreement"
  - Add fields: Contact name, date, signature
  - Configure payment collection if needed

- [ ] **2.2 Create Invoice Template**
  - Go to: Payments → Invoices → Templates
  - Create: "Carlos Service Invoice"

- [ ] **2.3 Create Email Templates**
  - Appointment Confirmation
  - Video Explainer / Collateral Email
  - 24h Reminder
  - 3h Reminder
  - 1h Reminder
  - No-Show Follow-up (x3)
  - Contract Sent
  - Contract Reminder (x3)
  - Welcome Pack
  - Booking Reminder (x3)
  - Nurture Series (x5)

- [ ] **2.4 Create SMS Templates**
  - Appointment Confirmation
  - 24h Reminder
  - 3h Reminder
  - 1h Reminder
  - No-Show SMS (x2)
  - Contract Reminder (x2)
  - Booking Reminder (x3)
  - Nurture Check-in

- [ ] **2.5 Record Voicemail Drops**
  - Booking reminder voicemail (x2)
  - No-show voicemail (x3)
  - Contract follow-up voicemail
  - Format: MP3, 64kbps

---

### Phase 3: Build Workflows (Days 3-5)

Build in this order (dependencies matter):

- [ ] **3.1 WF9: Nurture Sequence** (no dependencies)
- [ ] **3.2 WF7: Closed Won** (no dependencies)
- [ ] **3.3 WF6: DocuSign Sequence** (depends on WF7)
- [ ] **3.4 WF8: Second Chance** (depends on WF9)
- [ ] **3.5 WF5: Post-Call Handler** (depends on WF6, WF8)
- [ ] **3.6 WF4: No-Show Rebook** (depends on WF9)
- [ ] **3.7 WF2: Appointment Confirmation** (depends on WF4)
- [ ] **3.8 WF3: Booking Nurture** (depends on WF9)
- [ ] **3.9 WF1: Lead Intake** (depends on WF2, WF3)

---

### Phase 4: Testing (Day 6)

- [ ] **4.1 Test Lead Form → No Booking Path**
  - Submit test form (no appointment)
  - Verify: Contact created, opportunity created, tag added
  - Verify: Email received
  - Fast-forward and check sequence timing

- [ ] **4.2 Test Lead Form → Booking Path**
  - Submit form + book appointment
  - Verify: Stage moves to "Call Scheduled"
  - Verify: Confirmation email + video email received
  - Test reminder sequence (manually adjust times)

- [ ] **4.3 Test No-Show Flow**
  - Mark test appointment as No-show
  - Verify: Rebook sequence triggers
  - Test through all attempts

- [ ] **4.4 Test Agreed to Test Flow**
  - Add "Agreed to Test" tag to test contact
  - Verify: Contract sends
  - Simulate signature
  - Verify: Closed Won flow + invoice

- [ ] **4.5 Test Declined Flow**
  - Add "Declined Test" tag
  - Verify: Second chance sequence
  - Let it run to Nurture

---

### Phase 5: Go Live (Day 7)

- [ ] **5.1 Publish All Workflows**
  - Review each workflow
  - Change from Draft → Published

- [ ] **5.2 Connect Lead Form**
  - Embed/link form on landing page
  - Ensure form trigger is configured

- [ ] **5.3 Team Training**
  - Train sales reps on:
    - Marking appointment outcomes
    - Adding correct tags after calls
    - Monitoring pipeline

- [ ] **5.4 Set Up Notifications**
  - Configure Internal Notification recipients
  - Add COD email for closed won alerts

- [ ] **5.5 Create Dashboard**
  - Pipeline overview widget
  - Won/Lost opportunities
  - Conversion by stage
  - No-show rate

---

## Quick Reference: Trigger → Workflow Map

| Event | Trigger | Workflow |
|-------|---------|----------|
| Form submitted | Form Submitted | WF1: Lead Intake |
| Call booked | Customer Booked Appointment | WF2: Appointment Confirmation |
| Needs booking (no call) | Tag: Needs Booking | WF3: Booking Nurture |
| No-show | Appointment Status: No-show | WF4: No-Show Rebook |
| Call completed | Appointment Status: Showed | WF5: Post-Call Handler |
| Agreed to test | Tag: Agreed to Test | WF6: DocuSign Sequence |
| Contract signed | Document: Signed | WF7: Closed Won |
| Declined test | Tag: Declined Test | WF8: Second Chance |
| Lost → Nurture | Tag: Nurture Sequence | WF9: Nurture Sequence |

---

## Notes & Best Practices

### Timing Considerations
- **Reminder windows:** 24h, 3h, 1h are best for reducing no-shows
- **Follow-up spacing:** 2-3 days between touches feels persistent but not pushy
- **Voicemail drops:** Space at least 48h apart
- **Nurture:** Monthly touchpoints keep you top of mind without annoying

### Allow Reentry Settings
| Workflow | Allow Reentry |
|----------|---------------|
| WF1: Lead Intake | NO |
| WF2: Appointment Confirmation | YES (per appointment) |
| WF3: Booking Nurture | NO |
| WF4: No-Show Rebook | YES |
| WF5: Post-Call Handler | YES |
| WF6: DocuSign Sequence | NO |
| WF7: Closed Won | NO |
| WF8: Second Chance | NO |
| WF9: Nurture | NO |

### Exit Conditions
Always include IF/ELSE checks before follow-up messages to prevent sending to contacts who've already converted (booked, signed, etc.)

### GHL Limitations
- **No native DocuSign:** Use GHL's built-in Documents & Contracts
- **Voicemail drops:** ~70% success rate, depends on carrier
- **Wait Until:** Can wait until appointment time minus offset

---

## Document Version
- **Version:** 1.0
- **Last Updated:** 2026-01-30
- **Author:** Sierra (AI Assistant)

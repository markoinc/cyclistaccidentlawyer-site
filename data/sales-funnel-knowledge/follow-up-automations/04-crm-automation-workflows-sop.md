# CRM Automation Workflows SOP
## Complete Guide to Automating Sales Pipelines and Customer Journeys

**Source:** Compiled from HubSpot, Salesforce, GoHighLevel, and CRM best practices (2025-2026)  
**Last Updated:** January 2026

---

## What is CRM Automation?

CRM automation combines customer relationship management software with automated workflows that handle repetitive sales, marketing, and customer service tasks without manual intervention.

**Core Benefits:**
- No opportunity missed
- Consistent communication
- Always up-to-date information
- Faster response times
- Better team alignment
- Personalized customer experiences

---

## Why Unified CRM Automation Beats Stitched-Together Tools

| Problem with Multiple Tools | Solution with Unified CRM |
|----------------------------|---------------------------|
| Data silos across systems | Single source of truth |
| Inconsistent segmentation | Same customer insights everywhere |
| Brittle API integrations | Native features that work together |
| Conflicting report numbers | Centralized analytics |
| Multiple subscriptions | Single platform cost |
| Manual data syncing | Automatic data flow |

---

## Essential CRM Automation Features Checklist

### Must-Have Features

- [ ] **Unified Contacts/Companies** - Single source of truth for all customer data
- [ ] **Lead Scoring** - Automated ranking based on likelihood to convert
- [ ] **Lead Routing** - Instant assignment to right rep based on rules
- [ ] **Sequences/Workflows** - Automated follow-ups and internal processes
- [ ] **Customer Journey Mapping** - Multi-step campaign orchestration
- [ ] **Ticketing Automation** - Service request tracking and routing
- [ ] **Reporting/Analytics** - Unified dashboards across sales, marketing, service
- [ ] **AI Assistance** - Forecasting, content creation, lead qualification
- [ ] **Data Quality/Governance** - Clean data management, permissions, compliance
- [ ] **Extensibility** - Open APIs and app marketplace

---

## Three Revenue-Driving CRM Workflows

### Workflow 1: Marketing-to-Sales Handoff & Lead Routing

**Purpose:** Automatically qualify, score, and assign leads to the right rep

**Workflow Logic:**

```
TRIGGER: Lead captured (form, ad, event)
    ↓
ACTION: Lead scoring evaluates engagement
    ↓
CONDITION: Score threshold met?
    ↓ YES                    ↓ NO
    ↓                        ↓
Mark as "Sales Ready"     Continue nurturing
    ↓
Apply routing rules:
    • By region
    • By product line
    • By availability
    ↓
Assign to rep
    ↓
Trigger follow-up sequence
    ↓
Create task reminder
```

**Implementation Steps:**

1. **Set Up Lead Scoring**
   - Assign points for:
     - Email opens (+1)
     - Link clicks (+3)
     - Website visits (+2)
     - Pricing page view (+10)
     - Demo request form (+25)
     - Content downloads (+5)
   - Subtract points for:
     - No engagement 30 days (-5)
     - Unsubscribes (-20)

2. **Create Qualification Workflow**
   ```
   IF lead_score >= 50 AND
      company_size matches ideal_customer_profile
   THEN
      Mark lifecycle stage = "Sales Qualified Lead"
      Trigger: Marketing-to-Sales Handoff
   ```

3. **Configure Lead Routing Rules**
   - By territory: West Coast → Rep A, East Coast → Rep B
   - By deal size: >$10K → Senior Rep
   - By product interest: Product A → Specialist A
   - Round robin: Equal distribution

4. **Set Up Notifications**
   - Email rep when new lead assigned
   - Slack notification to channel
   - Create follow-up task due in 1 hour

---

### Workflow 2: Service & Success Automation

**Purpose:** Respond quickly, resolve issues, identify upsell opportunities

**Workflow Logic:**

```
TRIGGER: Support ticket submitted
    ↓
ACTION: Create and categorize ticket
    ↓
ROUTE: Based on issue type/priority
    ↓
    ├── Priority: High → Senior Agent + Manager Alert
    ├── Priority: Medium → Next Available Agent
    └── Priority: Low → Queue
    ↓
MONITOR: Resolution time
    ↓
CONDITION: SLA breach approaching?
    ↓ YES                    ↓ NO
    ↓                        ↓
Alert Manager            Continue monitoring
    ↓
TRIGGER (on resolve): Feedback survey
    ↓
CONDITION: Low satisfaction score?
    ↓ YES                    ↓ NO
    ↓                        ↓
Alert success team       Check for upsell opportunity
```

**Implementation Steps:**

1. **Create Ticketing Pipeline**
   - Stages: New → In Progress → Waiting on Customer → Resolved
   - Properties: Priority, Issue Type, SLA Due Date

2. **Set Up Auto-Routing**
   ```
   IF issue_type = "Billing"
   THEN assign to Billing Team
   
   IF issue_type = "Technical" AND priority = "High"
   THEN assign to Senior Tech + CC Manager
   ```

3. **Configure SLA Automation**
   ```
   IF time_since_creation > 4 hours AND status = "New"
   THEN
      Send escalation alert to manager
      Add "Escalated" tag
   ```

4. **Post-Resolution Automation**
   ```
   WHEN ticket status = "Resolved"
   WAIT 2 hours
   THEN
      Send satisfaction survey
      IF response = "Negative"
      THEN create follow-up task for success team
   ```

---

### Workflow 3: Content-Driven Nurture with Personalization

**Purpose:** Warm prospects with relevant content until sales-ready

**Workflow Logic:**

```
TRIGGER: Lead enters nurture segment
    ↓
SEGMENT: By role, industry, or interest
    ↓
DELIVER: Tailored content for segment
    ↓
MONITOR: Engagement
    ↓
BRANCH: Based on behavior
    ├── Clicked product link → Product-specific sequence
    ├── Downloaded case study → Social proof sequence
    └── Visited pricing → Sales alert + qualification sequence
    ↓
SCORE: Update lead score
    ↓
CONDITION: High-intent action detected?
    ↓ YES                    ↓ NO
    ↓                        ↓
Alert sales rep          Continue nurture
Move to "Sales Ready"
```

**Implementation Steps:**

1. **Create Dynamic Segments**
   ```
   Segment: "Marketing Leaders"
   Criteria:
   - Job title contains "Marketing" OR "CMO" OR "VP Marketing"
   - Industry = SaaS OR Technology
   - Engagement score > 20
   ```

2. **Build Personalized Content Tracks**
   
   | Segment | Content Focus | Cadence |
   |---------|---------------|---------|
   | Marketers | Marketing ROI, campaign tips | Weekly |
   | Sales Leaders | Pipeline optimization, closing | Weekly |
   | Technical | Product features, integrations | Bi-weekly |
   | Executives | Strategic insights, ROI | Monthly |

3. **Configure Behavioral Triggers**
   ```
   IF contact views pricing page 2+ times
   THEN
      Alert assigned rep immediately
      Add to "High Intent" segment
      Pause nurture sequence
      
   IF contact downloads case study
   THEN
      Send related case study 3 days later
      Add "Case Study Interest" tag
   ```

4. **Set Up Personalization Tokens**
   - {{first_name}}
   - {{company_name}}
   - {{industry}}
   - {{main_challenge}}
   - {{content_recommendation}}

---

## CRM Workflow Templates

### Template 1: New Lead Assignment

```yaml
Name: New Lead Auto-Assignment
Trigger: Contact created with source = "Website Form"

Actions:
  1. Set property "Lead Status" = "New"
  2. Calculate lead score
  3. IF score >= 50:
       - Set "Lifecycle Stage" = "SQL"
       - Assign to sales rep (round robin)
       - Send Slack notification
       - Create task "Follow up within 1 hour"
     ELSE:
       - Set "Lifecycle Stage" = "MQL"
       - Enroll in nurture sequence
       - Assign to marketing owner
```

### Template 2: Meeting Booked Follow-Up

```yaml
Name: Post-Meeting Booking Automation
Trigger: Meeting booked via calendar link

Actions:
  1. Send confirmation email immediately
  2. WAIT 24 hours before meeting:
       - Send reminder email with prep materials
  3. WAIT 1 hour after meeting ends:
       - Create task "Send meeting follow-up"
       - Update deal stage to "Meeting Completed"
  4. WAIT 24 hours after meeting:
       - IF no deal update:
           - Send automated check-in email
           - Alert rep
```

### Template 3: Deal Stage Progression

```yaml
Name: Deal Stage Automation
Trigger: Deal moves to new stage

Actions by Stage:
  
  Stage: "Discovery"
    - Send discovery prep email to contact
    - Create task "Conduct discovery call"
    - Set close date to 30 days from now
  
  Stage: "Proposal Sent"
    - Log activity "Proposal sent"
    - Set follow-up task for 3 days
    - Start proposal follow-up sequence
    - Alert manager if deal > $10K
  
  Stage: "Negotiation"
    - Remove from automated sequences
    - Alert manager
    - Create task "Prepare final terms"
  
  Stage: "Closed Won"
    - Send welcome/onboarding email
    - Create task for customer success
    - Update contact lifecycle = "Customer"
    - Log revenue in reporting
  
  Stage: "Closed Lost"
    - Send "sorry to see you go" email
    - Add to re-engagement list (6 months)
    - Log lost reason
    - Request feedback survey
```

### Template 4: Re-engagement Campaign

```yaml
Name: Cold Lead Re-engagement
Trigger: Contact with no activity in 90 days

Actions:
  1. Remove from active nurture sequences
  2. Add to "Re-engagement" list
  3. Send Email 1: "We haven't heard from you"
  4. WAIT 5 days
  5. IF no engagement:
       - Send Email 2: "Here's what you missed"
  6. WAIT 5 days
  7. IF no engagement:
       - Send Email 3: Special offer
  8. WAIT 7 days
  9. IF no engagement:
       - Send Email 4: "Should we part ways?"
  10. WAIT 7 days
  11. IF no engagement:
       - Move to "Inactive" list
       - Remove from marketing emails
  12. IF any engagement at any point:
       - Move back to active nurture
       - Alert assigned owner
```

---

## No-Show Follow-Up Automation

### Why It Matters
- 20-30% of scheduled calls result in no-shows
- Quick follow-up can recover 30-50% of no-shows
- Demonstrates professionalism and persistence

### No-Show Workflow

```
TRIGGER: Meeting time passes + contact didn't join
    ↓
WAIT: 5 minutes (confirm they're not running late)
    ↓
CHECK: Did they join late?
    ↓ YES                    ↓ NO
    ↓                        ↓
Mark as attended         Continue no-show flow
    ↓
IMMEDIATELY:
    - Send "Sorry we missed you" email
    - Include link to reschedule
    ↓
WAIT: 2 hours
    ↓
CHECK: Did they respond or reschedule?
    ↓ YES                    ↓ NO
    ↓                        ↓
Remove from flow         Send follow-up #2
                        (different tone, same ask)
    ↓
WAIT: 1 day
    ↓
CHECK: Did they respond?
    ↓ YES                    ↓ NO
    ↓                        ↓
Remove from flow         Alert rep + create task
    ↓
WAIT: 3 days
    ↓
Send final attempt email
    ↓
Mark contact as "Unresponsive"
```

### No-Show Email Templates

**Email 1 - Immediate (5 mins after no-show):**
```
Subject: Missed you on our call – let's reschedule

Hi {{first_name}},

I was looking forward to our call but didn't see you join.

No worries—things come up! Here's my calendar link to grab another time that works better:

[Reschedule Link]

If something changed or you have questions, just reply here.

Talk soon,
{{sender_name}}
```

**Email 2 - 2 hours later:**
```
Subject: Quick note about rescheduling

Hi {{first_name}},

Just a quick follow-up on our missed call earlier.

I know schedules get crazy. Here's that link again to find a new time:

[Reschedule Link]

Looking forward to connecting!

{{sender_name}}
```

**Email 3 - 1 day later:**
```
Subject: Should we try again?

Hi {{first_name}},

I wanted to reach out one more time about rescheduling our call.

If the timing isn't right anymore, no problem—just let me know.

Otherwise, I'd still love to chat about [topic/value proposition].

Here's my calendar: [Link]

Best,
{{sender_name}}
```

---

## Implementation Checklist

### Phase 1: Foundation (Week 1-2)
- [ ] Audit current manual processes
- [ ] Define workflow goals and KPIs
- [ ] Map customer journey stages
- [ ] Set up lead scoring model
- [ ] Configure user permissions

### Phase 2: Core Workflows (Week 3-4)
- [ ] Build lead assignment workflow
- [ ] Create basic nurture sequence
- [ ] Set up meeting booking automation
- [ ] Configure deal stage automations
- [ ] Test all workflows end-to-end

### Phase 3: Advanced (Week 5-6)
- [ ] Add behavioral triggers
- [ ] Implement re-engagement sequences
- [ ] Set up no-show automation
- [ ] Configure SLA/escalation rules
- [ ] Build reporting dashboards

### Phase 4: Optimization (Ongoing)
- [ ] Monitor workflow performance weekly
- [ ] A/B test email content
- [ ] Refine lead scoring based on data
- [ ] Clean up and update automations quarterly
- [ ] Train team on new features

---

## Common CRM Automation Mistakes

| Mistake | Impact | Solution |
|---------|--------|----------|
| Over-automation | Robotic experience | Keep personal touches for key moments |
| No documentation | Workflows break, no one knows why | Document every workflow and owner |
| Complex branching | Hard to debug | Start simple, add complexity gradually |
| No exit conditions | Contacts stuck in loops | Always define how/when to exit |
| Ignoring data quality | Bad automation decisions | Clean data monthly, validate inputs |
| Set and forget | Workflows become outdated | Review quarterly |

---

## Measuring CRM Automation Success

### Key Metrics

| Metric | What It Measures | Target |
|--------|-----------------|--------|
| Lead Response Time | Speed of first contact | < 5 minutes |
| Lead-to-SQL Rate | Nurture effectiveness | 15-25% |
| Pipeline Velocity | Deal progression speed | Improving monthly |
| Sales Cycle Length | Time to close | Decreasing |
| CSAT/NPS | Customer satisfaction | > 70 NPS |
| Automation Error Rate | Workflow reliability | < 1% |

### ROI Calculation

```
Time Saved = Hours saved per week × Weeks × Hourly cost
Revenue Impact = Additional deals closed × Average deal value
CRM Cost = Monthly subscription × Months

ROI = (Time Saved + Revenue Impact - CRM Cost) / CRM Cost × 100
```

# GHL Workflow Analysis
**Date:** 2026-01-30

## PUBLISHED (Active) Workflows

| Workflow | Purpose | Last Updated |
|----------|---------|--------------|
| **Cold Call Status** | Manages cold call pipeline stages | Jan 14 |
| **Facebook lead form submitted** | Processes FB ad leads | Jan 12 |
| **LP Client Acquisition Data Flow Update** | Client acquisition tracking | Jan 20 |
| **Lead Booked Appointment** | When lead books call | **Jan 30** (TODAY) |
| **New Inbound Lead - Create Contact** | Creates contacts from inbound | Jan 12 |
| **Onboarding Email Sequence - Follow Up** | Follow up after onboarding | Jan 12 |
| **Onboarding Summary To Notes** | Logs onboarding data | Jan 12 |
| **Power Dialer** | Auto-dialing leads | Jan 12 |

## DRAFT Workflows (Not Active)

### AI/Conversational
- 1. Conversational AI (GPT)
- 2. Conversational AI (GPT) - Looping
- AI Calling - Auto Dial - Inbound (24/7)
- AI Calling - Auto Dial - Outbound (8AM-9PM)
- AI Custom Fields Update
- AI Moderate - Response Category Classification
- AI Time Detect & Call Back Time Update
- AI Trigger - Stop AI Workflows (x2)
- Appointment Booking AI

### Lead Distribution
- 1. Lead Distribution (Email + SMS Only)
- 1. Lead Distribution (Webhook + Email + SMS)
- 1. Lead Distribution (Webhook Only)

### Appointment Management
- 1:1 Call Reminders
- Appointment No Show Nurture
- Appointment or Call Back Requested - Remove Lead from Workflows
- Appointment: Agent Positioning & Meeting Reminders
- Appointment: Meeting Reminders
- Appointment: Meeting Reminders - (Rescheduler)

### Call Handling
- Call Lead Now Workflow
- Call Not Answered
- Incoming Call Completed - Stop Workflows
- Outgoing Call Completed - Stop Workflows
- Pre Call: Notify Lead (Instant Call Back)
- Pre-Call: Notify Lead about Call

### Email/Nurture
- Customer Replied - START - Resubscribe
- Customer Replied - Stop Campaigns
- Email Unsubscribe
- Follow Up Emails (Goal: Book Appointment)
- Long Term Nurture

### Pipeline/Opportunity
- Opportunity Moved - Stop Workflows
- Sold - Remove from Workflows

### Onboarding
- Onboarding Sequence - email 1
- Welcome Kit - After Onboarding

### Other
- 2. AI Infrastructure Demo for Clients
- Booked Call FBConversion
- Chat Widget Internal Notifs
- Lead Reactivated - Distribute to Client
- New Lead Segmentation (from ClientUp Exchange)
- Post Sale Review Request
- Remove Test Leads
- Website Visitor Prospecting
- Various "Update Insurance Type" workflows (6)
- Update Date of Birth

## KEY WORKFLOWS FOR SALES - LEADS PIPELINE

Based on Carlos's video, we need these for the Sales - Leads pipeline:

### Already Exists (need to verify/connect):
1. ✅ **Lead Booked Appointment** - Updated TODAY, likely handles "Call - Booked" stage
2. ⚠️ **Appointment No Show Nurture** - DRAFT, needs activation for "Call - No Show"
3. ⚠️ **Appointment: Meeting Reminders** - DRAFT, needs activation for reminders

### Need to Build/Activate:
1. ❌ **Post-Call Handler** - Route to Contract or Second Call
2. ❌ **Contract Send & Follow-up** - DocuSign sequence
3. ❌ **Closed Won Handler** - Welcome pack, invoice, notify COD
4. ❌ **Long Term Nurture** - EXISTS as draft, connect to Deal Lost

## RECOMMENDATIONS

### Quick Wins (Activate Existing Drafts):
1. Appointment No Show Nurture → connect to "Call - No Show" stage
2. Appointment: Meeting Reminders → connect to "Call - Booked" stage
3. Long Term Nurture → connect to "Deal Lost" stage

### Build New:
1. Post-Call routing workflow (Completed → Contract or 2nd Call)
2. Contract sequence (send + follow-ups)
3. Closed Won automation (welcome + invoice + notify)

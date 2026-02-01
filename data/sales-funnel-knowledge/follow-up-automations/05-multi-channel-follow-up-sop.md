# Multi-Channel Follow-Up Automation SOP
## Guide to Coordinated Email, SMS, and Social Follow-Up Sequences

**Source:** Compiled from Pabbly, Omnisend, Brevo, and multi-channel marketing best practices (2025-2026)  
**Last Updated:** January 2026

---

## Why Multi-Channel Follow-Up?

**Key Statistics:**
- 73% of consumers prefer shopping through multiple channels
- Multi-channel campaigns see 287% higher purchase rate than single-channel
- Customers who interact on multiple channels have 30% higher lifetime value

**The Reality:** Your prospects are everywhere—email, phone, social media, SMS. Meeting them where they are dramatically increases engagement.

---

## Multi-Channel Framework

### Channel Options

| Channel | Best For | Response Time | Cost |
|---------|----------|---------------|------|
| Email | Detailed info, nurturing | 24-48 hours | Low |
| SMS | Urgent, time-sensitive | Minutes | Medium |
| Phone Call | High-value, complex | Immediate | High |
| LinkedIn | B2B, professionals | 24-72 hours | Free/Low |
| WhatsApp | International, casual | Hours | Low |
| Facebook Messenger | B2C, support | Hours | Free |
| Direct Mail | Stand out, high-value | Days | High |

### When to Use Each Channel

**Email:**
- Initial outreach
- Detailed proposals
- Content delivery
- Nurture sequences
- Newsletters

**SMS:**
- Appointment reminders
- Time-sensitive offers
- Cart abandonment
- Quick confirmations
- Event notifications

**Phone:**
- Discovery calls
- Complex negotiations
- High-value accounts
- Urgent issues
- Closing conversations

**LinkedIn:**
- B2B prospecting
- Professional networking
- Content engagement
- Relationship building

---

## Multi-Channel Sequence Design

### Basic Multi-Channel Sequence (7 days)

```
Day 0: Email - Introduction
    ↓
Day 2: LinkedIn - Connection request + note
    ↓
Day 4: Email - Value add/follow-up
    ↓
Day 5: SMS - Quick check-in (if opted in)
    ↓
Day 7: Phone Call - Personal outreach
    ↓
Day 9: Email - Different angle/case study
    ↓
Day 12: LinkedIn - Engage with their content
    ↓
Day 14: Email - Final follow-up
```

### High-Value Prospect Sequence

```
Day 0: LinkedIn - View profile (creates notification)
Day 1: LinkedIn - Connection request with personalized note
Day 2: Email - Introduction referencing LinkedIn
Day 4: LinkedIn - Comment on their content
Day 5: Email - Value piece (case study)
Day 7: Phone Call - Attempt #1
Day 7: Voicemail + Email combo
Day 10: LinkedIn - Direct message
Day 12: Email - New angle
Day 14: Phone Call - Attempt #2
Day 17: Direct Mail - Physical piece (high value accounts)
Day 21: Email - Breakup message
```

### Cart Abandonment Multi-Channel

```
TRIGGER: Cart abandoned
    ↓
1 hour: Email - "Forgot something?"
    ↓
4 hours: SMS - "Items waiting" (if opted in)
    ↓
24 hours: Email - Social proof + urgency
    ↓
48 hours: Retargeting ads activated
    ↓
72 hours: Email - Limited time discount
    ↓
5 days: SMS - Final discount reminder
```

---

## Channel-Specific Best Practices

### Email Best Practices

**Timing:**
- Best days: Tuesday, Wednesday, Thursday
- Best times: 9-11 AM, 1-3 PM
- Avoid: Monday mornings, Friday afternoons

**Format:**
- Subject line: 30-50 characters
- Body: 50-125 words
- CTA: Single, clear action
- Mobile-optimized design

**Frequency:**
- B2B: 2-3 touches per week max
- B2C: 3-5 per week acceptable
- Adjust based on engagement

### SMS Best Practices

**Legal Requirements:**
- Explicit opt-in required (TCPA, GDPR)
- Easy opt-out in every message
- Business hours only (8 AM - 9 PM)

**Format:**
- Length: 160 characters ideal
- Include business name
- Clear CTA
- Personalize with name

**Sample SMS Templates:**

**Appointment Reminder:**
```
Hi {{name}}! Reminder: Your call with {{company}} is tomorrow at {{time}}. Reply YES to confirm or click here to reschedule: {{link}}
```

**Cart Abandonment:**
```
Hey {{name}}, you left items in your cart! Complete your order now and get free shipping: {{link}} Reply STOP to opt out.
```

**Follow-Up:**
```
Hi {{name}}, {{sender}} from {{company}} here. Did you get a chance to review my email? Quick call this week? Reply with a good time.
```

### LinkedIn Best Practices

**Connection Request Note (300 char max):**
```
Hi {{name}}, I came across your work on {{topic}} and found it really insightful. I'm working on similar challenges at {{company}}. Would love to connect and exchange ideas. - {{your_name}}
```

**Sequencing:**
1. View their profile (day 1)
2. Send connection request (day 2)
3. If accepted, thank them (immediate)
4. Engage with their content (day 4-5)
5. Send value message (day 7)
6. Soft pitch if engaged (day 10+)

**Don'ts:**
- Don't pitch immediately after connecting
- Don't send generic "I'd like to add you to my network"
- Don't spam InMails
- Don't automate everything (engagement should be real)

### Phone/Voicemail Best Practices

**Best Call Times:**
- B2B: 8-9 AM, 4-6 PM
- Wednesday and Thursday perform best
- Avoid Mondays and Friday afternoons

**Voicemail Script (30 seconds max):**
```
"Hi {{name}}, this is {{your_name}} from {{company}}. 

I'm reaching out because [specific reason/trigger]. 

I'm going to send you a quick email with [value proposition], and I'd love to connect for 15 minutes to discuss.

You can reach me at {{phone}}. Again, that's {{phone}}.

Talk soon!"
```

**Always follow voicemail with email:**
```
Subject: Just left you a voicemail

Hi {{name}},

I just tried reaching you by phone. Wanted to follow up here in case email is easier.

[Same value proposition from voicemail]

Would {{day}} at {{time}} work for a quick call?

{{sender_name}}
{{phone}}
```

---

## Multi-Channel Automation Setup

### Tool Stack Options

**All-in-One Platforms:**
- GoHighLevel - SMS, email, calls, social
- HubSpot - Email, calls, social (SMS via integration)
- ActiveCampaign - Email, SMS, site messaging
- Omnisend - Email, SMS, push notifications

**Specialized + Integration:**
- Email: Mailchimp, Klaviyo, MailerLite
- SMS: Twilio, TextMagic, SimpleTexting
- LinkedIn: Expandi, Dux-Soup, PhantomBuster
- Integration: Zapier, Make, Pabbly Connect

### Workflow Design Pattern

```yaml
Multi-Channel Workflow: New Lead Follow-Up

Trigger: New lead from website form

Step 1 - Immediate:
  Channel: Email
  Action: Send welcome email
  Content: Introduction + value prop

Step 2 - 6 hours:
  Condition: Email opened?
  Yes: Skip to Step 4
  No: Continue

Step 3 - 24 hours:
  Channel: SMS (if opted in)
  Action: Send text
  Content: "Got your inquiry! Check your email for details - {{sender}}"

Step 4 - 48 hours:
  Channel: LinkedIn
  Action: Send connection request
  Condition: If LinkedIn URL known

Step 5 - 72 hours:
  Channel: Email
  Action: Send follow-up
  Content: Case study or resource

Step 6 - 5 days:
  Channel: Phone
  Action: Call attempt
  Fallback: Leave voicemail + email combo

Step 7 - 7 days:
  Channel: Email
  Action: Different angle email
  Content: Address common objection

Step 8 - 10 days:
  Condition: Any engagement?
  Yes: Continue personalized follow-up
  No: Move to long-term nurture

Exit Conditions:
  - Reply received
  - Meeting booked
  - Unsubscribe/opt-out
  - Max touches reached (8)
```

---

## Channel Coordination Rules

### Avoid Channel Fatigue

**Daily Limits:**
- Max 1 channel touch per day per contact
- Exception: Email + SMS for time-sensitive (cart abandonment)

**Weekly Limits:**
- Max 3-4 email touches
- Max 2 SMS messages
- Max 2 LinkedIn touches
- Max 2 call attempts

### Timing Coordination

```
RULE: Never send SMS and email within 2 hours of each other
RULE: Wait 24 hours after call before next email
RULE: LinkedIn engagement before LinkedIn pitch message
RULE: Phone call only after 2+ email/LinkedIn touches
```

### Personalization Consistency

**Maintain across channels:**
- Same sender name/identity
- Consistent value proposition
- Reference previous touchpoints
- Track and update preferences

**Example of Connected Messaging:**

Email Day 2:
```
"I shared a case study about [topic] in my last email..."
```

LinkedIn Day 4:
```
"Hi {{name}}, I sent you an email earlier this week about [topic]. Wanted to connect here as well..."
```

SMS Day 5:
```
"Hey {{name}}, {{sender}} here. Did you catch the case study I sent? Worth a look: {{short_link}}"
```

---

## Tracking Multi-Channel Engagement

### Unified Contact View

Track in CRM:
- Email: Opens, clicks, replies
- SMS: Delivery, clicks, replies
- Phone: Calls made, answered, duration
- LinkedIn: Connection status, messages
- Overall: Last touch date, channel preferences

### Lead Scoring by Channel

| Activity | Points |
|----------|--------|
| Email opened | +1 |
| Email clicked | +3 |
| Email replied | +10 |
| SMS replied | +15 |
| LinkedIn accepted | +5 |
| LinkedIn message reply | +10 |
| Phone answered | +20 |
| Meeting scheduled | +25 |

### Identifying Channel Preference

After 3+ touches, analyze:
- Which channel got responses?
- What time of day works best?
- What content resonated?

Then: Prioritize preferred channel in future sequences

---

## Compliance & Best Practices

### Legal Requirements

**Email (CAN-SPAM, GDPR):**
- Clear sender identification
- Physical address included
- Unsubscribe link in every email
- Honor opt-outs within 10 days

**SMS (TCPA):**
- Written opt-in consent required
- Clear opt-out instructions (STOP)
- Business hours only
- Identify sender in every message

**Phone (DNC, TCPA):**
- Check Do Not Call registry
- No auto-dialers to cell phones without consent
- Respect time zones and hours

### Best Practices Summary

✓ Always lead with value  
✓ Personalize for each channel  
✓ Respect channel preferences  
✓ Maintain consistent messaging  
✓ Track everything in CRM  
✓ Test and optimize constantly  
✓ Get proper consent for SMS/calls  
✓ Have clear opt-out processes  

✗ Don't blast same message across channels  
✗ Don't exceed frequency limits  
✗ Don't mix personal and automated too obviously  
✗ Don't ignore channel-specific norms  
✗ Don't forget compliance requirements  

---

## Implementation Checklist

### Week 1: Foundation
- [ ] Audit current channels in use
- [ ] Choose multi-channel platform/stack
- [ ] Set up integrations between tools
- [ ] Create unified contact view in CRM
- [ ] Document compliance requirements

### Week 2: Build Sequences
- [ ] Map multi-channel customer journey
- [ ] Create templates for each channel
- [ ] Build automation workflows
- [ ] Set up lead scoring rules
- [ ] Configure exit conditions

### Week 3: Launch & Test
- [ ] Test with small segment
- [ ] Monitor deliverability and engagement
- [ ] Check compliance processes work
- [ ] Adjust timing based on data
- [ ] Train team on new workflows

### Week 4+: Optimize
- [ ] Analyze channel performance
- [ ] A/B test messaging
- [ ] Identify preferred channels by segment
- [ ] Refine automation rules
- [ ] Scale successful sequences

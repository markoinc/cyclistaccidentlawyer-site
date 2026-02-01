# GoHighLevel SMS Automation - Complete SOP

**Source:** Industry guides & GoHighLevel documentation  
**Topic:** Setting up automated text message workflows in GoHighLevel  
**Last Updated:** January 2026

---

## Overview

This SOP covers how to set up and configure SMS text message automations in GoHighLevel (GHL) for lead nurturing, follow-ups, appointment reminders, and marketing campaigns.

---

## Prerequisites

Before setting up SMS automations:
1. Active GoHighLevel account
2. Phone number verified and configured in account
3. A2P 10DLC registration completed (required for US SMS)
4. Compliance with TCPA regulations
5. Opted-in contact list

---

## Step 1: Access the Workflow Builder

1. Log in to your GoHighLevel dashboard
2. Navigate to **Automation** → **Workflows**
3. Either create a new workflow or open an existing one
4. Click the plus (+) icon to add new actions

---

## Step 2: Add the Send SMS Action

1. From the action list, select **"Send SMS"**
2. The Send SMS card will appear in your workflow canvas
3. Configure the following settings:

### Basic SMS Settings

| Setting | Description |
|---------|-------------|
| **From** | Select the phone number that will send the SMS (must be verified) |
| **To** | Defaults to contact's primary phone number |
| **Message Body** | The text content you want to send |

---

## Step 3: Personalize Your Messages

### Using Dynamic Fields (Merge Tags)

Insert personalization tokens to customize each message:

- `{{contact.first_name}}` - Contact's first name
- `{{contact.last_name}}` - Contact's last name
- `{{contact.email}}` - Contact's email
- `{{appointment.date}}` - Appointment date
- `{{appointment.time}}` - Appointment time
- `{{user.name}}` - Assigned user's name

### Example Personalized Message:
```
Hi {{contact.first_name}}, this is {{user.name}} from [Business Name]. Thanks for your interest! When's a good time to chat about your project?
```

---

## Step 4: Set Up Triggers

Common triggers for SMS workflows:

### Lead Capture Triggers
- Form submission
- Survey completion
- Landing page opt-in
- Facebook/Google lead ad submission
- Manual contact creation

### Behavior-Based Triggers
- Tag added/removed
- Pipeline stage change
- Appointment booked/cancelled
- Missed call
- Email opened/clicked

### Time-Based Triggers
- Contact created (delay before sending)
- Date-based (birthdays, anniversaries)
- Recurring schedules

---

## Step 5: Build Common SMS Workflows

### Workflow 1: New Lead Welcome Sequence

**Trigger:** Form Submitted

**Sequence:**
1. **Immediately** - Send welcome SMS:
   ```
   Hey {{contact.first_name}}! Thanks for reaching out to [Business Name]. 
   I'm {{user.name}} and I'll be helping you. What questions can I answer?
   ```

2. **Wait 2 hours** - If no reply, send follow-up:
   ```
   {{contact.first_name}}, just following up! I noticed you were 
   interested in [Service]. Ready to chat when you are. 👍
   ```

3. **Wait 24 hours** - Send value message:
   ```
   Quick tip: [Share relevant insight]. Want me to show you how 
   this could work for your situation?
   ```

### Workflow 2: Missed Call Text Back

**Trigger:** Call Status = Missed

**Action:** Send SMS immediately:
```
Hey! Sorry I missed your call. I'm available now - 
would you like me to call you back, or is text easier?
```

### Workflow 3: Appointment Reminder Sequence

**Trigger:** Appointment Booked

**Sequence:**
1. **Immediately** - Confirmation:
   ```
   ✅ Confirmed! Your appointment with {{user.name}} is set for 
   {{appointment.date}} at {{appointment.time}}. Reply YES to confirm 
   or RESCHEDULE if you need to change it.
   ```

2. **24 hours before** - Reminder:
   ```
   Reminder: You have an appointment tomorrow at {{appointment.time}}. 
   Looking forward to speaking with you! Reply C to confirm.
   ```

3. **1 hour before** - Final reminder:
   ```
   Your appointment is in 1 hour! Here's the link to join: [Link] 
   See you soon!
   ```

---

## Step 6: Use Conditional Logic (If/Else)

Add smart branching to your workflows:

### Check for Reply
```
IF Contact Replied = Yes
  → Move to "Engaged" pipeline stage
  → Notify sales rep
ELSE (no reply after 48 hours)
  → Send follow-up message
  → Add tag "Needs Nurturing"
```

### Check Contact Status
```
IF Tag Contains "Hot Lead"
  → Send personalized offer
  → Assign to senior rep
ELSE
  → Continue nurture sequence
```

---

## Step 7: SMS Content Best Practices

### Message Guidelines

| Do | Don't |
|----|-------|
| Keep under 160 characters when possible | Include links in short code messages |
| Identify yourself/business name | Send during off-hours (before 8am/after 9pm) |
| Include clear CTA | Use excessive caps or emojis |
| Personalize with name | Sound robotic or impersonal |
| Respect opt-out requests | Send without permission |

### High-Converting SMS Templates

**Initial Contact:**
```
Hi {{contact.first_name}}, it's {{user.name}} from [Business]. 
Saw you checked out our [service]. Any questions I can answer?
```

**Value-First Follow-up:**
```
{{contact.first_name}}, quick tip that helped our clients: [Insight]. 
Want me to show you how this applies to your situation?
```

**Urgency/Scarcity:**
```
Last chance! Your exclusive offer expires today at midnight. 
Claim it here: [Link] - Reply STOP to opt out
```

---

## Step 8: Test Your Workflow

Before activating:

1. Add yourself as a test contact with your phone number
2. Trigger the workflow manually
3. Verify you receive the message(s)
4. Check:
   - Sender number displays correctly
   - Personalization fields populate
   - Message formatting looks good
   - Links work properly
5. Adjust timing and content as needed

---

## Step 9: Troubleshooting Common Issues

### Messages Not Sending

1. **Check phone number format** - Must include country code
2. **Verify A2P registration** - Required for US SMS
3. **Check workflow conditions** - Ensure contact meets trigger criteria
4. **Confirm opt-in status** - Contact must be opted-in
5. **Review SMS credits** - Ensure sufficient balance

### Low Deliverability

1. **Remove shortened URLs** - Carriers often block link shorteners
2. **Avoid spam trigger words** - "FREE," "WINNER," excessive symbols
3. **Check carrier filtering** - Some content may be blocked
4. **Use approved sender numbers** - Registered, verified numbers only

### Low Response Rates

1. **Improve personalization** - Use first names, context
2. **Adjust timing** - Test different send times
3. **Shorten messages** - Get to the point faster
4. **Add clear CTA** - Tell them exactly what to do
5. **Make it conversational** - Sound like a human, not a bot

---

## Step 10: Compliance Requirements

### TCPA Compliance Checklist

- [ ] Written consent obtained before texting
- [ ] Clear opt-in process with terms disclosed
- [ ] Easy opt-out mechanism (STOP to unsubscribe)
- [ ] Message frequency disclosed
- [ ] Business identification in messages
- [ ] "Msg & data rates may apply" disclaimer in opt-in
- [ ] Records of consent maintained

### A2P 10DLC Requirements

- [ ] Register your brand with The Campaign Registry
- [ ] Submit campaign use case for approval
- [ ] Use verified business phone numbers
- [ ] Follow throughput limits based on trust score

---

## Advanced Tips

### Multi-Channel Workflows
Combine SMS with email and voice:
1. Send SMS immediately (highest open rate)
2. Follow up with email 4 hours later (more detail)
3. If no response in 48h, trigger phone call task

### AI-Powered Responses
Enable Conversation AI in GoHighLevel:
1. Train bot on your FAQ and offerings
2. Let AI handle initial qualification
3. Route hot leads to human reps
4. Use AI for after-hours responses

### Segment-Based Messaging
Create different sequences for:
- Hot leads (rapid follow-up)
- Warm leads (educational content)
- Cold leads (re-engagement campaigns)
- Past customers (upsell/referral asks)

---

## Key Metrics to Track

| Metric | Target | How to Improve |
|--------|--------|----------------|
| Delivery Rate | >95% | Clean list, proper A2P registration |
| Open Rate | >90% | SMS naturally has high opens |
| Response Rate | >20% | Better personalization, clear CTAs |
| Opt-Out Rate | <2% | Don't over-message, provide value |
| Conversion Rate | >5% | Better offers, timing, segmentation |

---

## Summary

1. Set up your phone number and A2P registration
2. Create workflows with appropriate triggers
3. Personalize messages with dynamic fields
4. Use conditional logic for smart routing
5. Test thoroughly before activating
6. Monitor metrics and optimize continuously
7. Stay compliant with TCPA and carrier rules

**Remember:** SMS is a personal channel. Treat it with respect, provide value, and your leads will respond positively.

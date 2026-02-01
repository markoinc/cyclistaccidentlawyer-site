# SMS Appointment Reminders & Confirmation System

**Source:** GReminders, Apptoto, GoHighLevel, Demandforce guides  
**Topic:** Reducing no-shows and maximizing appointment attendance via SMS  
**Last Updated:** January 2026

---

## The No-Show Problem

Industry no-show rates average 20-30%, costing businesses thousands in lost revenue. SMS reminders can reduce no-shows by up to 90%.

### Why SMS Reminders Work

| Channel | Open Rate | Read Within 3 Min | Confirmation Rate |
|---------|-----------|-------------------|-------------------|
| Email | 20% | 5% | 10-15% |
| Phone Call | 30% | N/A | 25-30% |
| SMS | 98% | 90% | 40-50% |

---

## The Complete Reminder System

### Timing Strategy

| When | Purpose | Message Type |
|------|---------|--------------|
| Immediately | Confirmation | Details + confirmation request |
| 24 hours before | Reminder | Confirm/reschedule option |
| 2 hours before | Final reminder | Prep instructions + urgency |
| 15 min before | Last nudge | "See you soon!" (optional) |

---

## Message Templates by Stage

### Stage 1: Booking Confirmation (Immediate)

**Standard Confirmation:**
```
✅ Appointment Confirmed!

{{first_name}}, you're booked with {{provider_name}} on:
📅 {{date}} at ⏰ {{time}}
📍 {{location/link}}

Reply C to confirm or R to reschedule.
Msg & data rates may apply.
```

**With Preparation Instructions:**
```
You're booked, {{first_name}}! 🎉

Appointment: {{date}} at {{time}}
With: {{provider_name}}
Location: {{address}}

BEFORE YOUR VISIT:
• {{prep_item_1}}
• {{prep_item_2}}

Reply C to confirm you've received this.
```

**Virtual/Video Appointment:**
```
Your virtual consultation is confirmed!

📅 {{date}} at {{time}}
💻 Join here: {{meeting_link}}

Pro tip: Join 2 min early to test your connection.

Reply C to confirm!
```

### Stage 2: 24-Hour Reminder

**Simple Reminder:**
```
Reminder: Your appointment is tomorrow!

📅 {{date}} at {{time}}
📍 {{location}}

Still works for you? Reply C to confirm or R to reschedule.
```

**With Added Value:**
```
Hey {{first_name}}! Quick reminder - 
we're meeting tomorrow at {{time}}.

A few things to bring:
• {{item_1}}
• {{item_2}}

Parking tip: {{parking_info}}

See you there! Reply C to confirm.
```

**For Services Requiring Prep:**
```
{{first_name}}, your {{service_type}} is tomorrow at {{time}}!

Quick prep checklist:
☐ {{prep_step_1}}
☐ {{prep_step_2}}
☐ {{prep_step_3}}

Any questions? Just reply to this text!

Reply C to confirm you're all set.
```

### Stage 3: 2-Hour Reminder

**Final Reminder:**
```
Hi {{first_name}}! Your appointment starts in 2 hours.

📍 {{location}}
⏰ {{time}}

On your way soon? Reply Y when you're heading over!
```

**Virtual Appointment:**
```
{{first_name}}, your video call starts in 2 hours!

📍 Click to join: {{meeting_link}}

Make sure to:
• Find a quiet spot
• Test your camera/mic
• Have any documents ready

See you at {{time}}!
```

### Stage 4: Just Before (Optional)

**15-Minute Nudge:**
```
Almost time! See you in 15 min, {{first_name}}. 

Running a bit late? No worries - just give us a heads up!
```

---

## Handling Responses

### Response: Confirmed (C)

```
TRIGGER: Reply = C, YES, CONFIRM

RESPONSE:
"Perfect! You're all confirmed for {{date}} at {{time}}.

See you then, {{first_name}}! 

If anything changes, just text back."

ACTION: 
→ Update CRM: Appointment Confirmed
→ Stop additional reminders for this appointment
```

### Response: Reschedule (R)

```
TRIGGER: Reply = R, RESCHEDULE, CHANGE

RESPONSE:
"No problem! Let me find a new time for you.

Here's what's available this week:
1) {{option_1}}
2) {{option_2}}
3) {{option_3}}

Reply with 1, 2, or 3 - or text a specific 
day/time that works better!"

IF reply = 1, 2, or 3:
  → Reschedule to selected option
  → Send new confirmation
  
IF reply = specific request:
  → Check availability
  → Confirm or offer alternatives
```

### Response: Cancel

```
TRIGGER: Reply = CANCEL, CAN'T MAKE IT

RESPONSE:
"No worries, {{first_name}}! I've cancelled your 
appointment for {{date}}.

Would you like to reschedule for another time?
Reply YES and I'll send available slots."

ACTION:
→ Update CRM: Appointment Cancelled
→ Mark slot as available
→ Trigger re-engagement sequence in 7 days
```

### Response: Running Late

```
TRIGGER: Reply contains "LATE", "RUNNING BEHIND"

RESPONSE:
"Thanks for letting us know, {{first_name}}!

About how long do you think? 
We'll do our best to accommodate."

IF > 15 min late:
  "Got it! We may need to shorten the appointment 
  slightly, but we'll still take care of you.
  
  Drive safe!"
```

### No Response

```
TRIGGER: No reply to 24-hour reminder after 4 hours

ACTION: Send follow-up:
"Hey {{first_name}}, just checking - still good 
for tomorrow at {{time}}?

Reply C to confirm or R if you need to change."

TRIGGER: Still no reply, 12 hours before appointment

ACTION: Phone call attempt (if available)
OR: Final SMS:
"{{first_name}}, your appointment is in 12 hours. 
I haven't heard back - please let me know if 
you're still coming so we can hold your spot.

Reply YES to confirm!"
```

---

## Reducing No-Shows: Advanced Strategies

### 1. Confirmation Incentive

```
Confirm your appointment and get 10% off your next visit!

Reply C to confirm and we'll save your discount code.
```

### 2. Late Policy Reminder

```
Reminder: We have a 24-hour cancellation policy. 
Late cancellations may be subject to a fee.

Still works for you? Reply C to confirm.
```

### 3. Easy Reschedule Option

```
Can't make it? No worries! 

Text MOVE and I'll send you our next available times.
It only takes 30 seconds to reschedule.
```

### 4. Show Investment

```
{{first_name}}, we've reserved this time specifically 
for you with {{provider_name}}.

Looking forward to seeing you {{date}} at {{time}}!
Reply C to confirm you'll be there.
```

### 5. Reciprocity ("We Prepared for You")

```
Hey {{first_name}}! We've reviewed your [file/history/project] 
and prepared some great recommendations for our meeting tomorrow.

See you at {{time}}! Reply C to confirm.
```

---

## Industry-Specific Templates

### Healthcare/Dental

**24-Hour Reminder:**
```
Reminder: Dr. {{doctor_name}} is looking forward to 
seeing you tomorrow at {{time}}.

📍 {{practice_name}}
   {{address}}

Please arrive 10 min early for check-in.
Bring: Insurance card, ID, list of medications.

Reply C to confirm or call {{phone}} to reschedule.
```

### Salon/Spa

```
Your pamper session awaits! 💆

Service: {{service}}
Date: {{date}} at {{time}}
With: {{stylist_name}}

Arrive 5 min early to relax before your appointment.

Reply C to confirm we'll see you!
```

### Real Estate

```
{{first_name}}, excited to show you {{property_address}} tomorrow!

🏠 Tour Date: {{date}} at {{time}}
📍 Meet at: {{meeting_location}}

I'll have comps and neighborhood info ready for you.

Reply C to confirm - see you there!
```

### Consulting/Professional Services

```
{{first_name}}, looking forward to our strategy session!

📅 {{date}} at {{time}}
📞 I'll call you at: {{phone_number}}
   OR Join: {{meeting_link}}

What to have ready:
• {{prep_item_1}}
• {{prep_item_2}}

Reply C to confirm!
```

### Auto Service

```
🔧 Service Reminder for your {{vehicle}}

Appointment: {{date}} at {{time}}
Service: {{service_type}}
Location: {{address}}

Estimated time: {{duration}}
We offer a comfortable waiting area with WiFi ☕

Reply C to confirm or R to reschedule.
```

---

## Automation Setup

### Workflow Configuration

```
WORKFLOW: Appointment Reminder Sequence

TRIGGER: Appointment Booked

STEP 1 (Immediate):
  → Send Confirmation SMS
  → Wait for reply (24 hours)
  
IF Reply = Confirmed:
  → Tag "Appointment Confirmed"
  → Continue sequence
  
IF Reply = Reschedule:
  → Branch to Reschedule Flow
  → End current sequence
  
IF No Reply:
  → Continue sequence

STEP 2 (24 hours before):
  → Check if still scheduled
  → Send 24-Hour Reminder
  → Wait for reply (4 hours)
  
STEP 3 (2 hours before):
  → Send Final Reminder
  
STEP 4 (Post-Appointment):
  → Wait 2 hours after appointment time
  → Send feedback request
```

### Cancellation/No-Show Follow-Up

```
TRIGGER: Appointment marked as No-Show

WAIT: 2 hours

SEND:
"Hey {{first_name}}, we missed you today!

Everything okay? We had your spot reserved at {{time}}.

If something came up, no worries - reply REBOOK 
and I'll find you a new time."

WAIT: 3 days

IF not rebooked:
  "Still want to reschedule, {{first_name}}?
  
  I have a few openings this week. Reply YES 
  and I'll send times that work!"
```

---

## Metrics to Track

| Metric | Formula | Target |
|--------|---------|--------|
| Confirmation Rate | Confirmed / Sent | >50% |
| No-Show Rate | No-Shows / Total Scheduled | <10% |
| Reschedule Rate | Rescheduled / Cancellations | >50% |
| Response Rate | Replies / Reminders Sent | >30% |

### ROI Calculation

```
Monthly Appointments: 100
Previous No-Show Rate: 25% (25 no-shows)
Revenue Per Appointment: $200
Lost Revenue: $5,000/month

With SMS Reminders:
New No-Show Rate: 5% (5 no-shows)
Saved Appointments: 20
Recovered Revenue: $4,000/month
SMS Cost: ~$50/month

Net Monthly Savings: $3,950
Annual Impact: $47,400
```

---

## Summary: Appointment Reminder Best Practices

1. **Send confirmation immediately** after booking
2. **24-hour reminder** with confirmation request
3. **2-hour reminder** with prep instructions
4. **Make it easy** to confirm (reply C) or reschedule (reply R)
5. **Follow up** on no-responses before giving up
6. **Handle cancellations** with reschedule options
7. **Track metrics** and optimize timing/content
8. **Be human** - not robotic appointment robots

**The Goal:** Every customer should feel expected, prepared, and valued.

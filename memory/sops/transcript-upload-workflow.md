# Transcript Upload Workflow

**Created:** 2026-02-16

## When Mark Uploads New Call Transcripts

### Trigger
Mark says something like:
- "new transcript uploaded"
- "added a call recording"
- "transcribed the [X] call"
- Uploads a file to Slack/Drive

### Process

1. **Locate the transcript**
   - Check: `/home/ec2-user/data/Kurios Automation Projects/business/transcripts/`
   - Or: Google Drive "Sales Call Transcripts" folder
   - Or: Slack upload

2. **Identify the prospect**
   - Match to Google Sheet: `1iu8lHRKAt_eDoHr6SreDktQhwT8l0R-VFpfvObKHtMQ`
   - Get contact info, appointment date, status

3. **Pull email context**
   - Search Gmail (mark@kuriosbrand.com) for prospect email
   - Get latest thread/status

4. **Update Google Docs**
   - Append transcript to: `1R2GM7m1SHQpOpviZnZtdap0Lw6cJPw3XoFB7-kuYago` (Pre-Partnership transcripts) 
     OR create new doc in Sales Call Transcripts folder
   - Update prospect brief in: `1F19dw-DsTOKALbE0lvsL-Rs1OoEfXWXBLqvjwZ0qFZQ`

5. **Notify Carlos**
   - Post summary to #carlos-sierra
   - Include: prospect name, key takeaways, recommended next action

### Key Doc IDs
- **Prospect Briefs (Running):** `1F19dw-DsTOKALbE0lvsL-Rs1OoEfXWXBLqvjwZ0qFZQ`
- **Pre-Partnership Transcripts:** `1R2GM7m1SHQpOpviZnZtdap0Lw6cJPw3XoFB7-kuYago`
- **Sales Call Transcripts Folder:** `1drql12tAsDHzQIhAn7NOL609Zix0F_gu`
- **MVA Appointments Sheet:** `1iu8lHRKAt_eDoHr6SreDktQhwT8l0R-VFpfvObKHtMQ`

### Skip CA Prospects
California prospects are for SEO offer, not MVA lead gen offer.

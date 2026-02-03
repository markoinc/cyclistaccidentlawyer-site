# Voice Message Transcription & Response Workflow

**Created:** 2026-02-03
**Last Updated:** 2026-02-03

## Purpose
Handle voice messages from Marko efficiently — transcribe, understand, and act.

---

## Workflow

### 1. Transcription
Use OpenAI Whisper API:
```python
import openai
client = openai.OpenAI(api_key='[KEY]')
with open('[PATH_TO_AUDIO]', 'rb') as f:
    transcript = client.audio.transcriptions.create(model='whisper-1', file=f)
print(transcript.text)
```

### 2. Parse Instructions
- Listen for specific changes/corrections
- Note any "remember this" or preference statements
- Identify action items

### 3. Execute
- Make requested changes
- Show updated version for review
- Don't send externally until explicitly approved

### 4. Document Learnings
- If Marko corrects something, update relevant SOP
- Add preferences to MEMORY.md or specific SOP files

---

## Common Patterns

### Draft Review Cycle
1. Marko sends voice message with task
2. I create draft and show it
3. Marko sends voice corrections
4. I update and show again
5. Repeat until "send it" or approval

### Calendar Lookups
When Marko mentions "it's on my calendar":
```python
# Search by name
url = 'https://www.googleapis.com/calendar/v3/calendars/mark@kuriosbrand.com/events'
params = {'q': '[SEARCH_TERM]', 'timeMin': now, 'timeMax': future}
```

---

## Key Preferences Learned

1. **Signature** — Just name + kuriosbrand.com (no LLC, no phone)
2. **Timeline** — Signed cases = 30-40 days delivery
3. **Language** — "Already converted" not "they convert"
4. **Patrick mentions** — Don't include unless instructed
5. **Closing** — "Looking forward to getting started" (confident, not passive)

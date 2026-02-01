# Video References for Future Transcription

**Note:** YouTube video transcripts were blocked from AWS IP addresses. These videos were identified as high-quality educational content from known Meta Ads educators.

---

## Ben Heath Videos (415K subscribers)

### 1. The BEST Facebook Ads Tutorial For Beginners in 2026
- **URL:** https://www.youtube.com/watch?v=dAJyqo6wnq4
- **Length:** ~1 hour
- **Views:** 47K
- **Published:** January 2026
- **Topics:** Fundamentals, beginner tutorial

### 2. The ONLY Meta Ads Targeting Tutorial You Need in 2026
- **URL:** https://www.youtube.com/watch?v=-CsBl3tv-X0
- **Length:** 1:01:13
- **Views:** 92K
- **Topics:** Targeting strategies

### 3. I Reviewed Real Meta Ads (Here's What Actually Works)
- **URL:** https://www.youtube.com/watch?v=487xP7cEP6I
- **Length:** 35:37
- **Views:** 9.2K
- **Published:** ~1 month ago
- **Topics:** Creative review, what works

### 4. My UPDATED Meta Ad Strategy That's Beating Everyone Right Now
- **URL:** https://www.youtube.com/watch?v=hHuxr_ancXQ
- **Length:** 1:21:02
- **Views:** 31K
- **Topics:** Current winning strategies

### 5. If I Started Facebook Ads in 2026, I'd Do This...
- **URL:** https://www.youtube.com/watch?v=crId74rHjuA
- **Length:** 58:27
- **Views:** 77K
- **Topics:** Starting fresh, best approach

---

## Nick Theriot Videos

### 1. Best Facebook Ads Campaign Structure To Scale In 2026
- **URL:** https://www.youtube.com/watch?v=SVI2qz149Es
- **Published:** ~3 weeks ago
- **Topics:** Campaign structure, scaling

### 2. How To Test Facebook Ads In 2026
- **URL:** https://www.youtube.com/watch?v=G2ZAO9ZsZ-A
- **Published:** ~3 weeks ago
- **Topics:** Testing strategies

### 3. How To Scale Facebook Ads In 2026
- **URL:** https://www.youtube.com/watch?v=le19PPUNaYk
- **Published:** ~2 weeks ago
- **Topics:** Scaling strategies

### 4. Do this before running Facebook Ads in 2026 (if you want to scale)
- **URL:** https://www.youtube.com/watch?v=NPJb9U7HRTw
- **Published:** ~3 weeks ago
- **Topics:** Pre-launch preparation

### 5. Ads to Run in January 2026 to SCALE (Copy My Playbook)
- **URL:** https://www.youtube.com/watch?v=jYjp4Gus59U
- **Published:** December 31, 2025
- **Topics:** Q1 strategy, content calendar

### 6. ECOM Brand Does $1,711,582 in 30 Days With Facebook Ads (Here's How)
- **URL:** https://www.youtube.com/watch?v=ghvRqEKuUU4
- **Published:** ~1 month ago
- **Topics:** E-commerce case study, scaling

---

## Sam Piliero Videos

### 1. The NEW Way to Run Facebook Ads in 2026
- **URL:** https://www.youtube.com/watch?v=Gb3_SXgUDhI
- **Published:** ~2 weeks ago
- **Topics:** New approaches, updated strategies

### 2. Facebook Ads NEW Rules for 2026 (learn this ASAP)
- **URL:** https://www.youtube.com/watch?v=0cj09Aa3de8
- **Published:** ~1 month ago
- **Topics:** Platform changes, new rules

### 3. Brutally Honest Advice About Facebook Ads in 18 mins
- **URL:** https://www.youtube.com/watch?v=msa7sVEUtnc
- **Length:** 18:24
- **Views:** 39K
- **Topics:** Honest assessment, advice

---

## Account Structure & Strategy Videos

### 1. The BEST Meta Ads Account Structure for 2026 (Step By Step Tutorial)
- **URL:** https://www.youtube.com/watch?v=KKzb-kg_xaI
- **Source:** Sell More Online
- **Published:** December 31, 2025
- **Topics:** Account structure, step-by-step

### 2. Meta Ads for Beginners: How to Launch Your First Campaign in 2026
- **URL:** https://www.youtube.com/watch?v=LBaDH7xqhuE
- **Published:** ~2 weeks ago
- **Topics:** Beginner tutorial, first campaign

### 3. 🚀 How to Run Meta Ads for Beginners (Meta Ads Tutorial 2025)
- **URL:** https://www.youtube.com/watch?v=BZNGTK2jZZo
- **Source:** Star Agile
- **Topics:** Beginner tutorial

### 4. I Found the BEST Strategy to Scale Facebook Ads in 2026
- **URL:** https://www.youtube.com/watch?v=cs23-HQp12s
- **Source:** Skale It Agency
- **Published:** ~3 weeks ago
- **Topics:** Post-Andromeda/GEM strategy, scaling

---

## CBO vs ABO Videos

### 1. The Truth About CBO vs ABO On Facebook Ads In 2026
- **URL:** https://www.youtube.com/watch?v=VmyyxKxAtfc
- **Published:** ~3 weeks ago
- **Topics:** Budget optimization comparison

### 2. Facebook Ads ABO vs CBO - Which Should You Use in 2026?
- **URL:** https://www.youtube.com/watch?v=wKDeZWnVA9c
- **Source:** Sam Piliero
- **Published:** ~1 month ago
- **Topics:** When to use each strategy

---

## Disrupter School Videos

### 1. Copy This NEW Meta Ads Strategy, It'll Blow Up Your Business (Post-Andromeda)
- **URL:** https://www.youtube.com/watch?v=4jCF6Fug9To
- **Published:** ~1 month ago
- **Topics:** Post-Andromeda strategy

### 2. Use This Facebook Ad Setting, It'll Blow Up Your Business
- **URL:** https://www.youtube.com/watch?v=cK-CDZ4xpto
- **Published:** ~1 month ago
- **Topics:** Key settings, strategy

---

## Other Notable Videos

### Facebook Ads For Beginners: Complete Guide (2026)
- **URL:** https://www.youtube.com/watch?v=uUlU5G1Nda0
- **Source:** Chris Koerner on The Koerner Office Podcast
- **Length:** 46:19
- **Views:** 118K
- **Topics:** Complete beginner guide

### How to Run Meta Ads For Beginners (Meta Ads Tutorial 2025)
- **URL:** https://www.youtube.com/watch?v=t-6c16BH-0U
- **Source:** Hostinger Academy
- **Length:** 24:31
- **Views:** 226K
- **Topics:** Beginner tutorial

---

## How to Transcribe (Future Reference)

When IP restrictions are resolved, use:
```bash
# Get transcript via youtube-transcript-api
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
transcript = api.fetch('VIDEO_ID', languages=['en'])
text = ' '.join([e.text for e in transcript])
print(text)
"

# Or download audio and transcribe
yt-dlp --extract-audio --audio-format mp3 "URL"
whisper audio.mp3 --model medium
```

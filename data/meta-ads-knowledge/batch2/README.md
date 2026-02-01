# Meta Ads Course Videos - Batch 2

**Research Date:** January 31, 2026
**Status:** Videos identified, transcripts pending (YouTube blocking AWS IPs)

## Issue

YouTube and all third-party transcript services are blocking requests from AWS/cloud provider IPs. Both yt-dlp and youtube-transcript-api fail with bot detection errors. Browser-based transcript tools (youtubetotranscript.com, tactiq.io) are blocked by Cloudflare.

**Solution needed:** Run transcript extraction from a residential IP, or use a proxy service.

---

## 7 Curated Videos for Transcription

### 1. Ad Creative / Copywriting
**Title:** How to Write Winning Meta Ad Scripts ($450M Spent)
**Creator:** Fraser Cottrell (Fraggell)
**URL:** https://www.youtube.com/watch?v=KKp3rA0QK9A
**Published:** ~3 weeks ago (Jan 2026)
**Views:** 4.8K
**Subscribers:** 17.8K
**Key Topics:** Ad script writing, high-converting ad copy, $450M+ ad spend insights

---

### 2. Creative Process
**Title:** The Creative Process I Use To Make Winning Meta Ads Over And Over Again
**Creator:** Andrew Faris (Andrew Faris Podcast)
**URL:** https://www.youtube.com/watch?v=Tj2oufaLQjg
**Published:** ~3 weeks ago (Jan 2026)
**Key Topics:** Systematic creative process, repeatable winning ad frameworks

---

### 3. UGC / Video Ads
**Title:** How to Create AI UGC Ads That Get 3.8x ROAS (Full Tutorial)
**Creator:** Unknown
**URL:** https://www.youtube.com/watch?v=MLCNXcF_brM
**Published:** ~1 month ago (Dec 2025)
**Key Topics:** AI-generated UGC ads, 3.8x ROAS strategies, no camera/actors approach

---

### 4. Lookalike Audiences
**Title:** The New Way To Use Lookalike Audience On Meta Ads in 2026
**Creator:** Nestuge
**URL:** https://www.youtube.com/watch?v=ZQiAxA3JpJc
**Published:** ~3 weeks ago (Jan 2026)
**Key Topics:** Updated lookalike audience strategies, post-Andromeda changes

---

### 5. Scaling Strategy
**Title:** I Found the BEST Strategy to Scale Facebook Ads in 2026
**Creator:** Skale It Agency
**URL:** https://www.youtube.com/watch?v=cs23-HQp12s
**Published:** ~3 weeks ago (Jan 2026)
**Key Topics:** Scaling after Meta Andromeda & GEM updates, exact methodology

---

### 6. Post-Andromeda Strategy
**Title:** Copy This NEW Meta Ads Strategy, It'll Blow Up Your Business (Post-Andromeda)
**Creator:** Charley T (Professor Charley T / Disrupter School)
**URL:** https://www.youtube.com/watch?v=4jCF6Fug9To
**Published:** ~1 month ago (Dec 2025)
**Views:** 7.4K
**Duration:** 16:15
**Key Topics:** Post-Andromeda ad strategy, new Meta algorithm adaptation

---

### 7. Campaign Structure
**Title:** The NEW BEST Facebook Ads Campaign Structure for 2026
**Creator:** Charley T (Disrupter School)
**URL:** https://www.youtube.com/watch?v=E_wZJhuSK5U
**Published:** ~3 weeks ago (Jan 2026)
**Key Topics:** Optimal campaign structure 2026, best practices for ad organization

---

## Additional Notable Videos Found

| Title | Creator | URL | Topic |
|-------|---------|-----|-------|
| The Ultimate Meta Ads Training for 2026 (Full Course) | Sell More Online | https://www.youtube.com/watch?v=tzprpP9n-gc | Full course |
| The BEST Meta Ads Account Structure for 2026 | Sell More Online | https://www.youtube.com/watch?v=KKzb-kg_xaI | Account structure |
| Meta Ads in 2026: Andromeda, Gem & Lattice Explained | Unknown | https://www.youtube.com/watch?v=UMZW_Jd8XW8 | Algorithm updates |
| How to Find the Right UGC Creators in 2026 | Fraggell | https://www.youtube.com/watch?v=xB4jykCt_yU | UGC sourcing |
| The New Meta Ads Testing Strategy: 10 Ads vs 100 Ads | Caleb Kruse | https://www.youtube.com/watch?v=TIWDiHzsjbI | Creative testing |
| Best Meta Ads Audience Targeting Strategy | Unknown | https://www.youtube.com/watch?v=G-aCkVCVOHA | Targeting |
| Meta Ads Lookalike Audiences in 2026 | Facebook Ads Master | https://www.youtube.com/watch?v=_UQi2__7fKU | Lookalikes |
| How to Make Viral AI UGC Ads in 2026 | Unknown | https://www.youtube.com/watch?v=_H01wcSCEko | AI UGC |

---

## To Complete Transcription

Run from residential IP:
```bash
cd /home/ec2-user/clawd/data/meta-ads-knowledge/batch2
python3 fetch_transcripts.py
```

Or use yt-dlp with cookies from authenticated browser:
```bash
yt-dlp --cookies-from-browser chrome "URL" -x --audio-format mp3 -o "audio.mp3"
whisper audio.mp3 --model base --output_format txt
```

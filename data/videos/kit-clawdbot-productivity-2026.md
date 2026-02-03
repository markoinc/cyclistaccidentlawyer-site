# Kit's Clawdbot Productivity Setup - Greg Isenberg Podcast

**Source:** https://www.youtube.com/watch?v=YRhGtHfs1Lw
**Transcribed:** 2026-02-01

## Key Takeaways

### Multi-Persona Architecture
- One Clawdbot gateway serving multiple personas via Telegram/Discord
- Each persona has different skills, avatar, personality
- Examples:
  - **David Goggins** - Fitness coach (talks like Goggins, swears, motivational)
  - **Kevin (from The Office)** - Accountant
  - **Dr. Cox** - Health/medical (has all blood results, tracks health data)
  - **Darlene** - Home manager (groceries, shopping, family group)
  - **Gilfoyle (Silicon Valley)** - Professional engineer (React Native, Vercel, GitHub, SSH)

### Platform Recommendations
1. **Beginners:** Start with Telegram or iMessage (feel the magic)
2. **Power users:** Discord (channels, threads, sections, organization)
3. **Work:** Slack (familiar interface)
4. **Avoid:** WhatsApp (most finicky setup)

### Discord Organization
- Sections for different areas (customers, skills, etc.)
- Channels stay forever
- Threads for temporary tasks
- Forum posts for individual items (customer support threads)
- Control from main thread, spawn sub-agents for individual processing

### Security Best Practices
⚠️ **Critical:**
- Don't connect email if just starting
- Don't host on VPS if possible - self-host and dockerize
- Don't use cheap models (Haiku gets prompt injected)
- Use Opus for security-sensitive tasks
- No webhook for every email - use cron jobs instead
- Opus is extremely careful (even rejected "wake me at 8:30am" thinking it was suspicious)

### Model Delegation
- **Opus:** Main brain, security-sensitive, orchestration
- **Codex:** Spawn sub-agents for coding tasks
- Skill tells bot: "Anytime you need to code, spawn a Codex sub-agent"

### Cool Use Cases Demonstrated

1. **Printer Discovery** - "Find my printer and print something cool" → found on network, printed ASCII art

2. **TV Dashboard** - Finds displays via Home Assistant, creates HTML dashboard, casts to TV

3. **Anti-Captcha Integration** - anticapture.com for solving captchas ($5/mo)
   - But Opus can sometimes solve captchas itself ("Oh, brooms. Cool.")

4. **Smart Home Vision:**
   - Presence sensors in rooms detecting Apple Watch
   - Cloudbot knows GPS + room location
   - Context-aware commands
   - TV lights up red when late to meeting

5. **YouTube Playlist Workaround:**
   - YouTube won't let you make playlists from children's songs
   - Cloudbot: Downloaded from YouTube → NAS → Plex playlist

6. **Pi-Hole Setup** - "Set up Pi-Hole on my spare Mac Studio" → 92% ads blocked network-wide

7. **Excalidraw Skill** - Makes JSON, hosts it, gives link to open in Excalidraw

8. **Banking Analysis:**
   - Imported all bank CSVs since 2023
   - "Find dentist emails + bank transactions, visualize my dental history"
   - Created UI showing which tooth, what paid, implants, upcoming work

9. **Spellbook** - Prompt organizer with variables (spellbook.is)

### Hardware Mentioned
- **Pebble Ring** - AI ring with button + mic, API for sending voice notes anywhere
- **TRMNL** - E-ink programmable display for life OS dashboards
- Mac Studio for self-hosting

### Philosophy
- "If you don't see it, you don't see it" - stop convincing skeptics
- Tinkerers vs consumers split widening
- "18-year-old with agent army will destroy experienced devs without AI"
- Amazon laying off 15K, Pinterest 15% - "do more with less"
- "LLMs won't be uninvented. Embrace the speed."

### Resources
- **Tinkerers Club** - Tight community for ADHD tinkerers (mentioned discount code)
- Kit's DMs open for questions

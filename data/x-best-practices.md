# X Research: Best Practices for Clawdbot/OpenClaw

*Compiled: 2026-02-01 from X/Twitter research*

---

## 🦞 TL;DR - Top 10 Actionable Tips

1. **Use AGENTS.md as single canonical file** - simpler than separate CLAUDE.md files
2. **Skills > Agents** - Build reusable skills, they compound over time
3. **Spawn subagents for heavy tasks** - Keep main context clean
4. **Bind gateway to loopback** - Critical security (Shodan found hundreds exposed)
5. **Use pairing mode for DMs** - Manually approve new devices
6. **Kick off 3 small tasks before bed** - Claude mobile agents work while you sleep
7. **Edit SOUL.md for personality** - Customize your assistant's character
8. **Set up hooks for triggers** - Email arrivals, calendar events, etc.
9. **Use Tailscale for remote access** - Don't expose ports directly
10. **Run `openclaw doctor` regularly** - Diagnose issues and security risks

---

## 📦 Installation Quick Start

```bash
# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# Run onboarding wizard (installs as background daemon)
openclaw onboard --install-daemon

# Verify installation
openclaw doctor
openclaw status --all
openclaw security audit --deep
```

**Requirements:**
- Node.js ≥22
- Any modern hardware (Mac Mini, Raspberry Pi 4/5, $5/mo VPS works)
- API keys (Anthropic Claude recommended)

---

## 🧠 Memory Management Best Practices

### File Structure
```
workspace/
├── AGENTS.md       # Main instructions (read every session)
├── SOUL.md         # Personality & character definition
├── USER.md         # Info about the human you're helping
├── MEMORY.md       # Long-term curated memories
├── TOOLS.md        # Local tool notes & credentials
└── memory/
    └── YYYY-MM-DD.md  # Daily raw logs
```

### Key Insights from @AndrewYNg & @omarsar0
- **MemGPT Pattern**: Use LLM to manage context window like OS manages memory
- **Unified Memory**: Long-term persists across stages, short-term resets between stages
- **Tool-based Operations**: ADD, UPDATE, DELETE for storage; RETRIEVE, SUMMARY, FILTER for context

### Daily Workflow
1. Read `SOUL.md` → `USER.md` → today's `memory/YYYY-MM-DD.md`
2. In main sessions: also load `MEMORY.md`
3. Write significant events to daily files
4. Periodically distill daily logs into `MEMORY.md`

**Quote from @doodlestein:**
> "Don't bother with CLAUDE.md files, just use AGENTS.md - it's simpler to have one canonical file, and you shouldn't rely on agents automatically reading it anyway."

---

## 🔧 Skills System

### Location
```
~/.claude/skills/skill-name/SKILL.md
```

### Features (Claude Code 2.1.0+)
- Forked context
- Hot reload  
- Custom agent support
- Invoke with `/` command

### Building Skills (@omarsar0)
> "The more skills you build, the more useful Claude Code gets. Skills are the way you make Claude Code more knowledgeable over time."

**Anthropic Philosophy:** Skills > Agents - procedural knowledge compounds

### Example Skill Ideas (@trillhause_)
- Email triage workflow
- Daily brief generation
- Meeting time finder
- Custom code patterns

---

## 👥 Delegation & Subagents

### Hierarchy Pattern
```
You (Human)
  └── Chief Agent (main)
        ├── Research Agent
        ├── Coding Agent
        ├── Email Agent
        └── Social Agent
```

### Claude Code Subagents
1. Start with `/agents` command
2. Let Claude generate initial agents
3. Press `e` to edit and refine
4. Be precise in description fields - Claude uses them for routing

### Key Insight (@BadUncleX)
> "Sub-agents and skills are NOT the same. Sub-agents handle async tasks with delegation. Skills are reusable procedures."

### Multi-Agent Orchestration (@nummanali)
Claude Code has hidden multi-agent orchestration. Enable via CC Mirror:
```
https://github.com/numman-ali/cc-mirror
```

---

## 🛡️ Security Best Practices

### CRITICAL - Do These First

```yaml
# In your config:
gateway:
  bind: "loopback"  # Never expose externally!
  
agents:
  defaults:
    sandbox:
      mode: "non-main"  # Sandbox group chats
```

### Security Checklist
- [ ] Gateway bound to loopback only
- [ ] DM pairing mode enabled (manual approval)
- [ ] Sandbox mode for group/channel sessions
- [ ] Tailscale or Cloudflare Tunnel for remote (not exposed ports)
- [ ] API keys secured (agent has access to them!)
- [ ] Regular `openclaw security audit --deep`

### Why This Matters
**@doodlestein:** "It uses more tokens and increases latency somewhat, but I think it's worth it given how much chaos could conceivably be caused by a fully set up Clawdbot getting hijacked."

**Shodan finding:** Hundreds of exposed gateways found vulnerable.

---

## 🌙 Overnight/Background Workflows

### Claude Mobile Trick (@AlexFinnX)
> "Download Claude mobile app. There's a Code section where you can spin up cloud AI agents that work while you sleep. Every night before bed, kick off 3 small tasks."

### Benefits
1. Wake up to completed work
2. Build consistent momentum
3. Even tiny visual changes count

### Clawdbot Hooks
Set up triggers for:
- Email arrivals
- Calendar events
- File changes
- Custom webhooks

```bash
# Example: Agent wakes for emails
openclaw hooks add --trigger email --action notify
```

---

## 🎯 Workflow Patterns from Power Users

### @steipete's Workflow
1. Agent controls browser autonomously
2. Group chat lurking (observe without responding)
3. Background bash tool (no hanging on CLI breaks)
4. Self-modifying code + auto-restart
5. Voice calls via plugin

### @heyitsyashu's Setup
- Email handling
- Calendar management
- Task tracking
- API integrations (grocery delivery, etc.)
- "Like Claude Code but as a personal Jarvis"

### @iamkasparp's Setup
- Baby room temperature monitoring
- Vacuum automation
- Custom personality ("Skippy")
- Wake words for voice activation
- Omi dev kit for 24/7 wearable assistant

---

## 📊 Dashboard Building

### OpenClaw Dashboard
```bash
openclaw dashboard
# Opens at http://127.0.0.1:18789/
```

### Integration Ideas
- **Obsidian** for personal knowledge base
- **Daily PDF briefs** (automated summaries)
- **GitHub tracking** for repos
- **Health data** (Whoop, Apple Health)

### Remote Access
```bash
# SSH tunnel method
ssh -L 18789:127.0.0.1:18789 user@YOUR_SERVER

# Tailscale (recommended)
tailscale serve 18789
```

---

## 🔗 Tools & Resources

### Official
- Docs: https://docs.openclaw.ai
- GitHub: https://github.com/openclaw/openclaw
- Install: `curl -fsSL https://openclaw.ai/install.sh | bash`

### Tutorials
- Claude Agent SDK Workshop (2hr): https://youtube.com/watch?v=TqC1qOfiVcQ
- Codecademy Tutorial: codecademy.com/article/open-claw-tutorial
- DigitalOcean Guide: gist.github.com/dabit3/42cce744beaa6a0d47d6a6783e443636

### Community
- Clawdbot Community: https://x.com/i/communities/2003018816251453457
- Claude Code Community: @claude_code

---

## 🌟 Accounts to Follow

| Handle | Focus |
|--------|-------|
| @steipete | Clawdbot creator, cutting-edge tips |
| @clawdbot | Official updates |
| @openclaw | OpenClaw official |
| @claude_code | Claude Code community & plugins |
| @AlexFinnX | Vibe coding, practical AI workflows |
| @indexsy | SEO automation, AI business |
| @trillhause_ | Skills & personal assistant setup |
| @dabit3 | Claude Agent SDK tutorials |
| @omarsar0 | AI memory research |
| @nummanali | Multi-agent orchestration |
| @doodlestein | Agent Flywheel methodology |

---

## 💡 Quick Wins to Implement Today

1. **Edit your SOUL.md** - Give your agent personality
2. **Create one skill** - Start with email triage or daily brief
3. **Set up mobile Claude** - Kick off overnight tasks
4. **Run security audit** - `openclaw security audit --deep`
5. **Join the community** - Follow @clawdbot and @steipete

---

*Research compiled from 47 sources on X/Twitter. Data current as of 2026-02-01.*

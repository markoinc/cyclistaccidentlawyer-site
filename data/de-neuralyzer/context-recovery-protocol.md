# De-Neuralyzer Context Recovery Protocol

## 🧠 What is Memory Compaction?

When Claude's context window fills up, Clawdbot performs **compaction** - truncating older messages to make room. This is like the "neuralyzer" from Men in Black - wiping recent memory.

The problem: **You forget what you were just working on.**

## 🔄 The De-Neuralyzer Solution

Session transcripts at `~/.clawdbot/agents/main/sessions/` contain **everything** - every message, tool call, and decision. The De-Neuralyzer extracts this to rebuild context.

---

## 🚨 Step-by-Step Recovery Protocol

### Step 1: Detect Compaction

Run the analyzer to check if compaction happened recently:

```bash
python3 /home/ec2-user/clawd/data/de-neuralyzer/session-analyzer.py --detect
```

Output:
- `COMPACTION_DETECTED` (exit 1) - You lost context
- `NO_RECENT_COMPACTION` (exit 0) - Context is intact

### Step 2: Extract Current Context

Generate a context recovery file:

```bash
python3 /home/ec2-user/clawd/data/de-neuralyzer/session-analyzer.py
```

This creates `/home/ec2-user/clawd/data/de-neuralyzer/current-context.json` with:
- Recent user requests
- Active tasks
- Key decisions
- Files read/modified
- Conversation summary

### Step 3: Quick Summary

For a human-readable summary of recent conversation:

```bash
python3 /home/ec2-user/clawd/data/de-neuralyzer/session-analyzer.py --summary
```

---

## 🔧 Automatic Recovery (HEARTBEAT Integration)

Add this to your `HEARTBEAT.md` for automatic context recovery:

```markdown
## Context Recovery Check
If you feel disoriented or context seems missing:
1. Read `/home/ec2-user/clawd/data/de-neuralyzer/current-context.json`
2. Check recent user requests and active tasks
3. Resume the most recent active task
```

Or add a cron job to regenerate context regularly:

```bash
*/5 * * * * python3 /home/ec2-user/clawd/data/de-neuralyzer/session-analyzer.py 2>/dev/null
```

---

## 📊 What Gets Extracted

### Recent User Requests
The last 10 messages from the user - what they asked for.

### Active Tasks
Tasks that appear to be in-progress based on phrases like:
- "working on", "in progress", "currently"
- "let me", "I'll", "spawning", "checking"

### Key Decisions
Important decisions captured by keywords like:
- "decided", "plan is", "strategy:", "solution:"
- "created", "updated", "deployed", "fixed"

### Files Touched
- Files that were read (from compaction details)
- Files that were modified (from compaction details)

### Conversation Summary
The last 15-20 messages in readable format.

---

## 🛠 Manual Recovery Checklist

If automatic recovery isn't enough:

1. **Check the context JSON:**
   ```bash
   cat /home/ec2-user/clawd/data/de-neuralyzer/current-context.json | jq '.recent_user_requests[-3:]'
   ```

2. **Review files modified:**
   ```bash
   cat /home/ec2-user/clawd/data/de-neuralyzer/current-context.json | jq '.files_touched.modified'
   ```

3. **Check memory files:**
   ```bash
   cat /home/ec2-user/clawd/memory/$(date +%Y-%m-%d).md
   ```

4. **Review active subagents:**
   ```bash
   clawdbot sessions list
   ```

---

## 🎯 Best Practices

1. **Write to memory frequently** - Document important decisions in `memory/YYYY-MM-DD.md`
2. **Update MEMORY.md** - Keep long-term context in your curated memory
3. **Use descriptive commits** - Good commit messages help recover what you did
4. **Spawn subagents** - They have their own context and survive main session compaction

---

## ⚡ Quick Commands

| Action | Command |
|--------|---------|
| Check for compaction | `python3 ~/clawd/data/de-neuralyzer/session-analyzer.py --detect` |
| Generate context | `python3 ~/clawd/data/de-neuralyzer/session-analyzer.py` |
| View summary | `python3 ~/clawd/data/de-neuralyzer/session-analyzer.py --summary` |
| View recent requests | `cat ~/clawd/data/de-neuralyzer/current-context.json \| jq '.recent_user_requests'` |
| View active tasks | `cat ~/clawd/data/de-neuralyzer/current-context.json \| jq '.active_tasks'` |

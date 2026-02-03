# De-Neuralyzer 🧠🔄

*"The memory compaction is like the neuralyzer from Men in Black. This is the De-Neuralyzer."*

## The Problem

When Claude's context window fills up, Clawdbot performs **memory compaction** - removing older messages to make room for new ones. This causes the agent to forget:

- What you were just working on
- The context of current tasks
- Recent decisions and progress
- Active subagent missions

This hurts workflow continuity.

## The Solution

**De-Neuralyzer** is a context recovery system that:

1. **Analyzes session transcripts** - All conversations are logged in `~/.clawdbot/agents/main/sessions/`
2. **Extracts key context** - Recent requests, active tasks, decisions, files touched
3. **Provides recovery data** - JSON output that can be read to restore context
4. **Detects compaction events** - Knows when memory was wiped

## Files

| File | Purpose |
|------|---------|
| `session-analyzer.py` | Python script to analyze session transcripts |
| `current-context.json` | Extracted context (regenerate when needed) |
| `context-recovery-protocol.md` | Step-by-step recovery process |
| `README.md` | This file |

## Quick Start

### 1. Generate Current Context
```bash
python3 /home/ec2-user/clawd/data/de-neuralyzer/session-analyzer.py
```

### 2. View the Context
```bash
cat /home/ec2-user/clawd/data/de-neuralyzer/current-context.json
```

### 3. Quick Summary
```bash
python3 /home/ec2-user/clawd/data/de-neuralyzer/session-analyzer.py --summary
```

## What It Extracts

### From Session Transcripts
- **Recent User Requests** - Last 10 messages from the user
- **Active Tasks** - Tasks that appear in-progress
- **Key Decisions** - Important decisions made
- **Conversation Summary** - Human-readable recent exchange

### From Compaction Events
- **Files Read** - What files were accessed before compaction
- **Files Modified** - What files were changed
- **Token Count** - How many tokens were in context
- **Compaction Timestamp** - When compaction occurred

## Integration

### HEARTBEAT.md Addition
Add to your HEARTBEAT.md:
```markdown
## Context Recovery
- Read `/home/ec2-user/clawd/data/de-neuralyzer/current-context.json` if context seems missing
- Check `recent_user_requests` and `active_tasks` to resume work
```

### AGENTS.md Addition
Add to the "Every Session" section:
```markdown
5. **If disoriented** - Run `python3 ~/clawd/data/de-neuralyzer/session-analyzer.py --summary`
```

### Cron Job (Optional)
Regenerate context every 5 minutes:
```bash
*/5 * * * * python3 /home/ec2-user/clawd/data/de-neuralyzer/session-analyzer.py 2>/dev/null
```

## How It Works

1. **Session File Location**: `~/.clawdbot/agents/main/sessions/*.jsonl`
   - Each line is a JSON object
   - Types: `session`, `message`, `compaction`, `custom`

2. **Compaction Events** contain:
   ```json
   {
     "type": "compaction",
     "timestamp": "2026-02-01T04:41:04.673Z",
     "summary": "...",
     "firstKeptEntryId": "abc123",
     "tokensBefore": 180000,
     "details": {
       "readFiles": [...],
       "modifiedFiles": [...]
     }
   }
   ```

3. **Message Events** contain:
   ```json
   {
     "type": "message",
     "message": {
       "role": "user|assistant|toolResult",
       "content": [...]
     }
   }
   ```

4. **The Analyzer**:
   - Finds the main session (largest active `.jsonl` file)
   - Locates compaction events
   - Extracts messages since last compaction
   - Identifies patterns for tasks, decisions, requests
   - Outputs structured JSON for context recovery

## Statistics

The main session typically contains:
- 8000+ messages
- 40+ compaction events
- 1000+ custom events (tool calls, etc.)

All of this is searchable and extractable for context recovery.

## Future Improvements

- [ ] Auto-trigger on compaction detection
- [ ] Summarize context using LLM
- [ ] Store context snapshots before compaction
- [ ] Build searchable context index
- [ ] Integrate with Supermemory for persistent storage

---

*The De-Neuralyzer: Because forgetting shouldn't be permanent.*

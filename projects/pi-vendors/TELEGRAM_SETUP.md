# Telegram Bot Setup for SCOUT + Head Agents Group

## Step 1: Create SCOUT Bot

1. Open Telegram, message **@BotFather**
2. Send `/newbot`
3. Name: `PI Vendors Scout`
4. Username: `PIVendorScoutBot` (must be unique, add numbers if taken)
5. Copy the **bot token** BotFather gives you

**Send me the token and I'll configure SCOUT to respond via that bot.**

---

## Step 2: Create Head Agents Group

1. Create a new Telegram group
2. Name it: `Kurios Head Agents` (or whatever you prefer)
3. Add me (Sierra) to the group
4. Add SCOUT bot to the group (once created)
5. Add any other head agent bots you create

**Purpose:** All head agents report here, collaborate, and you get a single feed of updates.

---

## Step 3: Configure Clawdbot for Multiple Bots

Once you have the SCOUT bot token, I'll:
1. Add it as a new Telegram channel in Clawdbot config
2. Route messages to the SCOUT session
3. Set up the group chat for announcements

---

## Head Agents Architecture

```
┌─────────────────────────────────────────────────┐
│           KURIOS HEAD AGENTS GROUP              │
│                                                 │
│  @Sierra (Main) - Brain, orchestration          │
│  @PIVendorScoutBot - PI Vendors data collection │
│  @[Future] - Other project leads                │
│                                                 │
│  Daily standups, cross-project updates          │
└─────────────────────────────────────────────────┘
         │
         ├── Sierra DM (you ↔ me directly)
         │
         ├── SCOUT DM (you ↔ SCOUT for PI Vendors)
         │
         └── Group (all agents collaborate)
```

---

## Bot Commands for SCOUT

Once configured, SCOUT will respond to:

- `/status` - Current scraping status
- `/stats` - Data collection statistics
- `/latest` - Latest findings
- `/search [term]` - Search collected data
- `/report` - Generate daily report
- `/vendors` - List tracked vendors
- `/insights` - Key buyer insights found

---

## Next Steps

1. Create the SCOUT bot via BotFather
2. Send me the token
3. Create the Head Agents group
4. Add me + SCOUT to the group
5. I'll configure everything

Ready when you are!

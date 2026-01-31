#!/usr/bin/env python3
"""
SCOUT - Telegram Bot Interface for PI Vendor Intelligence System
"""
import asyncio
import json
import logging
import os
import sys
import functools
from datetime import datetime
from pathlib import Path
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup paths
PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR / "agents"))

# Logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("scout_bot")

# Lazy imports to avoid circular issues
def get_db_stats():
    from base_scraper import get_db_stats as _get_db_stats
    return _get_db_stats()

def get_extraction_stats():
    from profile_extractor import get_extraction_stats as _get_extraction_stats
    return _get_extraction_stats()

def get_coordinator():
    from coordinator import coordinator
    return coordinator

def get_matching_engine():
    from matching_engine import MatchingEngine
    return MatchingEngine()

# Load config
CONFIG_PATH = Path.home() / ".config" / "scout-bot" / "config.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

BOT_TOKEN = CONFIG["bot_token"]

# Authorized users (add your Telegram user ID)
AUTHORIZED_USERS = [
    1968536547,  # Marko
]


def authorized(func):
    """Decorator to check authorization"""
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        logger.info(f"Auth check for user {user_id} on {func.__name__}")
        if user_id not in AUTHORIZED_USERS:
            await update.message.reply_text("⛔ Unauthorized. Contact admin for access.")
            logger.warning(f"Unauthorized access attempt: {user_id}")
            return
        return await func(update, context)
    return wrapper


# ─────────────────────────────────────────
# COMMAND HANDLERS
# ─────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    await update.message.reply_text(
        f"🏔️ **SCOUT - PI Vendor Intelligence**\n\n"
        f"Hey {user.first_name}! I'm SCOUT, your data assistant for "
        f"personal injury vendor intelligence.\n\n"
        f"**Commands:**\n"
        f"/status - System status\n"
        f"/stats - Database statistics\n"
        f"/vendors - List all tracked vendors\n"
        f"/vendor <name> - Get vendor details\n"
        f"/search <query> - Search data\n"
        f"/rankings - Vendor reputation rankings\n"
        f"/report - Generate daily report\n"
        f"/scrape <source> - Trigger manual scrape\n"
        f"/help - This help message",
        parse_mode="Markdown"
    )


@authorized
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    await update.message.reply_text("⏳ Fetching status...")
    
    try:
        coord = get_coordinator()
        summary = coord.get_summary()
        await update.message.reply_text(summary, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Status error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


@authorized
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    try:
        db_stats = get_db_stats()
        ext_stats = get_extraction_stats()
        logger.info(f"Stats: db={db_stats}, ext={ext_stats}")
        
        msg = "📊 **Database Statistics**\n\n"
        msg += f"**Raw Data:** {db_stats.get('total_raw', 0)} items\n"
        
        for source, count in db_stats.get('raw_by_source', {}).items():
            msg += f"  • {source}: {count}\n"
        
        msg += f"\n**Processed:** {db_stats.get('processed', 0)}\n"
        msg += f"**Pending:** {db_stats.get('unprocessed', 0)}\n"
        msg += f"\n**Profiles:**\n"
        msg += f"  • Vendors: {ext_stats.get('total_vendors', 0)}\n"
        msg += f"  • Buyers: {ext_stats.get('total_buyers', 0)}\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


@authorized
async def vendors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /vendors command - list all vendors"""
    try:
        engine = get_matching_engine()
        all_vendors = engine.get_all_vendors()
        
        if not all_vendors:
            await update.message.reply_text("📭 No vendors in database yet.")
            return
        
        msg = f"🏢 **Tracked Vendors ({len(all_vendors)})**\n\n"
        
        for v in all_vendors[:20]:  # Limit to 20
            name = v.get("basics", {}).get("name", v.get("slug", "Unknown"))
            rep = v.get("reputation", {}).get("aggregate_score", "N/A")
            msg += f"• {name} (Rep: {rep})\n"
        
        if len(all_vendors) > 20:
            msg += f"\n... and {len(all_vendors) - 20} more"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


@authorized
async def vendor_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /vendor <name> command"""
    if not context.args:
        await update.message.reply_text("Usage: /vendor <name>\nExample: /vendor scorpion")
        return
    
    query = " ".join(context.args).lower()
    
    try:
        engine = get_matching_engine()
        all_vendors = engine.get_all_vendors()
        
        # Find matching vendor
        vendor = None
        for v in all_vendors:
            name = v.get("basics", {}).get("name", "").lower()
            slug = v.get("slug", "").lower()
            if query in name or query in slug:
                vendor = v
                break
        
        if not vendor:
            await update.message.reply_text(f"❌ Vendor '{query}' not found.")
            return
        
        basics = vendor.get("basics", {})
        services = vendor.get("services", {})
        reputation = vendor.get("reputation", {})
        
        msg = f"🏢 **{basics.get('name', 'Unknown')}**\n\n"
        
        if basics.get("url"):
            msg += f"🔗 {basics['url']}\n"
        if basics.get("description"):
            msg += f"\n📝 {basics['description'][:200]}...\n"
        
        msg += f"\n**Services:**\n"
        for svc in services.get("types", []):
            msg += f"  • {svc}\n"
        
        msg += f"\n**Ratings:**\n"
        for platform, data in reputation.get("ratings", {}).items():
            if isinstance(data, dict) and data.get("score"):
                msg += f"  • {platform}: {data['score']} ({data.get('count', 'N/A')} reviews)\n"
        
        red_flags = vendor.get("red_flags", [])
        if red_flags:
            msg += f"\n⚠️ **Red Flags ({len(red_flags)}):**\n"
            for flag in red_flags[:3]:
                msg += f"  • {flag.get('description', 'Unknown')[:100]}\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


@authorized
async def rankings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rankings command"""
    try:
        engine = get_matching_engine()
        vendor_rankings = engine.get_vendor_rankings()
        
        if not vendor_rankings:
            await update.message.reply_text("📭 No vendor rankings available yet.")
            return
        
        msg = "🏆 **Vendor Reputation Rankings**\n\n"
        
        for i, v in enumerate(vendor_rankings[:15], 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            flags = f" ⚠️{v['red_flags']}" if v['red_flags'] > 0 else ""
            msg += f"{emoji} **{v['name']}** - {v['reputation_score']:.0f}/100{flags}\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


@authorized
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /search command"""
    if not context.args:
        await update.message.reply_text("Usage: /search <query>\nExample: /search lead quality")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Searching for: {query}\n\n(Full search coming soon)")


@authorized
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /report command - generate daily report"""
    await update.message.reply_text("📝 Generating report...")
    
    try:
        db_stats = get_db_stats()
        ext_stats = get_extraction_stats()
        engine = get_matching_engine()
        rankings = engine.get_vendor_rankings()
        
        msg = f"📊 **Daily Intelligence Report**\n"
        msg += f"_{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}_\n\n"
        
        msg += f"**Data Pipeline:**\n"
        msg += f"• Raw data: {db_stats.get('total_raw', 0)} items\n"
        msg += f"• Processed: {db_stats.get('processed', 0)}\n"
        msg += f"• Pending: {db_stats.get('unprocessed', 0)}\n\n"
        
        msg += f"**Profiles Built:**\n"
        msg += f"• Vendors: {ext_stats.get('total_vendors', 0)}\n"
        msg += f"• Buyer Insights: {ext_stats.get('total_buyers', 0)}\n\n"
        
        if rankings:
            msg += f"**Top 5 Vendors by Reputation:**\n"
            for i, v in enumerate(rankings[:5], 1):
                msg += f"{i}. {v['name']} ({v['reputation_score']:.0f})\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating report: {e}")


@authorized
async def scrape(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /scrape command - trigger manual scrape"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /scrape <source>\n"
            "Sources: reddit, reviews, linkedin, all"
        )
        return
    
    source = context.args[0].lower()
    
    if source == "all":
        await update.message.reply_text("🚀 Starting all scrapers... This will take a while.")
        # Would trigger coordinator.run_all() here
    elif source in ["reddit", "reviews", "linkedin"]:
        await update.message.reply_text(f"🚀 Starting {source} scraper...")
        # Would trigger coordinator.run_scraper(source) here
    else:
        await update.message.reply_text(f"❌ Unknown source: {source}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await start(update, context)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    text = update.message.text.lower()
    
    # Simple keyword responses
    if "status" in text:
        await status(update, context)
    elif "help" in text:
        await help_command(update, context)
    else:
        await update.message.reply_text(
            "👋 I'm SCOUT! Use /help to see available commands."
        )


async def post_to_group(context: ContextTypes.DEFAULT_TYPE, message: str):
    """Post a message to the Head Agents group"""
    config_path = PROJECT_DIR / "config" / "scout_config.json"
    try:
        with open(config_path) as f:
            config = json.load(f)
        group_id = config.get("head_agents_group")
        if group_id:
            await context.bot.send_message(
                chat_id=group_id,
                text=message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.info(f"Posted to group {group_id}")
    except Exception as e:
        logger.error(f"Failed to post to group: {e}")


@authorized
async def setgroup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setgroup command - save current chat as Head Agents group"""
    chat = update.effective_chat
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("❌ Run this command in a group chat.")
        return
    
    config_path = PROJECT_DIR / "config" / "scout_config.json"
    try:
        with open(config_path) as f:
            config = json.load(f)
        
        config["head_agents_group"] = chat.id
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        await update.message.reply_text(
            f"✅ **Head Agents Group Set!**\n\n"
            f"Group: {chat.title}\n"
            f"ID: `{chat.id}`\n\n"
            f"I'll post high-value AI agent use cases here.",
            parse_mode="Markdown"
        )
        logger.info(f"Set Head Agents group to {chat.id} ({chat.title})")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


@authorized  
async def scanx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /scanx command - manually trigger X scan for agent use cases"""
    await update.message.reply_text("🔍 Scanning X for AI agent use cases... (this takes ~2 min)")
    
    try:
        # Import and run X scraper
        sys.path.insert(0, str(PROJECT_DIR / "agents" / "scrapers"))
        from x_scraper import XScraper
        
        scraper = XScraper()
        high_value = await scraper.scrape()
        
        if not high_value:
            await update.message.reply_text("📭 No high-value posts found this scan.")
            return
        
        await update.message.reply_text(f"✅ Found {len(high_value)} high-value posts!")
        
        # Post top results
        for tweet in high_value[:5]:
            msg = f"🔍 **{tweet.get('query', 'AI Agent')}**\n\n"
            content = tweet.get('content', tweet.get('snippet', ''))[:400]
            msg += f"{content}\n\n"
            msg += f"🔗 {tweet.get('url', '')}"
            
            await update.message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=True)
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"X scan error: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


def main():
    """Start the bot"""
    logger.info("Starting SCOUT bot...")
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("vendors", vendors))
    app.add_handler(CommandHandler("vendor", vendor_detail))
    app.add_handler(CommandHandler("rankings", rankings))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("scrape", scrape))
    app.add_handler(CommandHandler("scanx", scanx))
    app.add_handler(CommandHandler("setgroup", setgroup))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start polling
    logger.info("SCOUT is online!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

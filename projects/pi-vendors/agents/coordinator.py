#!/usr/bin/env python3
"""
Main Coordinator - Orchestrates all scrapers and processing
Runs 24/7, manages scrape schedules, triggers AI processing
"""
import asyncio
import json
import logging
import os
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# Setup paths
PROJECT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_DIR / "agents"))
sys.path.insert(0, str(PROJECT_DIR / "agents" / "scrapers"))

from base_scraper import get_db_stats, DB_PATH
from profile_extractor import process_unprocessed_data, get_extraction_stats
from matching_engine import MatchingEngine

# Logging
LOG_DIR = PROJECT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "coordinator.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("coordinator")


class Coordinator:
    """Main orchestrator for the PI Vendor Intelligence System"""
    
    def __init__(self):
        self.running = False
        self.scrapers = {}
        self.last_runs = {}
        self.stats = {
            "started_at": None,
            "total_scrapes": 0,
            "total_extractions": 0,
            "errors": 0
        }
        
        # Schedule intervals (in hours)
        self.schedules = {
            "reddit": 4,      # Every 4 hours
            "reviews": 24,    # Daily
            "linkedin": 24,   # Daily
        }
        
        self.matching_engine = MatchingEngine()
    
    async def load_scrapers(self):
        """Dynamically load scraper modules"""
        try:
            from reddit_scraper import RedditScraper
            self.scrapers["reddit"] = RedditScraper()
            logger.info("Loaded Reddit scraper")
        except Exception as e:
            logger.error(f"Failed to load Reddit scraper: {e}")
        
        try:
            from review_scraper import ReviewScraper
            self.scrapers["reviews"] = ReviewScraper()
            logger.info("Loaded Review scraper")
        except Exception as e:
            logger.error(f"Failed to load Review scraper: {e}")
        
        try:
            from linkedin_scraper import LinkedInScraper
            self.scrapers["linkedin"] = LinkedInScraper()
            logger.info("Loaded LinkedIn scraper")
        except Exception as e:
            logger.error(f"Failed to load LinkedIn scraper: {e}")
    
    def should_run(self, scraper_name: str) -> bool:
        """Check if scraper should run based on schedule"""
        if scraper_name not in self.last_runs:
            return True
        
        interval = self.schedules.get(scraper_name, 24)
        last_run = self.last_runs[scraper_name]
        next_run = last_run + timedelta(hours=interval)
        
        return datetime.now() >= next_run
    
    async def run_scraper(self, name: str):
        """Run a specific scraper"""
        if name not in self.scrapers:
            logger.warning(f"Scraper {name} not found")
            return
        
        scraper = self.scrapers[name]
        logger.info(f"Starting {name} scraper")
        
        try:
            await scraper.scrape()
            self.last_runs[name] = datetime.now()
            self.stats["total_scrapes"] += 1
            logger.info(f"Completed {name} scraper")
        except Exception as e:
            logger.error(f"Error in {name} scraper: {e}")
            self.stats["errors"] += 1
    
    async def run_extraction(self, batch_size: int = 50):
        """Run AI extraction on unprocessed data"""
        logger.info("Starting profile extraction")
        
        try:
            result = process_unprocessed_data(batch_size)
            self.stats["total_extractions"] += result.get("processed", 0)
            logger.info(f"Extraction complete: {result}")
        except Exception as e:
            logger.error(f"Extraction error: {e}")
            self.stats["errors"] += 1
    
    def get_status(self) -> Dict:
        """Get current system status"""
        db_stats = get_db_stats()
        extraction_stats = get_extraction_stats()
        
        return {
            "status": "running" if self.running else "stopped",
            "started_at": self.stats["started_at"],
            "uptime": str(datetime.now() - datetime.fromisoformat(self.stats["started_at"])) if self.stats["started_at"] else None,
            "scrapers": {
                name: {
                    "status": scraper.get_status(),
                    "last_run": self.last_runs.get(name, "never").isoformat() if isinstance(self.last_runs.get(name), datetime) else "never",
                    "next_run_in": f"{self.schedules.get(name, 24)}h"
                }
                for name, scraper in self.scrapers.items()
            },
            "database": db_stats,
            "extraction": extraction_stats,
            "totals": self.stats
        }
    
    def get_summary(self) -> str:
        """Get human-readable summary"""
        status = self.get_status()
        db = status.get("database", {})
        ext = status.get("extraction", {})
        
        lines = [
            "📊 **PI Vendor Intelligence Status**",
            "",
            f"🔄 Status: {status['status'].upper()}",
            f"⏱️ Uptime: {status.get('uptime', 'N/A')}",
            "",
            "**Data Collection:**"
        ]
        
        for source, count in db.get("raw_by_source", {}).items():
            lines.append(f"  • {source}: {count} items")
        
        lines.extend([
            "",
            f"📦 Total Raw: {db.get('total_raw', 0)}",
            f"✅ Processed: {db.get('processed', 0)}",
            f"⏳ Pending: {db.get('unprocessed', 0)}",
            "",
            "**Profiles:**",
            f"  • Vendors: {ext.get('total_vendors', 0)}",
            f"  • Buyers: {ext.get('total_buyers', 0)}",
            "",
            "**Recent Runs:**"
        ])
        
        for run in db.get("recent_runs", [])[:5]:
            lines.append(f"  • {run['source']}: {run['scraped']} scraped, {run['saved']} saved")
        
        return "\n".join(lines)
    
    async def main_loop(self):
        """Main coordinator loop"""
        self.running = True
        self.stats["started_at"] = datetime.now().isoformat()
        
        await self.load_scrapers()
        logger.info("Coordinator started")
        
        while self.running:
            try:
                # Check each scraper
                for name in self.scrapers:
                    if self.should_run(name):
                        await self.run_scraper(name)
                        # Process after each scrape
                        await self.run_extraction(25)
                        await asyncio.sleep(60)  # Brief pause between scrapers
                
                # Sleep before next check
                logger.info("Cycle complete, sleeping 30 minutes")
                await asyncio.sleep(1800)  # 30 minutes
                
            except asyncio.CancelledError:
                logger.info("Received shutdown signal")
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                await asyncio.sleep(300)  # 5 min on error
        
        logger.info("Coordinator stopped")
    
    def stop(self):
        """Stop the coordinator"""
        self.running = False


# Global coordinator instance
coordinator = Coordinator()


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}")
    coordinator.stop()


async def main():
    """Entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    await coordinator.main_loop()


if __name__ == "__main__":
    asyncio.run(main())

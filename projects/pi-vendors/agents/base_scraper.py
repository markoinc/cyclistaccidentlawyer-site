"""
Base scraper class - all source scrapers inherit from this
"""
import json
import hashlib
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "vendor_intel.db"

class BaseScraper(ABC):
    """Base class for all data source scrapers"""
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.logger = logging.getLogger(source_name)
        self.stats = {
            "started_at": None,
            "items_scraped": 0,
            "items_saved": 0,
            "errors": 0
        }
        self._ensure_dirs()
        self._ensure_db()
    
    def _ensure_dirs(self):
        """Create data directories if needed"""
        (DATA_DIR / "raw" / self.source_name).mkdir(parents=True, exist_ok=True)
        (DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)
        (DATA_DIR / "profiles" / "vendors").mkdir(parents=True, exist_ok=True)
        (DATA_DIR / "profiles" / "buyers").mkdir(parents=True, exist_ok=True)
    
    def _ensure_db(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Raw data table - dedupe by content hash
        c.execute('''
            CREATE TABLE IF NOT EXISTS raw_data (
                id INTEGER PRIMARY KEY,
                source TEXT NOT NULL,
                source_url TEXT,
                content_hash TEXT UNIQUE,
                content TEXT,
                metadata TEXT,
                scraped_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT 0
            )
        ''')
        
        # Vendor profiles
        c.execute('''
            CREATE TABLE IF NOT EXISTS vendors (
                id TEXT PRIMARY KEY,
                slug TEXT UNIQUE,
                name TEXT NOT NULL,
                data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Buyer profiles
        c.execute('''
            CREATE TABLE IF NOT EXISTS buyers (
                id TEXT PRIMARY KEY,
                source TEXT,
                source_url TEXT,
                data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Vendor mentions (links raw data to vendors)
        c.execute('''
            CREATE TABLE IF NOT EXISTS vendor_mentions (
                id INTEGER PRIMARY KEY,
                vendor_id TEXT,
                raw_data_id INTEGER,
                sentiment TEXT,
                summary TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vendor_id) REFERENCES vendors(id),
                FOREIGN KEY (raw_data_id) REFERENCES raw_data(id)
            )
        ''')
        
        # Scrape stats
        c.execute('''
            CREATE TABLE IF NOT EXISTS scrape_runs (
                id INTEGER PRIMARY KEY,
                source TEXT,
                started_at DATETIME,
                completed_at DATETIME,
                items_scraped INTEGER,
                items_saved INTEGER,
                errors INTEGER,
                notes TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def content_hash(self, content: str) -> str:
        """Generate hash for deduplication"""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def save_raw(self, content: str, source_url: str = None, metadata: Dict = None) -> bool:
        """Save raw scraped content with deduplication"""
        c_hash = self.content_hash(content)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        try:
            c.execute('''
                INSERT INTO raw_data (source, source_url, content_hash, content, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                self.source_name,
                source_url,
                c_hash,
                content,
                json.dumps(metadata) if metadata else None
            ))
            conn.commit()
            self.stats["items_saved"] += 1
            self.logger.debug(f"Saved: {source_url}")
            return True
        except sqlite3.IntegrityError:
            # Duplicate content
            self.logger.debug(f"Duplicate: {source_url}")
            return False
        finally:
            conn.close()
    
    def save_raw_json(self, data: Dict, filename: str = None):
        """Save raw data as JSON file (backup)"""
        if not filename:
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.stats['items_scraped']}.json"
        
        path = DATA_DIR / "raw" / self.source_name / filename
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return path
    
    def log_run(self, notes: str = None):
        """Log scrape run stats"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO scrape_runs (source, started_at, completed_at, items_scraped, items_saved, errors, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.source_name,
            self.stats["started_at"],
            datetime.now().isoformat(),
            self.stats["items_scraped"],
            self.stats["items_saved"],
            self.stats["errors"],
            notes
        ))
        conn.commit()
        conn.close()
    
    def start(self):
        """Mark scrape start"""
        self.stats["started_at"] = datetime.now().isoformat()
        self.logger.info(f"Starting {self.source_name} scraper")
    
    def finish(self, notes: str = None):
        """Complete scrape run"""
        self.log_run(notes)
        self.logger.info(
            f"Finished {self.source_name}: "
            f"{self.stats['items_scraped']} scraped, "
            f"{self.stats['items_saved']} saved, "
            f"{self.stats['errors']} errors"
        )
    
    @abstractmethod
    async def scrape(self) -> List[Dict]:
        """Override in subclass - main scrape logic"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        """Override in subclass - return current status"""
        pass


def get_db_stats() -> Dict:
    """Get overall database statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    stats = {}
    
    # Raw data by source
    c.execute("SELECT source, COUNT(*) FROM raw_data GROUP BY source")
    stats["raw_by_source"] = dict(c.fetchall())
    
    # Total raw
    c.execute("SELECT COUNT(*) FROM raw_data")
    stats["total_raw"] = c.fetchone()[0]
    
    # Processed vs unprocessed
    c.execute("SELECT processed, COUNT(*) FROM raw_data GROUP BY processed")
    processed = dict(c.fetchall())
    stats["processed"] = processed.get(1, 0)
    stats["unprocessed"] = processed.get(0, 0)
    
    # Vendors
    c.execute("SELECT COUNT(*) FROM vendors")
    stats["vendors"] = c.fetchone()[0]
    
    # Buyers
    c.execute("SELECT COUNT(*) FROM buyers")
    stats["buyers"] = c.fetchone()[0]
    
    # Recent runs
    c.execute("""
        SELECT source, started_at, items_scraped, items_saved 
        FROM scrape_runs 
        ORDER BY started_at DESC 
        LIMIT 10
    """)
    stats["recent_runs"] = [
        {"source": r[0], "started": r[1], "scraped": r[2], "saved": r[3]}
        for r in c.fetchall()
    ]
    
    conn.close()
    return stats

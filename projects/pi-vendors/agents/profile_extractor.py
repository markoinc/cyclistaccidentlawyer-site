"""
AI-powered profile extractor
Takes raw scraped data and extracts structured vendor/buyer profiles
"""
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("profile_extractor")

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "vendor_intel.db"
SCHEMAS_PATH = Path(__file__).parent.parent / "config" / "schemas.json"

# Load schemas
with open(SCHEMAS_PATH) as f:
    SCHEMAS = json.load(f)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


BUYER_EXTRACTION_PROMPT = '''Extract buyer profile data from this text. Return ONLY valid JSON matching this schema:

{schema}

Text to analyze:
---
{text}
---

If you can't determine a field, use null. Extract ALL pain points, vendor mentions, and budget signals you can find.
Return ONLY the JSON object, no explanation.'''


VENDOR_EXTRACTION_PROMPT = '''Extract vendor profile data from this text. Return ONLY valid JSON matching this schema:

{schema}

Text to analyze:
---
{text}
---

Focus on: services offered, pricing mentioned, reviews/ratings, complaints, and differentiators.
Return ONLY the JSON object, no explanation.'''


def extract_buyer_profile(text: str, source_url: str = None) -> Optional[Dict]:
    """Extract buyer profile from raw text using GPT-4"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": BUYER_EXTRACTION_PROMPT.format(
                    schema=json.dumps(SCHEMAS["buyer_profile"], indent=2),
                    text=text[:8000]  # Limit text length
                )
            }],
            temperature=0,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        
        # Try to parse JSON
        try:
            profile = json.loads(result)
            profile["source_url"] = source_url
            profile["extracted_at"] = datetime.now().isoformat()
            return profile
        except json.JSONDecodeError:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                profile = json.loads(json_match.group())
                profile["source_url"] = source_url
                profile["extracted_at"] = datetime.now().isoformat()
                return profile
            logger.error(f"Failed to parse JSON from response")
            return None
            
    except Exception as e:
        logger.error(f"Buyer extraction error: {e}")
        return None


def extract_vendor_profile(text: str, vendor_name: str = None, source_url: str = None) -> Optional[Dict]:
    """Extract vendor profile from raw text using GPT-4"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": VENDOR_EXTRACTION_PROMPT.format(
                    schema=json.dumps(SCHEMAS["vendor_profile"], indent=2),
                    text=text[:8000]
                )
            }],
            temperature=0,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        
        try:
            profile = json.loads(result)
            if vendor_name:
                profile["basics"] = profile.get("basics", {})
                profile["basics"]["name"] = vendor_name
            profile["data_sources"] = [source_url] if source_url else []
            profile["last_updated"] = datetime.now().isoformat()
            return profile
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                profile = json.loads(json_match.group())
                return profile
            return None
            
    except Exception as e:
        logger.error(f"Vendor extraction error: {e}")
        return None


def classify_content(text: str) -> Tuple[str, float]:
    """Classify if content is buyer-focused or vendor-focused"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f'''Classify this text as either:
- "buyer" - Discussion FROM a lawyer/law firm about vendors, leads, marketing
- "vendor" - Information ABOUT a specific vendor company (reviews, company info)
- "both" - Contains both buyer insights and vendor information
- "neither" - Not relevant

Text:
{text[:2000]}

Return JSON: {{"classification": "buyer|vendor|both|neither", "confidence": 0.0-1.0, "reason": "brief reason"}}'''
            }],
            temperature=0,
            max_tokens=200
        )
        
        result = json.loads(response.choices[0].message.content)
        return result["classification"], result["confidence"]
        
    except:
        return "neither", 0.0


def process_unprocessed_data(limit: int = 50) -> Dict:
    """Process unprocessed raw data and extract profiles"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get unprocessed items
    c.execute("""
        SELECT id, source, source_url, content, metadata 
        FROM raw_data 
        WHERE processed = 0 
        LIMIT ?
    """, (limit,))
    
    rows = c.fetchall()
    logger.info(f"Processing {len(rows)} unprocessed items")
    
    stats = {
        "processed": 0,
        "buyers_extracted": 0,
        "vendors_extracted": 0,
        "skipped": 0,
        "errors": 0
    }
    
    for row in rows:
        data_id, source, source_url, content, metadata_str = row
        
        try:
            # Parse content if it's JSON
            try:
                content_data = json.loads(content)
                # Flatten to text for analysis
                if isinstance(content_data, dict):
                    text = json.dumps(content_data, indent=2)
                else:
                    text = str(content_data)
            except:
                text = content
            
            metadata = json.loads(metadata_str) if metadata_str else {}
            
            # Classify content
            classification, confidence = classify_content(text)
            
            if classification == "neither" or confidence < 0.5:
                stats["skipped"] += 1
            elif classification == "buyer" or classification == "both":
                profile = extract_buyer_profile(text, source_url)
                if profile:
                    save_buyer_profile(profile, source, source_url)
                    stats["buyers_extracted"] += 1
            
            if classification == "vendor" or classification == "both":
                vendor_name = metadata.get("vendor")
                profile = extract_vendor_profile(text, vendor_name, source_url)
                if profile:
                    save_vendor_profile(profile)
                    stats["vendors_extracted"] += 1
            
            # Mark as processed
            c.execute("UPDATE raw_data SET processed = 1 WHERE id = ?", (data_id,))
            stats["processed"] += 1
            
        except Exception as e:
            logger.error(f"Error processing {data_id}: {e}")
            stats["errors"] += 1
    
    conn.commit()
    conn.close()
    
    logger.info(f"Processing complete: {stats}")
    return stats


def save_buyer_profile(profile: Dict, source: str, source_url: str):
    """Save extracted buyer profile to database"""
    import uuid
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    profile_id = str(uuid.uuid4())[:8]
    
    c.execute("""
        INSERT INTO buyers (id, source, source_url, data)
        VALUES (?, ?, ?, ?)
    """, (profile_id, source, source_url, json.dumps(profile)))
    
    conn.commit()
    conn.close()
    
    # Also save as JSON file
    path = DATA_DIR / "profiles" / "buyers" / f"{profile_id}.json"
    with open(path, 'w') as f:
        json.dump(profile, f, indent=2)
    
    logger.info(f"Saved buyer profile: {profile_id}")


def save_vendor_profile(profile: Dict):
    """Save or update vendor profile"""
    import uuid
    import re
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    name = profile.get("basics", {}).get("name", "unknown")
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    
    # Check if vendor exists
    c.execute("SELECT id, data FROM vendors WHERE slug = ?", (slug,))
    existing = c.fetchone()
    
    if existing:
        # Merge with existing data
        vendor_id = existing[0]
        existing_data = json.loads(existing[1])
        
        # Merge mentions
        existing_mentions = existing_data.get("mentions", [])
        new_mentions = profile.get("mentions", [])
        profile["mentions"] = existing_mentions + new_mentions
        
        # Merge data sources
        existing_sources = existing_data.get("data_sources", [])
        new_sources = profile.get("data_sources", [])
        profile["data_sources"] = list(set(existing_sources + new_sources))
        
        c.execute("""
            UPDATE vendors SET data = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (json.dumps(profile), vendor_id))
        
        logger.info(f"Updated vendor profile: {name}")
    else:
        vendor_id = str(uuid.uuid4())[:8]
        
        c.execute("""
            INSERT INTO vendors (id, slug, name, data)
            VALUES (?, ?, ?, ?)
        """, (vendor_id, slug, name, json.dumps(profile)))
        
        logger.info(f"Created vendor profile: {name}")
    
    conn.commit()
    conn.close()
    
    # Save as JSON file
    path = DATA_DIR / "profiles" / "vendors" / f"{slug}.json"
    with open(path, 'w') as f:
        json.dump(profile, f, indent=2)


def get_extraction_stats() -> Dict:
    """Get profile extraction statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    stats = {}
    
    c.execute("SELECT COUNT(*) FROM buyers")
    stats["total_buyers"] = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM vendors")
    stats["total_vendors"] = c.fetchone()[0]
    
    c.execute("SELECT processed, COUNT(*) FROM raw_data GROUP BY processed")
    processed = dict(c.fetchall())
    stats["raw_processed"] = processed.get(1, 0)
    stats["raw_pending"] = processed.get(0, 0)
    
    conn.close()
    return stats


if __name__ == "__main__":
    # Test run
    stats = process_unprocessed_data(10)
    print(f"Extraction stats: {stats}")

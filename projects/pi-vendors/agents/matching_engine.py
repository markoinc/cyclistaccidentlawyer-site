"""
Matching Engine - Scores vendor/buyer compatibility
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("matching_engine")

DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DATA_DIR / "vendor_intel.db"


class MatchingEngine:
    """Scores and matches vendors to buyer profiles"""
    
    def __init__(self):
        self.weights = {
            "pain_point_fit": 0.25,
            "budget_fit": 0.20,
            "geography_fit": 0.15,
            "reputation": 0.20,
            "case_type_match": 0.10,
            "size_fit": 0.10
        }
    
    def get_all_vendors(self) -> List[Dict]:
        """Load all vendor profiles"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, slug, name, data FROM vendors")
        vendors = []
        for row in c.fetchall():
            data = json.loads(row[3])
            data["id"] = row[0]
            data["slug"] = row[1]
            vendors.append(data)
        conn.close()
        return vendors
    
    def get_vendor(self, vendor_id: str) -> Optional[Dict]:
        """Get single vendor by ID or slug"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, slug, name, data FROM vendors 
            WHERE id = ? OR slug = ?
        """, (vendor_id, vendor_id))
        row = c.fetchone()
        conn.close()
        
        if row:
            data = json.loads(row[3])
            data["id"] = row[0]
            data["slug"] = row[1]
            return data
        return None
    
    def get_all_buyers(self) -> List[Dict]:
        """Load all buyer profiles"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, source, data FROM buyers")
        buyers = []
        for row in c.fetchall():
            data = json.loads(row[2])
            data["id"] = row[0]
            data["source"] = row[1]
            buyers.append(data)
        conn.close()
        return buyers
    
    def score_pain_point_fit(self, buyer: Dict, vendor: Dict) -> Tuple[float, List[str]]:
        """Score how well vendor addresses buyer pain points"""
        score = 50.0  # Base score
        reasons = []
        
        pain_points = buyer.get("signals", {}).get("pain_points", [])
        differentiators = vendor.get("differentiators", [])
        red_flags = vendor.get("red_flags", [])
        
        # Check if vendor differentiators address pain points
        for pain in pain_points:
            category = pain.get("category", "")
            desc = pain.get("description", "").lower()
            
            # Check differentiators
            for diff in differentiators:
                diff_lower = diff.lower()
                if category in diff_lower or any(word in diff_lower for word in desc.split()):
                    score += 10
                    reasons.append(f"Addresses pain: {category}")
                    break
        
        # Penalize for red flags matching pain points
        for flag in red_flags:
            flag_type = flag.get("type", "")
            flag_desc = flag.get("description", "").lower()
            
            for pain in pain_points:
                if pain.get("category") in flag_desc:
                    score -= 15
                    reasons.append(f"Red flag in pain area: {flag_type}")
        
        return min(max(score, 0), 100), reasons
    
    def score_budget_fit(self, buyer: Dict, vendor: Dict) -> Tuple[float, List[str]]:
        """Score budget compatibility"""
        score = 60.0  # Base - assume moderate fit
        reasons = []
        
        budget_signals = buyer.get("signals", {}).get("budget_signals", [])
        pricing_models = vendor.get("services", {}).get("pricing_models", [])
        
        if not budget_signals or not pricing_models:
            return score, ["Insufficient pricing data"]
        
        # Check decision style
        decision_style = buyer.get("signals", {}).get("decision_style", "unknown")
        
        if decision_style == "price_focused":
            # Price sensitive buyer - check for lower cost options
            for model in pricing_models:
                if "subscription" in model.get("model", "").lower():
                    score += 10
                    reasons.append("Subscription model available")
                if "retainer" in model.get("model", "").lower():
                    score -= 10
                    reasons.append("Retainer might be too expensive")
        
        return min(max(score, 0), 100), reasons
    
    def score_geography_fit(self, buyer: Dict, vendor: Dict) -> Tuple[float, List[str]]:
        """Score geographic coverage match"""
        score = 50.0
        reasons = []
        
        buyer_location = buyer.get("firm_info", {}).get("location", {})
        buyer_state = buyer_location.get("state")
        
        vendor_geo = vendor.get("services", {}).get("geography", [])
        vendor_states = vendor.get("services", {}).get("states_served", [])
        
        if "nationwide" in vendor_geo:
            score = 90
            reasons.append("Nationwide coverage")
        elif buyer_state and buyer_state in vendor_states:
            score = 95
            reasons.append(f"Serves {buyer_state}")
        elif buyer_state and vendor_states:
            score = 30
            reasons.append(f"Doesn't serve {buyer_state}")
        
        return score, reasons
    
    def score_reputation(self, vendor: Dict) -> Tuple[float, List[str]]:
        """Score vendor reputation"""
        reasons = []
        
        reputation = vendor.get("reputation", {})
        ratings = reputation.get("ratings", {})
        
        if not ratings:
            return 50, ["No rating data"]
        
        # Average across platforms
        scores = []
        for platform, data in ratings.items():
            if isinstance(data, dict) and data.get("score"):
                scores.append(float(data["score"]))
                if data.get("count", 0) > 100:
                    reasons.append(f"{platform}: {data['score']} ({data['count']} reviews)")
        
        if scores:
            avg = sum(scores) / len(scores)
            # Convert 5-star to 100-point
            score = (avg / 5) * 100
            return score, reasons
        
        return 50, ["Insufficient reviews"]
    
    def score_case_type_match(self, buyer: Dict, vendor: Dict) -> Tuple[float, List[str]]:
        """Score case type coverage"""
        buyer_types = buyer.get("firm_info", {}).get("case_types", [])
        vendor_types = vendor.get("services", {}).get("case_types", [])
        
        if not buyer_types:
            return 70, ["Buyer case types unknown"]
        
        if "all" in vendor_types:
            return 95, ["Covers all case types"]
        
        if not vendor_types:
            return 50, ["Vendor case types unknown"]
        
        # Calculate overlap
        overlap = len(set(buyer_types) & set(vendor_types))
        coverage = overlap / len(buyer_types) if buyer_types else 0
        
        score = coverage * 100
        reasons = [f"Covers {overlap}/{len(buyer_types)} case types"]
        
        return score, reasons
    
    def score_size_fit(self, buyer: Dict, vendor: Dict) -> Tuple[float, List[str]]:
        """Score firm size compatibility"""
        buyer_size = buyer.get("firm_info", {}).get("size", "unknown")
        buyer_volume = buyer.get("firm_info", {}).get("volume_tier", "unknown")
        
        # Most vendors can serve any size, but some are better for enterprise
        # This is a simplified heuristic
        score = 70
        reasons = []
        
        employee_count = vendor.get("basics", {}).get("employee_count", 0)
        
        if buyer_size in ["large", "mid"] and employee_count and employee_count > 50:
            score = 85
            reasons.append("Enterprise-capable vendor")
        elif buyer_size == "solo" and employee_count and employee_count < 50:
            score = 80
            reasons.append("Good fit for smaller firms")
        
        return score, reasons
    
    def calculate_match(self, buyer: Dict, vendor: Dict) -> Dict:
        """Calculate full match score between buyer and vendor"""
        breakdown = {}
        all_reasons = []
        warnings = []
        
        # Score each dimension
        pain_score, pain_reasons = self.score_pain_point_fit(buyer, vendor)
        breakdown["pain_point_fit"] = pain_score
        all_reasons.extend(pain_reasons)
        
        budget_score, budget_reasons = self.score_budget_fit(buyer, vendor)
        breakdown["budget_fit"] = budget_score
        all_reasons.extend(budget_reasons)
        
        geo_score, geo_reasons = self.score_geography_fit(buyer, vendor)
        breakdown["geography_fit"] = geo_score
        all_reasons.extend(geo_reasons)
        
        rep_score, rep_reasons = self.score_reputation(vendor)
        breakdown["reputation_score"] = rep_score
        all_reasons.extend(rep_reasons)
        
        case_score, case_reasons = self.score_case_type_match(buyer, vendor)
        breakdown["case_type_match"] = case_score
        all_reasons.extend(case_reasons)
        
        size_score, size_reasons = self.score_size_fit(buyer, vendor)
        breakdown["size_fit"] = size_score
        all_reasons.extend(size_reasons)
        
        # Calculate weighted overall score
        overall = sum(
            breakdown[k] * self.weights[k] 
            for k in self.weights.keys()
        )
        
        # Add warnings for red flags
        for flag in vendor.get("red_flags", []):
            if flag.get("severity") == "high":
                warnings.append(f"⚠️ {flag.get('type')}: {flag.get('description')}")
        
        return {
            "buyer_id": buyer.get("id"),
            "vendor_id": vendor.get("id"),
            "vendor_name": vendor.get("basics", {}).get("name"),
            "overall_score": round(overall, 1),
            "breakdown": {k: round(v, 1) for k, v in breakdown.items()},
            "reasons": all_reasons[:10],  # Top reasons
            "warnings": warnings,
            "calculated_at": datetime.now().isoformat()
        }
    
    def find_best_matches(self, buyer: Dict, top_n: int = 5) -> List[Dict]:
        """Find top N vendor matches for a buyer"""
        vendors = self.get_all_vendors()
        matches = []
        
        for vendor in vendors:
            match = self.calculate_match(buyer, vendor)
            matches.append(match)
        
        # Sort by overall score
        matches.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return matches[:top_n]
    
    def get_vendor_rankings(self) -> List[Dict]:
        """Rank all vendors by reputation score"""
        vendors = self.get_all_vendors()
        rankings = []
        
        for vendor in vendors:
            rep_score, reasons = self.score_reputation(vendor)
            rankings.append({
                "vendor_id": vendor.get("id"),
                "name": vendor.get("basics", {}).get("name"),
                "slug": vendor.get("slug"),
                "reputation_score": rep_score,
                "total_reviews": vendor.get("reputation", {}).get("total_reviews", 0),
                "red_flags": len(vendor.get("red_flags", [])),
                "reasons": reasons
            })
        
        rankings.sort(key=lambda x: x["reputation_score"], reverse=True)
        return rankings


def main():
    engine = MatchingEngine()
    
    # Get rankings
    rankings = engine.get_vendor_rankings()
    print("Vendor Rankings:")
    for i, v in enumerate(rankings[:10], 1):
        print(f"{i}. {v['name']}: {v['reputation_score']}")


if __name__ == "__main__":
    main()

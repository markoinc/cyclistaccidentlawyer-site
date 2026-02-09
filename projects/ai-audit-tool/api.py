#!/usr/bin/env python3
"""
FastAPI backend for AI & Local Visibility Audit Tool
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel, EmailStr
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

from analyzer import WebsiteAnalyzer, AuditResult
from enhanced_audit import EnhancedAuditor, EnhancedAuditResult
from pdf_generator import generate_pdf
from email_sender import send_audit_report

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI & Local Visibility Audit API",
    description="Automated website audit for AI visibility and local SEO",
    version="1.0.0"
)

# CORS - allow all origins for the audit tool
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lawyerseoaudit.com",
        "https://www.lawyerseoaudit.com",
        "https://kuriosbrand.com",
        "https://www.kuriosbrand.com",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread pool for blocking operations
executor = ThreadPoolExecutor(max_workers=4)

# Serve static files
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class AuditRequest(BaseModel):
    url: str
    email: EmailStr
    name: Optional[str] = None


class AuditResponse(BaseModel):
    success: bool
    message: str
    url: str
    business_name: Optional[str] = None
    ai_visibility_score: Optional[int] = None
    local_seo_score: Optional[int] = None
    total_score: Optional[int] = None
    ai_categories: Optional[list] = None
    local_categories: Optional[list] = None
    quick_wins: Optional[list] = None
    priority_fixes: Optional[list] = None


def run_audit_sync(url: str, email: str, name: Optional[str] = None, full_mode: bool = True) -> dict:
    """Run the audit synchronously (for thread pool)
    
    Args:
        url: Website URL to audit
        email: Email to send report to
        name: Optional business name override
        full_mode: If True, run full DataForSEO analysis for PDF (slower but comprehensive)
    """
    try:
        logger.info(f"Starting audit for {url} (full_mode={full_mode})")
        
        # Use enhanced auditor with DataForSEO
        auditor = EnhancedAuditor(url)
        
        if full_mode:
            # Full mode: comprehensive data for PDF (~30-60 sec)
            enhanced_result = auditor.run_full_audit()
        else:
            # Fast mode: quick results for web display (~5 sec)
            enhanced_result = auditor.run_fast_audit()
            
        result = enhanced_result.basic_result
        logger.info(f"Audit complete: AI={result.ai_visibility_score}, Local={result.local_seo_score}, API cost=${enhanced_result.api_cost:.4f}")
        
        # Generate PDF with enhanced data
        pdf_bytes = generate_pdf(result, enhanced_result if full_mode else None)
        logger.info(f"PDF generated: {len(pdf_bytes)} bytes")
        
        # Send email
        business_name = name or result.business_name or url
        email_sent = send_audit_report(
            to_email=email,
            business_name=business_name,
            url=url,
            ai_score=result.ai_visibility_score,
            local_score=result.local_seo_score,
            total_score=result.total_score,
            pdf_bytes=pdf_bytes
        )
        
        return {
            "success": True,
            "email_sent": email_sent,
            "result": result,
            "enhanced_result": enhanced_result,
            "api_cost": enhanced_result.api_cost
        }
        
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/")
async def root():
    """Serve the frontend"""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "ok", "service": "AI & Local Visibility Audit API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


def run_full_audit_background(url: str, email: str, name: Optional[str] = None):
    """Run full audit in background and send email with comprehensive PDF"""
    try:
        logger.info(f"Background: Starting FULL audit for {url}")
        run_audit_sync(url, email, name, full_mode=True)
        logger.info(f"Background: Full audit complete, email sent to {email}")
    except Exception as e:
        logger.error(f"Background audit failed: {e}")


@app.post("/audit", response_model=AuditResponse)
async def request_audit(request: AuditRequest, background_tasks: BackgroundTasks):
    """
    Request an audit for a website.
    
    Two-tier approach:
    1. FAST: Returns results to web in <10 seconds
    2. FULL: Sends comprehensive PDF via email (runs in background)
    """
    url = request.url
    if not url.startswith('http'):
        url = f"https://{url}"
    
    # Quick validation - try to parse the URL
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    loop = asyncio.get_event_loop()
    
    try:
        # FAST MODE: Quick results for web display (<10 sec)
        logger.info(f"Running FAST audit for {url}")
        
        # Run fast audit (no email)
        auditor = EnhancedAuditor(url)
        enhanced_result = await loop.run_in_executor(
            executor,
            auditor.run_fast_audit
        )
        audit_result = enhanced_result.basic_result
        
        logger.info(f"FAST audit complete in {enhanced_result.fast_mode_time:.1f}s: AI={audit_result.ai_visibility_score}, Local={audit_result.local_seo_score}")
        
        # FULL MODE: Schedule comprehensive audit + email in background
        background_tasks.add_task(run_full_audit_background, url, request.email, request.name)
        
        return AuditResponse(
            success=True,
            message="Audit complete! A detailed PDF report is being sent to your email.",
            url=url,
            business_name=audit_result.business_name,
            ai_visibility_score=audit_result.ai_visibility_score,
            local_seo_score=audit_result.local_seo_score,
            total_score=audit_result.total_score,
            ai_categories=[
                {"name": c.name, "score": c.score, "findings": c.findings, "recommendations": c.recommendations}
                for c in audit_result.ai_categories
            ],
            local_categories=[
                {"name": c.name, "score": c.score, "findings": c.findings, "recommendations": c.recommendations}
                for c in audit_result.local_categories
            ],
            quick_wins=audit_result.quick_wins,
            priority_fixes=audit_result.priority_fixes
        )
            
    except Exception as e:
        logger.exception("Audit request failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/audit/preview")
async def preview_audit(request: AuditRequest):
    """
    Run audit and return results without sending email.
    Useful for testing.
    """
    url = request.url
    if not url.startswith('http'):
        url = f"https://{url}"
    
    try:
        loop = asyncio.get_event_loop()
        analyzer = WebsiteAnalyzer(url)
        result = await loop.run_in_executor(executor, analyzer.run_full_audit)
        
        return {
            "success": True,
            "url": url,
            "business_name": result.business_name,
            "ai_visibility_score": result.ai_visibility_score,
            "local_seo_score": result.local_seo_score,
            "total_score": result.total_score,
            "ai_categories": [
                {
                    "name": c.name,
                    "score": c.score,
                    "findings": c.findings,
                    "recommendations": c.recommendations
                }
                for c in result.ai_categories
            ],
            "local_categories": [
                {
                    "name": c.name,
                    "score": c.score,
                    "findings": c.findings,
                    "recommendations": c.recommendations
                }
                for c in result.local_categories
            ],
            "quick_wins": result.quick_wins,
            "priority_fixes": result.priority_fixes
        }
        
    except Exception as e:
        logger.exception("Preview audit failed")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

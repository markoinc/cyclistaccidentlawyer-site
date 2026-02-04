#!/usr/bin/env python3
"""
Tool & Connection Monitor for Clawdbot
Checks all integrated services and returns a health report.
Usage:
    python3 tool_monitor.py           # Human-readable output
    python3 tool_monitor.py --json    # JSON output
    python3 tool_monitor.py --slack   # Slack mrkdwn formatted output
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import shutil
import ssl
import socket
import subprocess
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests

# Optional imports
try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

# ─── Configuration ───────────────────────────────────────────────────────────

STATE_FILE = Path("/home/ec2-user/clawd/data/monitor_state.json")
TOKEN_FILE = Path.home() / ".config" / "gcal-pro" / "token.json"

NOTION_API_KEY = "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"
GHL_API_KEY = "pit-9c041df9-b51b-4c7b-9329-241b528dc726"
GHL_LOCATION = "OsNgWuy8oZzLbp5BXbnD"
LEMLIST_API_KEY = "74625ab77cc446e66516d47ced121627"
NEON_CONN = "postgresql://neondb_owner:npg_hOuILz6BQn7Y@ep-summer-silence-ahgxcxho-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
NEON_API_KEY = "napi_07nt51snyfakkmvxk7yvikjs2gkvo4uvi408hrda91g35i5y8spkt1fv7gnqvz40"
NEON_PROJECT = "odd-math-10907968"

X_CONSUMER_KEY = "Zf1brMTJtTyj2sV2j3siRVv84"
X_CONSUMER_SECRET = "S4GQ6BzqonVVxa3NnaLPRibL5g7wPAMWFgRhs1MtcAhbLYhlni"
X_ACCESS_TOKEN = "1198729883867848706-BTyel5aWEfhYBZ5tQnQ6V88XX5CWgD"
X_ACCESS_SECRET = "NTLIHTbBnseszyqgWWCGJ2UA1Up4TizLfq6dfRLycQ5vi"

APOLLO_API_KEY = "t_j7hexbGUqksRuWZWi9hw"
DATAFORSEO_AUTH = "bWFya0BrdXJpb3NicmFuZC5jb206YjI5MmI0YTVlNjg2YmM3NQ=="

PROXY_HOST = "p.webshare.io"
PROXY_PORT = 80
PROXY_USER = "dtwmetwu-1"
PROXY_PASS = "ww846x37mmd9"

ANTHROPIC_CREDS_FILE = Path.home() / ".config" / "anthropic" / "credentials.json"

DOMAINS_TO_CHECK = []  # Add domains here if needed, e.g. ["kuriosbrand.com"]

ENV_LOCAL = Path("/home/ec2-user/clawd/.env.local")

REQUEST_TIMEOUT = 15  # seconds


def _load_anthropic_key():
    """Read Anthropic API key from credentials file at runtime."""
    try:
        with open(ANTHROPIC_CREDS_FILE) as f:
            data = json.load(f)
        return data.get("api_key", "")
    except Exception:
        return ""


def _load_openai_key():
    """Read OpenAI API key from .env.local at runtime."""
    try:
        with open(ENV_LOCAL) as f:
            for line in f:
                line = line.strip()
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return os.environ.get("OPENAI_API_KEY", "")

# ─── Result Structure ────────────────────────────────────────────────────────

class CheckResult:
    def __init__(self, service, status, message, severity="info", action=None, details=None):
        self.service = service
        self.status = status          # "healthy", "warning", "critical", "error"
        self.message = message
        self.severity = severity      # "info", "warning", "critical"
        self.action = action or ""
        self.details = details or {}

    def to_dict(self):
        d = {
            "service": self.service,
            "status": self.status,
            "message": self.message,
            "severity": self.severity,
        }
        if self.action:
            d["action"] = self.action
        if self.details:
            d["details"] = self.details
        return d


# ─── OAuth1 Helper (no external lib needed) ─────────────────────────────────

def _percent_encode(s):
    return urllib.parse.quote(str(s), safe="")

def _oauth1_sign(method, url, params, consumer_secret, token_secret):
    sorted_params = "&".join(f"{_percent_encode(k)}={_percent_encode(v)}"
                             for k, v in sorted(params.items()))
    base_string = f"{method.upper()}&{_percent_encode(url)}&{_percent_encode(sorted_params)}"
    signing_key = f"{_percent_encode(consumer_secret)}&{_percent_encode(token_secret)}"
    sig = hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1)
    return base64.b64encode(sig.digest()).decode()

def oauth1_request(method, url, consumer_key, consumer_secret, access_token, access_secret, params=None):
    import uuid
    oauth_params = {
        "oauth_consumer_key": consumer_key,
        "oauth_nonce": uuid.uuid4().hex,
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": access_token,
        "oauth_version": "1.0",
    }
    all_params = {**oauth_params}
    if params:
        all_params.update(params)
    sig = _oauth1_sign(method, url, all_params, consumer_secret, access_secret)
    oauth_params["oauth_signature"] = sig
    auth_header = "OAuth " + ", ".join(
        f'{_percent_encode(k)}="{_percent_encode(v)}"'
        for k, v in sorted(oauth_params.items())
    )
    resp = requests.request(method, url, headers={"Authorization": auth_header},
                            params=params, timeout=REQUEST_TIMEOUT)
    return resp


# ─── Individual Checks ───────────────────────────────────────────────────────

def check_google_oauth():
    """Check Google OAuth token expiry and refresh if needed."""
    service = "Google OAuth"
    try:
        if not TOKEN_FILE.exists():
            return CheckResult(service, "critical", "Token file not found",
                             "critical", f"Re-authenticate at {TOKEN_FILE}")

        with open(TOKEN_FILE) as f:
            token_data = json.load(f)

        expiry_str = token_data.get("expiry")
        refresh_token = token_data.get("refresh_token")

        if not expiry_str:
            return CheckResult(service, "warning", "No expiry field in token",
                             "warning", "Check token format")

        # Parse expiry
        expiry_str_clean = expiry_str.replace("Z", "+00:00")
        try:
            expiry = datetime.fromisoformat(expiry_str_clean)
        except ValueError:
            expiry = datetime.strptime(expiry_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        delta = expiry - now

        details = {
            "expiry": expiry.isoformat(),
            "hours_until_expiry": round(delta.total_seconds() / 3600, 2),
            "has_refresh_token": bool(refresh_token),
            "scopes": token_data.get("scopes", []),
        }

        if delta.total_seconds() < 0:
            # Token expired - try refresh
            if refresh_token:
                try:
                    resp = requests.post("https://oauth2.googleapis.com/token", data={
                        "client_id": token_data.get("client_id"),
                        "client_secret": token_data.get("client_secret"),
                        "refresh_token": refresh_token,
                        "grant_type": "refresh_token",
                    }, timeout=REQUEST_TIMEOUT)
                    if resp.status_code == 200:
                        new_data = resp.json()
                        token_data["token"] = new_data["access_token"]
                        new_expiry = datetime.now(timezone.utc) + timedelta(seconds=new_data.get("expires_in", 3600))
                        token_data["expiry"] = new_expiry.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                        with open(TOKEN_FILE, "w") as f:
                            json.dump(token_data, f, indent=4)
                        details["refreshed"] = True
                        details["new_expiry"] = token_data["expiry"]
                        return CheckResult(service, "healthy",
                                         "Token was expired but successfully refreshed",
                                         "info", details=details)
                    else:
                        details["refresh_error"] = resp.text[:200]
                        return CheckResult(service, "critical",
                                         f"Token expired and refresh failed (HTTP {resp.status_code})",
                                         "critical", "Re-authenticate manually", details)
                except Exception as e:
                    details["refresh_error"] = str(e)
                    return CheckResult(service, "critical",
                                     f"Token expired and refresh threw error: {e}",
                                     "critical", "Re-authenticate manually", details)
            else:
                return CheckResult(service, "critical", "Token expired, no refresh token",
                                 "critical", "Re-authenticate manually", details)

        elif delta < timedelta(hours=24):
            return CheckResult(service, "warning",
                             f"Token expiring in {delta.total_seconds()/3600:.1f}h",
                             "warning", "Token will auto-refresh on next use", details)
        else:
            return CheckResult(service, "healthy",
                             f"Token valid for {delta.total_seconds()/3600:.1f}h",
                             "info", details=details)

    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}",
                         "critical", "Investigate error")


def check_notion():
    """Ping Notion API."""
    service = "Notion API"
    try:
        resp = requests.get("https://api.notion.com/v1/users/me", headers={
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Notion-Version": "2022-06-28",
        }, timeout=REQUEST_TIMEOUT)

        details = {"status_code": resp.status_code, "response_time_ms": int(resp.elapsed.total_seconds() * 1000)}

        if resp.status_code == 200:
            data = resp.json()
            details["user_name"] = data.get("name", "unknown")
            details["user_type"] = data.get("type", "unknown")
            return CheckResult(service, "healthy", f"Connected as {data.get('name', 'unknown')}",
                             "info", details=details)
        elif resp.status_code == 401:
            return CheckResult(service, "critical", "Authentication failed (401)",
                             "critical", "Check/rotate API key", details)
        else:
            return CheckResult(service, "warning", f"Unexpected status {resp.status_code}",
                             "warning", details=details)
    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out",
                         "warning", "Check network connectivity")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_ghl():
    """Check Go High Level API."""
    service = "Go High Level"
    try:
        resp = requests.get(
            f"https://services.leadconnectorhq.com/locations/{GHL_LOCATION}",
            headers={
                "Authorization": f"Bearer {GHL_API_KEY}",
                "Version": "2021-07-28",
            },
            timeout=REQUEST_TIMEOUT
        )
        details = {"status_code": resp.status_code, "response_time_ms": int(resp.elapsed.total_seconds() * 1000)}

        if resp.status_code == 200:
            data = resp.json()
            loc = data.get("location", data)
            details["location_name"] = loc.get("name", "unknown")
            return CheckResult(service, "healthy",
                             f"Connected - Location: {loc.get('name', GHL_LOCATION)}",
                             "info", details=details)
        elif resp.status_code == 401:
            return CheckResult(service, "critical", "Authentication failed (401)",
                             "critical", "Check/rotate API key", details)
        else:
            return CheckResult(service, "warning", f"HTTP {resp.status_code}",
                             "warning", details=details)
    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out", "warning")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_lemlist():
    """Check Lemlist API."""
    service = "Lemlist API"
    try:
        resp = requests.get(
            "https://api.lemlist.com/api/team",
            auth=("", LEMLIST_API_KEY),
            timeout=REQUEST_TIMEOUT
        )
        details = {"status_code": resp.status_code, "response_time_ms": int(resp.elapsed.total_seconds() * 1000)}

        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, dict):
                details["team_name"] = data.get("name", "unknown")
            return CheckResult(service, "healthy", "Connected", "info", details=details)
        elif resp.status_code == 401:
            return CheckResult(service, "critical", "Authentication failed",
                             "critical", "Check API key", details)
        else:
            return CheckResult(service, "warning", f"HTTP {resp.status_code}",
                             "warning", details=details)
    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out", "warning")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_neon_postgres():
    """Check Neon Postgres connection and DB size."""
    service = "Neon Postgres"
    details = {}

    # Direct DB connection
    if HAS_PSYCOPG2:
        try:
            conn = psycopg2.connect(NEON_CONN, connect_timeout=10)
            cur = conn.cursor()

            # Check connection
            cur.execute("SELECT version()")
            version = cur.fetchone()[0]
            details["pg_version"] = version.split(",")[0] if version else "unknown"

            # Check DB size
            cur.execute("SELECT pg_database_size(current_database())")
            db_size_bytes = cur.fetchone()[0]
            details["db_size_mb"] = round(db_size_bytes / (1024 * 1024), 2)
            details["db_size_human"] = f"{details['db_size_mb']:.1f} MB"

            # Table count
            cur.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'")
            details["table_count"] = cur.fetchone()[0]

            cur.close()
            conn.close()
            details["direct_connection"] = "ok"

        except Exception as e:
            details["direct_connection"] = f"failed: {e}"
    else:
        details["direct_connection"] = "psycopg2 not installed"

    # Neon API check
    try:
        resp = requests.get(
            f"https://console.neon.tech/api/v2/projects/{NEON_PROJECT}",
            headers={"Authorization": f"Bearer {NEON_API_KEY}"},
            timeout=REQUEST_TIMEOUT
        )
        details["api_status_code"] = resp.status_code
        if resp.status_code == 200:
            proj = resp.json().get("project", {})
            details["project_name"] = proj.get("name", "unknown")
            details["region"] = proj.get("region_id", "unknown")
            details["created_at"] = proj.get("created_at", "unknown")
        else:
            details["api_error"] = resp.text[:200]
    except Exception as e:
        details["api_error"] = str(e)

    # Determine overall status
    if details.get("direct_connection") == "ok":
        return CheckResult(service, "healthy",
                         f"Connected - {details.get('db_size_human', 'unknown size')}, {details.get('table_count', '?')} tables",
                         "info", details=details)
    elif "api_status_code" in details and details["api_status_code"] == 200:
        return CheckResult(service, "warning",
                         "API reachable but direct connection failed",
                         "warning", "Check direct connection string", details)
    else:
        return CheckResult(service, "critical",
                         "Both direct connection and API failed",
                         "critical", "Check Neon dashboard", details)


def check_twitter():
    """Check X/Twitter API via OAuth1."""
    service = "X/Twitter API"
    try:
        url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
        resp = oauth1_request("GET", url,
                            X_CONSUMER_KEY, X_CONSUMER_SECRET,
                            X_ACCESS_TOKEN, X_ACCESS_SECRET,
                            params={"resources": "statuses,search"})

        details = {"status_code": resp.status_code, "response_time_ms": int(resp.elapsed.total_seconds() * 1000)}

        if resp.status_code == 200:
            data = resp.json()
            # Extract some rate limit info
            resources = data.get("resources", {})
            rate_info = {}
            for category, endpoints in resources.items():
                for endpoint, limits in endpoints.items():
                    remaining = limits.get("remaining", 0)
                    limit = limits.get("limit", 0)
                    if limit > 0 and remaining / limit < 0.1:
                        rate_info[endpoint] = f"{remaining}/{limit} remaining"
            details["low_rate_limits"] = rate_info if rate_info else "all good"
            if rate_info:
                return CheckResult(service, "warning",
                                 f"Connected but {len(rate_info)} endpoints near rate limit",
                                 "warning", "Reduce API calls", details)
            return CheckResult(service, "healthy", "Connected, rate limits healthy",
                             "info", details=details)
        elif resp.status_code == 401:
            return CheckResult(service, "critical", "Authentication failed (401)",
                             "critical", "Check OAuth credentials", details)
        elif resp.status_code == 429:
            return CheckResult(service, "warning", "Rate limited (429)",
                             "warning", "Wait before making more requests", details)
        else:
            details["response_body"] = resp.text[:200]
            return CheckResult(service, "warning", f"HTTP {resp.status_code}",
                             "warning", details=details)
    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out", "warning")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_apollo():
    """Check Apollo.io API credit usage."""
    service = "Apollo.io API"
    try:
        # Use the mixed_people/search endpoint with minimal query to verify auth
        # This is the most reliable endpoint for API key validation
        resp = requests.post(
            "https://api.apollo.io/v1/mixed_people/search",
            headers={
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
                "X-Api-Key": APOLLO_API_KEY,
            },
            json={"per_page": 1, "page": 1, "person_titles": ["CEO"]},
            timeout=REQUEST_TIMEOUT
        )
        details = {"status_code": resp.status_code, "response_time_ms": int(resp.elapsed.total_seconds() * 1000)}

        if resp.status_code == 200:
            data = resp.json()
            pagination = data.get("pagination", {})
            details["total_entries"] = pagination.get("total_entries", "unknown")
            # Check for rate limit headers
            remaining = resp.headers.get("x-rate-limit-remaining")
            if remaining is not None:
                details["rate_limit_remaining"] = int(remaining)
                hourly_limit = resp.headers.get("x-hourly-usage-limit")
                if hourly_limit:
                    details["hourly_limit"] = int(hourly_limit)
            return CheckResult(service, "healthy", "Connected and authenticated",
                             "info", details=details)
        elif resp.status_code == 401:
            return CheckResult(service, "critical", "Authentication failed (401)",
                             "critical", "Check/rotate API key", details)
        elif resp.status_code == 422:
            # 422 means auth worked but bad params - still "connected"
            return CheckResult(service, "healthy", "Connected (auth verified)",
                             "info", details=details)
        elif resp.status_code == 429:
            return CheckResult(service, "warning", "Rate limited",
                             "warning", "Reduce API call frequency", details)
        else:
            details["response_body"] = resp.text[:300]
            return CheckResult(service, "warning", f"HTTP {resp.status_code}",
                             "warning", details=details)
    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out", "warning")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_dataforseo():
    """Check DataForSEO balance."""
    service = "DataForSEO API"
    try:
        resp = requests.get(
            "https://api.dataforseo.com/v3/appendix/user_data",
            headers={"Authorization": f"Basic {DATAFORSEO_AUTH}"},
            timeout=REQUEST_TIMEOUT
        )
        details = {"status_code": resp.status_code, "response_time_ms": int(resp.elapsed.total_seconds() * 1000)}

        if resp.status_code == 200:
            data = resp.json()
            tasks = data.get("tasks", [])
            if tasks and len(tasks) > 0:
                result = tasks[0].get("result", [])
                if result and len(result) > 0:
                    user_data = result[0]
                    money = user_data.get("money", {})
                    balance = money.get("balance", 0)
                    total_spent = money.get("total", 0)
                    details["balance"] = balance
                    details["total_spent"] = total_spent
                    details["login"] = user_data.get("login", "unknown")

                    if balance <= 0:
                        return CheckResult(service, "critical",
                                         f"No balance remaining (${balance:.2f})",
                                         "critical", "Top up DataForSEO account", details)
                    elif balance < 5:
                        return CheckResult(service, "warning",
                                         f"Low balance: ${balance:.2f}",
                                         "warning", "Consider topping up", details)
                    return CheckResult(service, "healthy",
                                     f"Balance: ${balance:.2f}",
                                     "info", details=details)
            return CheckResult(service, "healthy", "Connected", "info", details=details)
        elif resp.status_code == 401:
            return CheckResult(service, "critical", "Authentication failed",
                             "critical", "Check credentials", details)
        else:
            return CheckResult(service, "warning", f"HTTP {resp.status_code}",
                             "warning", details=details)
    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out", "warning")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_webshare_proxy():
    """Test Webshare proxy connection."""
    service = "Webshare Proxies"
    try:
        proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
        proxies = {"http": proxy_url, "https": proxy_url}

        start = time.time()
        resp = requests.get("http://httpbin.org/ip", proxies=proxies, timeout=REQUEST_TIMEOUT)
        elapsed_ms = int((time.time() - start) * 1000)

        details = {
            "status_code": resp.status_code,
            "response_time_ms": elapsed_ms,
            "proxy": f"{PROXY_HOST}:{PROXY_PORT}",
        }

        if resp.status_code == 200:
            data = resp.json()
            details["proxy_ip"] = data.get("origin", "unknown")
            return CheckResult(service, "healthy",
                             f"Working - IP: {data.get('origin', '?')} ({elapsed_ms}ms)",
                             "info", details=details)
        else:
            return CheckResult(service, "warning", f"HTTP {resp.status_code}",
                             "warning", "Check proxy credentials", details)
    except requests.exceptions.ProxyError as e:
        return CheckResult(service, "critical", f"Proxy connection failed: {e}",
                         "critical", "Check proxy credentials or Webshare account")
    except requests.Timeout:
        return CheckResult(service, "warning", "Proxy request timed out",
                         "warning", "Proxy may be slow or blocked")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "warning")


def check_server_health():
    """Check server disk, memory, and processes."""
    service = "Server Health"
    details = {}
    issues = []

    # Disk space
    try:
        usage = shutil.disk_usage("/")
        pct_used = (usage.used / usage.total) * 100
        details["disk"] = {
            "total_gb": round(usage.total / (1024**3), 1),
            "used_gb": round(usage.used / (1024**3), 1),
            "free_gb": round(usage.free / (1024**3), 1),
            "percent_used": round(pct_used, 1),
        }
        if pct_used > 90:
            issues.append(("critical", f"Disk {pct_used:.0f}% full"))
        elif pct_used > 80:
            issues.append(("warning", f"Disk {pct_used:.0f}% full"))
    except Exception as e:
        details["disk_error"] = str(e)

    # Memory
    try:
        with open("/proc/meminfo") as f:
            meminfo = {}
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    meminfo[parts[0].rstrip(":")] = int(parts[1])

        total_kb = meminfo.get("MemTotal", 0)
        avail_kb = meminfo.get("MemAvailable", 0)
        used_kb = total_kb - avail_kb
        pct_used = (used_kb / total_kb * 100) if total_kb else 0

        details["memory"] = {
            "total_mb": round(total_kb / 1024, 0),
            "used_mb": round(used_kb / 1024, 0),
            "available_mb": round(avail_kb / 1024, 0),
            "percent_used": round(pct_used, 1),
        }
        if pct_used > 95:
            issues.append(("critical", f"Memory {pct_used:.0f}% used"))
        elif pct_used > 85:
            issues.append(("warning", f"Memory {pct_used:.0f}% used"))
    except Exception as e:
        details["memory_error"] = str(e)

    # Load average
    try:
        with open("/proc/loadavg") as f:
            load = f.read().strip().split()[:3]
            details["load_avg"] = {"1m": float(load[0]), "5m": float(load[1]), "15m": float(load[2])}
            # Get CPU count for context
            cpu_count = os.cpu_count() or 1
            details["cpu_count"] = cpu_count
            if float(load[0]) > cpu_count * 2:
                issues.append(("warning", f"High load: {load[0]} (CPUs: {cpu_count})"))
    except Exception as e:
        details["load_error"] = str(e)

    # Uptime
    try:
        with open("/proc/uptime") as f:
            uptime_seconds = float(f.read().split()[0])
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            details["uptime"] = f"{days}d {hours}h"
    except Exception:
        pass

    if not issues:
        msg = f"All OK - Disk: {details.get('disk', {}).get('percent_used', '?')}%, Mem: {details.get('memory', {}).get('percent_used', '?')}%"
        return CheckResult(service, "healthy", msg, "info", details=details)

    worst = max(issues, key=lambda x: {"critical": 2, "warning": 1}.get(x[0], 0))
    msg = "; ".join(f"[{sev}] {desc}" for sev, desc in issues)
    return CheckResult(service, worst[0], msg, worst[0],
                     "Check server resources" if worst[0] == "critical" else "Monitor usage",
                     details)


def check_anthropic_api():
    """Check Anthropic/Claude API - credits and rate limits."""
    service = "Anthropic API"
    api_key = _load_anthropic_key()
    if not api_key:
        return CheckResult(service, "critical",
                         f"Cannot read API key from {ANTHROPIC_CREDS_FILE}",
                         "critical", "Check credentials file exists and has api_key field")
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 5,
                "messages": [{"role": "user", "content": "hi"}],
            },
            timeout=REQUEST_TIMEOUT,
        )
        details = {
            "status_code": resp.status_code,
            "response_time_ms": int(resp.elapsed.total_seconds() * 1000),
        }

        # ── Parse rate-limit headers regardless of status ──
        rl_headers = {}
        for hdr in (
            "anthropic-ratelimit-requests-limit",
            "anthropic-ratelimit-requests-remaining",
            "anthropic-ratelimit-requests-reset",
            "anthropic-ratelimit-tokens-limit",
            "anthropic-ratelimit-tokens-remaining",
            "anthropic-ratelimit-tokens-reset",
            "anthropic-ratelimit-input-tokens-limit",
            "anthropic-ratelimit-input-tokens-remaining",
            "anthropic-ratelimit-output-tokens-limit",
            "anthropic-ratelimit-output-tokens-remaining",
            "retry-after",
        ):
            val = resp.headers.get(hdr)
            if val is not None:
                rl_headers[hdr] = val
        if rl_headers:
            details["rate_limits"] = rl_headers

        # ── Evaluate response ──
        body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
        error_msg = ""
        if isinstance(body, dict) and body.get("error"):
            error_msg = body["error"].get("message", "")
            details["error_type"] = body["error"].get("type", "")

        # Credit balance exhausted
        if "credit balance" in error_msg.lower() or "billing" in error_msg.lower():
            details["error_message"] = error_msg
            return CheckResult(service, "critical",
                             f"Credit balance too low — {error_msg}",
                             "critical",
                             "Top up Anthropic credits at console.anthropic.com",
                             details)

        # Auth failure
        if resp.status_code == 401:
            return CheckResult(service, "critical",
                             "Authentication failed (401)",
                             "critical", "Check/rotate API key", details)

        # Overloaded / server error
        if resp.status_code == 529:
            return CheckResult(service, "warning",
                             "API overloaded (529)",
                             "warning", "Retry later", details)

        # Rate-limited
        if resp.status_code == 429:
            return CheckResult(service, "warning",
                             "Rate limited (429)",
                             "warning", "Reduce request frequency", details)

        # Success path (200) — check rate-limit headroom
        if resp.status_code == 200:
            warnings = []
            try:
                req_limit = int(rl_headers.get("anthropic-ratelimit-requests-limit", 0))
                req_remaining = int(rl_headers.get("anthropic-ratelimit-requests-remaining", 0))
                if req_limit and req_remaining / req_limit < 0.20:
                    pct = round(req_remaining / req_limit * 100, 1)
                    warnings.append(f"requests {pct}% remaining ({req_remaining}/{req_limit})")
            except (ValueError, ZeroDivisionError):
                pass
            try:
                tok_limit = int(rl_headers.get("anthropic-ratelimit-tokens-limit", 0))
                tok_remaining = int(rl_headers.get("anthropic-ratelimit-tokens-remaining", 0))
                if tok_limit and tok_remaining / tok_limit < 0.20:
                    pct = round(tok_remaining / tok_limit * 100, 1)
                    warnings.append(f"tokens {pct}% remaining ({tok_remaining}/{tok_limit})")
            except (ValueError, ZeroDivisionError):
                pass

            if warnings:
                return CheckResult(service, "warning",
                                 f"Connected but rate limits low: {'; '.join(warnings)}",
                                 "warning", "Reduce API usage", details)

            return CheckResult(service, "healthy",
                             "Connected, credits OK, rate limits healthy",
                             "info", details=details)

        # Any other HTTP error with a known error message
        if error_msg:
            details["error_message"] = error_msg
            return CheckResult(service, "warning",
                             f"HTTP {resp.status_code}: {error_msg[:120]}",
                             "warning", details=details)

        return CheckResult(service, "warning",
                         f"Unexpected HTTP {resp.status_code}",
                         "warning", details=details)

    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out",
                         "warning", "API may be slow")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_clawdbot_gateway():
    """Dedicated check for the Clawdbot gateway process."""
    service = "Clawdbot Gateway"
    details = {}
    try:
        # Primary: look for 'clawdbot' in process list
        result = subprocess.run(
            ["pgrep", "-af", "clawdbot"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            procs = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
            details["processes"] = procs[:5]  # cap for readability
            details["process_count"] = len(procs)

            # Grab PID of the main gateway and check uptime
            try:
                pid = procs[0].split()[0]
                stat = Path(f"/proc/{pid}/stat").read_text().split()
                # Field 22 = starttime in clock ticks
                starttime_ticks = int(stat[21])
                clk_tck = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
                boot_time = None
                with open("/proc/stat") as f:
                    for line in f:
                        if line.startswith("btime"):
                            boot_time = int(line.split()[1])
                            break
                if boot_time:
                    start_epoch = boot_time + starttime_ticks / clk_tck
                    uptime_s = time.time() - start_epoch
                    days = int(uptime_s // 86400)
                    hours = int((uptime_s % 86400) // 3600)
                    mins = int((uptime_s % 3600) // 60)
                    details["gateway_uptime"] = f"{days}d {hours}h {mins}m"
            except Exception:
                pass

            return CheckResult(service, "healthy",
                             f"Running ({len(procs)} process{'es' if len(procs)!=1 else ''})",
                             "info", details=details)

        # Fallback: search for 'gateway' process
        result2 = subprocess.run(
            ["pgrep", "-af", "gateway"],
            capture_output=True, text=True, timeout=5,
        )
        if result2.returncode == 0:
            procs = [l.strip() for l in result2.stdout.strip().splitlines() if l.strip()]
            details["fallback_processes"] = procs[:5]
            return CheckResult(service, "healthy",
                             f"Running (via gateway match, {len(procs)} procs)",
                             "info", details=details)

        return CheckResult(service, "critical",
                         "Gateway process NOT running",
                         "critical",
                         "Run: clawdbot gateway start",
                         details)

    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_openai():
    """Check OpenAI API key validity and rate limits."""
    service = "OpenAI API"
    try:
        api_key = _load_openai_key()
        if not api_key:
            return CheckResult(service, "critical", "No API key found",
                             "critical", "Check OPENAI_API_KEY in .env.local")

        # Make a tiny request to check key + get rate limit headers
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "max_tokens": 5,
                "messages": [{"role": "user", "content": "hi"}],
            },
            timeout=REQUEST_TIMEOUT
        )

        details = {
            "status_code": resp.status_code,
            "response_time_ms": int(resp.elapsed.total_seconds() * 1000),
        }

        # Parse rate limit headers
        rl_headers = {}
        for h in ["limit-requests", "limit-tokens", "remaining-requests",
                   "remaining-tokens", "reset-requests", "reset-tokens"]:
            val = resp.headers.get(f"x-ratelimit-{h}")
            if val is not None:
                rl_headers[h] = val
        if rl_headers:
            details["rate_limits"] = rl_headers

        if resp.status_code == 200:
            warnings = []
            req_limit = rl_headers.get("limit-requests")
            req_remaining = rl_headers.get("remaining-requests")
            tok_limit = rl_headers.get("limit-tokens")
            tok_remaining = rl_headers.get("remaining-tokens")

            if req_limit and req_remaining:
                pct = int(req_remaining) / int(req_limit)
                details["requests_pct_remaining"] = round(pct * 100, 1)
                if pct < 0.2:
                    warnings.append(f"requests {req_remaining}/{req_limit}")
            if tok_limit and tok_remaining:
                pct = int(tok_remaining) / int(tok_limit)
                details["tokens_pct_remaining"] = round(pct * 100, 1)
                if pct < 0.2:
                    warnings.append(f"tokens {tok_remaining}/{tok_limit}")

            if warnings:
                return CheckResult(service, "warning",
                                 f"Connected but near limits: {', '.join(warnings)}",
                                 "warning", "Reduce API usage", details)
            return CheckResult(service, "healthy",
                             f"Connected — {req_remaining}/{req_limit} req, {tok_remaining}/{tok_limit} tokens remaining",
                             "info", details=details)

        elif resp.status_code == 401:
            return CheckResult(service, "critical", "Authentication failed (401)",
                             "critical", "Check/rotate API key", details)
        elif resp.status_code == 429:
            body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            err_msg = body.get("error", {}).get("message", "")
            if "quota" in err_msg.lower() or "billing" in err_msg.lower():
                return CheckResult(service, "critical",
                                 f"Quota/billing issue: {err_msg[:150]}",
                                 "critical", "Check billing at platform.openai.com", details)
            return CheckResult(service, "warning", "Rate limited (429)",
                             "warning", "Back off API calls", details)
        else:
            details["response_body"] = resp.text[:200]
            return CheckResult(service, "warning", f"HTTP {resp.status_code}",
                             "warning", details=details)

    except requests.Timeout:
        return CheckResult(service, "warning", "Request timed out", "warning")
    except Exception as e:
        return CheckResult(service, "error", f"Check failed: {e}", "critical")


def check_ssl_domains():
    """Check SSL certificate expiry for configured domains."""
    service = "SSL/Domains"
    if not DOMAINS_TO_CHECK:
        return CheckResult(service, "healthy", "No domains configured for monitoring",
                         "info", details={"domains": []})

    details = {}
    issues = []

    for domain in DOMAINS_TO_CHECK:
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(10)
                s.connect((domain, 443))
                cert = s.getpeercert()

            not_after = ssl.cert_time_to_seconds(cert["notAfter"])
            expiry = datetime.fromtimestamp(not_after, tz=timezone.utc)
            days_left = (expiry - datetime.now(timezone.utc)).days

            details[domain] = {
                "expiry": expiry.isoformat(),
                "days_left": days_left,
                "issuer": dict(x[0] for x in cert.get("issuer", [])).get("organizationName", "unknown"),
            }

            if days_left < 7:
                issues.append(("critical", f"{domain}: SSL expires in {days_left} days"))
            elif days_left < 30:
                issues.append(("warning", f"{domain}: SSL expires in {days_left} days"))

        except Exception as e:
            details[domain] = {"error": str(e)}
            issues.append(("warning", f"{domain}: SSL check failed - {e}"))

    if not issues:
        return CheckResult(service, "healthy", "All SSL certs OK", "info", details=details)

    worst = max(issues, key=lambda x: {"critical": 2, "warning": 1}.get(x[0], 0))
    msg = "; ".join(desc for _, desc in issues)
    return CheckResult(service, worst[0], msg, worst[0], "Renew certificates", details)


# ─── State Management ────────────────────────────────────────────────────────

def load_previous_state():
    """Load previous monitoring state."""
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def save_state(report):
    """Save current monitoring state."""
    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        state = {
            "last_run": report["timestamp"],
            "issues": {},
        }
        for item in report.get("alerts", []) + report.get("warnings", []):
            key = item["service"]
            state["issues"][key] = {
                "status": item["status"],
                "message": item["message"],
                "first_seen": item.get("first_seen", report["timestamp"]),
                "last_seen": report["timestamp"],
            }
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass

def annotate_with_state(report, prev_state):
    """Mark issues as new or recurring."""
    prev_issues = prev_state.get("issues", {})
    now = datetime.now(timezone.utc)

    for item in report.get("alerts", []) + report.get("warnings", []):
        key = item["service"]
        if key in prev_issues:
            first_seen = prev_issues[key].get("first_seen", report["timestamp"])
            item["first_seen"] = first_seen
            item["is_new"] = False
            # Check if it's been >24h since first seen (re-alert)
            try:
                fs = datetime.fromisoformat(first_seen.replace("Z", "+00:00"))
                hours_old = (now - fs).total_seconds() / 3600
                item["hours_old"] = round(hours_old, 1)
                item["re_alert"] = hours_old > 24
            except Exception:
                item["re_alert"] = False
        else:
            item["first_seen"] = report["timestamp"]
            item["is_new"] = True
            item["re_alert"] = False


# ─── Output Formatters ───────────────────────────────────────────────────────

def format_human(report):
    """Human-readable output."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  🔍 Tool & Connection Monitor Report")
    lines.append(f"  {report['timestamp']}")
    lines.append(f"{'='*60}")
    lines.append(f"\n  📊 Summary: {report['summary']}\n")

    if report["alerts"]:
        lines.append(f"  🚨 ALERTS ({len(report['alerts'])})")
        lines.append(f"  {'─'*40}")
        for a in report["alerts"]:
            new_tag = " 🆕" if a.get("is_new") else ""
            lines.append(f"  ❌ {a['service']}: {a['message']}{new_tag}")
            if a.get("action"):
                lines.append(f"     → {a['action']}")
        lines.append("")

    if report["warnings"]:
        lines.append(f"  ⚠️  WARNINGS ({len(report['warnings'])})")
        lines.append(f"  {'─'*40}")
        for w in report["warnings"]:
            new_tag = " 🆕" if w.get("is_new") else ""
            lines.append(f"  ⚠️  {w['service']}: {w['message']}{new_tag}")
            if w.get("action"):
                lines.append(f"     → {w['action']}")
        lines.append("")

    if report["healthy"]:
        lines.append(f"  ✅ HEALTHY ({len(report['healthy'])})")
        lines.append(f"  {'─'*40}")
        for h in report["healthy"]:
            lines.append(f"  ✅ {h['service']}: {h['message']}")
        lines.append("")

    lines.append(f"{'='*60}\n")
    return "\n".join(lines)


def format_slack(report):
    """Slack mrkdwn formatted output."""
    blocks = []
    blocks.append(f"*🔍 Tool & Connection Monitor*")
    blocks.append(f"_{report['timestamp']}_")
    blocks.append(f"*Summary:* {report['summary']}")
    blocks.append("")

    if report["alerts"]:
        blocks.append(f"*🚨 ALERTS ({len(report['alerts'])})*")
        for a in report["alerts"]:
            new_tag = " 🆕" if a.get("is_new") else ""
            blocks.append(f"• ❌ *{a['service']}*: {a['message']}{new_tag}")
            if a.get("action"):
                blocks.append(f"  _→ {a['action']}_")
        blocks.append("")

    if report["warnings"]:
        blocks.append(f"*⚠️ WARNINGS ({len(report['warnings'])})*")
        for w in report["warnings"]:
            new_tag = " 🆕" if w.get("is_new") else ""
            blocks.append(f"• ⚠️ *{w['service']}*: {w['message']}{new_tag}")
            if w.get("action"):
                blocks.append(f"  _→ {w['action']}_")
        blocks.append("")

    if report["healthy"]:
        blocks.append(f"*✅ HEALTHY ({len(report['healthy'])})*")
        for h in report["healthy"]:
            blocks.append(f"• ✅ {h['service']}")
        blocks.append("")

    return "\n".join(blocks)


# ─── Main ────────────────────────────────────────────────────────────────────

def run_all_checks():
    """Run all checks concurrently and build report."""
    checks = [
        check_google_oauth,
        check_notion,
        check_ghl,
        check_lemlist,
        check_neon_postgres,
        check_twitter,
        check_apollo,
        check_dataforseo,
        check_webshare_proxy,
        check_anthropic_api,
        check_openai,
        check_server_health,
        check_clawdbot_gateway,
        check_ssl_domains,
    ]

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_check = {executor.submit(fn): fn.__name__ for fn in checks}
        for future in as_completed(future_to_check):
            name = future_to_check[future]
            try:
                result = future.result(timeout=30)
                results.append(result)
            except Exception as e:
                results.append(CheckResult(
                    name.replace("check_", "").replace("_", " ").title(),
                    "error", f"Check crashed: {e}", "critical"
                ))

    # Build report
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    alerts = [r.to_dict() for r in results if r.status in ("critical", "error")]
    warnings = [r.to_dict() for r in results if r.status == "warning"]
    healthy = [r.to_dict() for r in results if r.status == "healthy"]

    summary_parts = []
    if alerts:
        summary_parts.append(f"{len(alerts)} alert{'s' if len(alerts)!=1 else ''}")
    if warnings:
        summary_parts.append(f"{len(warnings)} warning{'s' if len(warnings)!=1 else ''}")
    if healthy:
        summary_parts.append(f"{len(healthy)} healthy")
    summary = ", ".join(summary_parts) if summary_parts else "No checks completed"

    report = {
        "timestamp": now,
        "summary": summary,
        "total_checks": len(results),
        "alerts": alerts,
        "warnings": warnings,
        "healthy": healthy,
        "details": {r.service: r.to_dict() for r in results},
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="Tool & Connection Monitor")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--slack", action="store_true", help="Slack mrkdwn output")
    parser.add_argument("--no-state", action="store_true", help="Skip state tracking")
    args = parser.parse_args()

    # Load previous state
    prev_state = {} if args.no_state else load_previous_state()

    # Run checks
    report = run_all_checks()

    # Annotate with state info
    if not args.no_state:
        annotate_with_state(report, prev_state)
        save_state(report)

    # Output
    if args.json:
        print(json.dumps(report, indent=2))
    elif args.slack:
        print(format_slack(report))
    else:
        print(format_human(report))

    # Exit code: 2 for alerts, 1 for warnings, 0 for healthy
    if report["alerts"]:
        sys.exit(2)
    elif report["warnings"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

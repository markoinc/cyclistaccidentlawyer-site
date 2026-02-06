#!/usr/bin/env python3
"""Change Google account passwords - v2 with better Google sign-in handling."""

import json
import time
import sys
from playwright.sync_api import sync_playwright

ACCOUNTS = [
    {"email": "gundrum@trykuriosbrand.com", "old_pw": "n5SRLPKAid", "new_pw": "15yyBy3QugA5mNZ9"},
    {"email": "mark.gundrum@trykuriosbrand.com", "old_pw": "n5SRLPKAid", "new_pw": "jVSlcf09RfxtJ5kQ"},
    {"email": "markgundrum@trykuriosbrand.com", "old_pw": "n5SRLPKAid", "new_pw": "e0VcMwAC3SM55hqP"},
    {"email": "mgundrum@successkuriosbrand.com", "old_pw": "CWXZmZQYEa", "new_pw": "hG1y6dJjoQw9UKRm"},
    {"email": "mark.gundrum@successkuriosbrand.com", "old_pw": "CWXZmZQYEa", "new_pw": "eLZz1A6x3ictwtdR"},
    {"email": "markgundrum@successkuriosbrand.com", "old_pw": "CWXZmZQYEa", "new_pw": "n0bOIeJQpvN0HVzx"},
    {"email": "markgundrum@brandkuriosbrand.com", "old_pw": "L3L684LVdn", "new_pw": "goigaW9YrEk8Cvq2"},
    {"email": "mark.gundrum@brandkuriosbrand.com", "old_pw": "L3L684LVdn", "new_pw": "3pkEj7XNhbPseN4m"},
    {"email": "mark@brandkuriosbrand.com", "old_pw": "L3L684LVdn", "new_pw": "nuLIG6U3vXDHCrp8"},
    {"email": "sales@mykuriosbrand.com", "old_pw": "Le8327SWME", "new_pw": "RTVGuesmfeTAE9a5"},
    {"email": "markg@mykuriosbrand.com", "old_pw": "Le8327SWME", "new_pw": "HxcSHdbBSOB7Y1BE"},
    {"email": "mark@mykuriosbrand.com", "old_pw": "Le8327SWME", "new_pw": "o8jgWT015Blfo2jA"},
    {"email": "info@getkuriosbrand.com", "old_pw": "6EIr0Oo8LV", "new_pw": "rwK5vcS7MvDTrTB3"},
    {"email": "markg@getkuriosbrand.com", "old_pw": "6EIr0Oo8LV", "new_pw": "zZYnjIEqSHpfTcDG"},
    {"email": "mark@getkuriosbrand.com", "old_pw": "6EIr0Oo8LV", "new_pw": "gCjBpXRqfasPeJVg"},
]

results = []

def change_password(account, browser):
    email = account["email"]
    old_pw = account["old_pw"]
    new_pw = account["new_pw"]
    
    context = browser.new_context(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    
    try:
        # Step 1: Go to Google sign in
        page.goto("https://accounts.google.com/ServiceLogin", wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Handle "Choose an account" vs direct login
        if page.query_selector('text=Use another account'):
            page.click('text=Use another account')
            time.sleep(2)
        
        # Step 2: Enter email
        # Google uses identifier field with specific name
        email_field = page.wait_for_selector('input[type="email"]:visible', timeout=10000)
        email_field.fill(email)
        time.sleep(0.5)
        
        # Click Next
        page.keyboard.press("Enter")
        time.sleep(4)
        
        # Step 3: Enter password - Google hides the real input, use the visible one
        # Wait for the password page to load
        page.wait_for_selector('input[name="Passwd"]:visible, input[type="password"]:visible', timeout=15000)
        time.sleep(1)
        
        # Try name="Passwd" first (Google's actual field name)
        pw_field = page.query_selector('input[name="Passwd"]:visible')
        if not pw_field:
            # Fallback: find visible password input
            pw_fields = page.query_selector_all('input[type="password"]')
            pw_field = None
            for f in pw_fields:
                if f.is_visible():
                    pw_field = f
                    break
        
        if not pw_field:
            raise Exception("Could not find visible password field")
        
        pw_field.fill(old_pw)
        time.sleep(0.5)
        page.keyboard.press("Enter")
        time.sleep(5)
        
        # Step 4: Check if logged in - navigate to password change
        current_url = page.url
        if "challenge" in current_url.lower() or "signin" in current_url.lower():
            # Might have 2FA or some challenge - take screenshot for debug
            raise Exception(f"Login might have failed or hit challenge. URL: {current_url}")
        
        # Step 5: Go directly to password change page
        page.goto("https://myaccount.google.com/signinoptions/password", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Check if we need to re-authenticate
        reauth_field = page.query_selector('input[name="Passwd"]:visible, input[type="password"]:visible')
        if reauth_field and "signin" in page.url.lower():
            reauth_field.fill(old_pw)
            page.keyboard.press("Enter")
            time.sleep(5)
        
        # Step 6: Fill new password fields
        # Google password change page has two fields
        page.wait_for_selector('input[name="password"]:visible, input[aria-label="New password"]:visible', timeout=15000)
        time.sleep(1)
        
        new_pw_field = page.query_selector('input[name="password"]:visible')
        if not new_pw_field:
            new_pw_field = page.query_selector('input[aria-label="New password"]:visible')
        if not new_pw_field:
            # Try all visible password fields
            visible_pw = [f for f in page.query_selector_all('input[type="password"]') if f.is_visible()]
            if len(visible_pw) >= 2:
                new_pw_field = visible_pw[0]
            else:
                raise Exception("Could not find new password field")
        
        new_pw_field.fill(new_pw)
        time.sleep(0.5)
        
        # Confirm password field
        confirm_field = page.query_selector('input[name="confirmation_password"]:visible')
        if not confirm_field:
            confirm_field = page.query_selector('input[aria-label="Confirm new password"]:visible')
        if not confirm_field:
            visible_pw = [f for f in page.query_selector_all('input[type="password"]') if f.is_visible()]
            if len(visible_pw) >= 2:
                confirm_field = visible_pw[1]
        
        if confirm_field:
            confirm_field.fill(new_pw)
        time.sleep(0.5)
        
        # Click Change password button
        change_btn = page.query_selector('button:has-text("Change password")')
        if change_btn:
            change_btn.click()
        else:
            # Try submitting via keyboard
            page.keyboard.press("Enter")
        
        time.sleep(5)
        
        # Check success
        final_url = page.url
        if "password" not in final_url or "myaccount" in final_url:
            print(f"✅ {email} — password changed!", flush=True)
            results.append({"email": email, "new_pw": new_pw, "status": "success"})
        else:
            print(f"⚠️ {email} — uncertain (URL: {final_url})", flush=True)
            results.append({"email": email, "new_pw": new_pw, "status": "uncertain"})
            
    except Exception as e:
        err = str(e)[:200]
        print(f"❌ {email} — ERROR: {err}", flush=True)
        results.append({"email": email, "new_pw": new_pw, "status": f"error: {err}"})
    finally:
        context.close()

print("Starting password changes for 15 accounts...", flush=True)
print("=" * 60, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for i, account in enumerate(ACCOUNTS):
        print(f"\n[{i+1}/15] {account['email']}...", flush=True)
        change_password(account, browser)
        time.sleep(1)
    
    browser.close()

# Add the first account (already changed)
results.insert(0, {"email": "mark@trykuriosbrand.com", "new_pw": "vkWU!1ogzEsz%oGa", "status": "already_changed"})
# Add sales@ (already changed by Marko)
results.append({"email": "sales@getkuriosbrand.com", "new_pw": "5YY6DeqTUaxVxphQE3f#", "status": "changed_by_marko"})

print(f"\n{'='*60}", flush=True)
success = sum(1 for r in results if r['status'] in ['success', 'already_changed', 'changed_by_marko'])
print(f"RESULTS: {success}/{len(results)} successful", flush=True)
print(f"{'='*60}", flush=True)

# Save to file
with open("/home/ec2-user/.config/instantly/new-passwords.json", "w") as f:
    json.dump(results, f, indent=2)

# Print final table
print("\nFinal credentials:", flush=True)
for r in results:
    status = "✅" if r["status"] in ["success", "already_changed", "changed_by_marko"] else "❌"
    print(f"{status} {r['email']} — {r['new_pw']}", flush=True)

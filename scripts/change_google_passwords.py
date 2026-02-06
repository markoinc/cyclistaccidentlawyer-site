#!/usr/bin/env python3
"""Change Google account passwords for all warmed email accounts."""

import json
import time
import sys
from playwright.sync_api import sync_playwright

ACCOUNTS = [
    {"email": "mark@trykuriosbrand.com", "old_pw": "n5SRLPKAid", "new_pw": "vkWU!1ogzEsz%oGa"},
    {"email": "gundrum@trykuriosbrand.com", "old_pw": "n5SRLPKAid", "new_pw": "15yyBy3QugA5%mNZ"},
    {"email": "mark.gundrum@trykuriosbrand.com", "old_pw": "n5SRLPKAid", "new_pw": "jVS$lcf09%RfxtJ5"},
    {"email": "markgundrum@trykuriosbrand.com", "old_pw": "n5SRLPKAid", "new_pw": "e0VcM!wAC3SM55hq"},
    {"email": "mgundrum@successkuriosbrand.com", "old_pw": "CWXZmZQYEa", "new_pw": "hG1$y6dJjoQw9UKR"},
    {"email": "mark.gundrum@successkuriosbrand.com", "old_pw": "CWXZmZQYEa", "new_pw": "eLZz1A6x3ictwtdR"},
    {"email": "markgundrum@successkuriosbrand.com", "old_pw": "CWXZmZQYEa", "new_pw": "@n0bO$IeJQpvN0HV"},
    {"email": "markgundrum@brandkuriosbrand.com", "old_pw": "L3L684LVdn", "new_pw": "goigaW9YrEk8!Cvq"},
    {"email": "mark.gundrum@brandkuriosbrand.com", "old_pw": "L3L684LVdn", "new_pw": "3$%pkEj7XNhbPseN"},
    {"email": "mark@brandkuriosbrand.com", "old_pw": "L3L684LVdn", "new_pw": "nu@LIG6U3vXDHCrp"},
    {"email": "sales@mykuriosbrand.com", "old_pw": "Le8327SWME", "new_pw": "RTVGuesmfeTAE9a%"},
    {"email": "markg@mykuriosbrand.com", "old_pw": "Le8327SWME", "new_pw": "HxcSHdbBSOB7Y1BE"},
    {"email": "mark@mykuriosbrand.com", "old_pw": "Le8327SWME", "new_pw": "o8jgWT015Blfo2jA"},
    {"email": "info@getkuriosbrand.com", "old_pw": "6EIr0Oo8LV", "new_pw": "rwK5vc#S7MvDTrTB"},
    {"email": "markg@getkuriosbrand.com", "old_pw": "6EIr0Oo8LV", "new_pw": "zZYnjIEqSHpfTcDG"},
    {"email": "mark@getkuriosbrand.com", "old_pw": "6EIr0Oo8LV", "new_pw": "gCjBpXRqfasPeJVg"},
]

# Note: mark@trykuriosbrand.com was already changed via browser, but we'll use new_pw as old_pw for it
ACCOUNTS[0]["old_pw"] = "vkWU!1ogzEsz%oGa"  # Already changed

results = []

def change_password(account, browser):
    email = account["email"]
    old_pw = account["old_pw"]
    new_pw = account["new_pw"]
    
    context = browser.new_context()
    page = context.new_page()
    
    try:
        # Go to Google sign in
        page.goto("https://accounts.google.com/signin", wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Check for "Use another account" button
        use_another = page.query_selector('text=Use another account')
        if use_another:
            use_another.click()
            time.sleep(2)
        
        # Enter email
        email_input = page.wait_for_selector('input[type="email"]', timeout=10000)
        email_input.fill(email)
        page.click('button:has-text("Next")')
        time.sleep(3)
        
        # Enter password
        pw_input = page.wait_for_selector('input[type="password"]', timeout=10000)
        pw_input.fill(old_pw)
        page.click('button:has-text("Next")')
        time.sleep(5)
        
        # Check if we're logged in (look for account page or password change link)
        # Navigate directly to password change
        page.goto("https://myaccount.google.com/signinoptions/password", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        
        # Check if we need to re-authenticate
        reauth_pw = page.query_selector('input[type="password"]')
        if reauth_pw and 'signinoptions/password' not in page.url:
            # Re-auth needed
            reauth_pw.fill(old_pw)
            next_btn = page.query_selector('button:has-text("Next")')
            if next_btn:
                next_btn.click()
                time.sleep(3)
        
        # Now on the password change page
        # Find "New password" and "Confirm new password" fields
        new_pw_input = page.wait_for_selector('input[name="password"]', timeout=10000)
        if not new_pw_input:
            # Try alternate selectors
            inputs = page.query_selector_all('input[type="password"]')
            if len(inputs) >= 2:
                new_pw_input = inputs[0]
                confirm_input = inputs[1]
            else:
                raise Exception("Could not find password fields")
        
        new_pw_input.fill(new_pw)
        
        # Find confirm field
        confirm_input = page.query_selector('input[name="confirmation_password"]')
        if not confirm_input:
            inputs = page.query_selector_all('input[type="password"]')
            confirm_input = inputs[-1] if len(inputs) > 1 else None
        
        if confirm_input:
            confirm_input.fill(new_pw)
        
        # Click "Change password"
        change_btn = page.query_selector('button:has-text("Change password")')
        if change_btn:
            change_btn.click()
            time.sleep(5)
        
        # Check if we're redirected back (success)
        if "signinoptions/password" not in page.url or "myaccount.google.com" in page.url:
            print(f"✅ {email} — password changed successfully")
            results.append({"email": email, "new_pw": new_pw, "status": "success"})
        else:
            print(f"⚠️ {email} — may not have changed (still on password page)")
            results.append({"email": email, "new_pw": new_pw, "status": "uncertain"})
            
    except Exception as e:
        print(f"❌ {email} — ERROR: {str(e)}")
        results.append({"email": email, "new_pw": new_pw, "status": f"error: {str(e)}"})
    finally:
        context.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for i, account in enumerate(ACCOUNTS):
        if i == 0:
            # Skip first one, already changed via browser
            print(f"⏭️ {account['email']} — already changed, skipping")
            results.append({"email": account["email"], "new_pw": account["new_pw"], "status": "already_changed"})
            continue
        
        print(f"\n[{i+1}/16] Processing {account['email']}...")
        change_password(account, browser)
        time.sleep(2)  # Brief pause between accounts
    
    browser.close()

# Save results
print(f"\n{'='*60}")
print(f"RESULTS: {sum(1 for r in results if r['status'] in ['success','already_changed'])}/{len(results)} successful")
print(f"{'='*60}")

# Save to file
with open("/home/ec2-user/.config/instantly/new-passwords.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nPasswords saved to ~/.config/instantly/new-passwords.json")

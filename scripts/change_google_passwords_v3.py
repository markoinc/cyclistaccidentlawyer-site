#!/usr/bin/env python3
"""Change Google account passwords - v3 with proper wait handling."""

import json
import time
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
        # Go to Google sign in
        page.goto("https://accounts.google.com/ServiceLogin", timeout=30000)
        time.sleep(3)
        
        # Handle "Choose an account" 
        use_another = page.query_selector('text=Use another account')
        if use_another:
            use_another.click()
            time.sleep(2)
        
        # Enter email
        email_field = page.wait_for_selector('input[type="email"]:visible', timeout=10000)
        email_field.fill(email)
        page.keyboard.press("Enter")
        
        # Wait for password page - wait for Passwd field specifically
        page.wait_for_selector('input[name="Passwd"]', timeout=15000)
        time.sleep(2)
        
        # Enter password using JavaScript to bypass visibility issues
        page.evaluate('''(pw) => {
            const input = document.querySelector('input[name="Passwd"]');
            if (input) {
                input.value = pw;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }''', old_pw)
        time.sleep(0.5)
        
        # Also try clicking and typing as fallback
        try:
            passwd_field = page.query_selector('input[name="Passwd"]')
            passwd_field.focus()
            page.keyboard.press("Control+a")
            page.keyboard.type(old_pw, delay=50)
        except:
            pass
        
        time.sleep(0.5)
        page.keyboard.press("Enter")
        
        # Wait for login to complete - wait for URL to NOT contain 'signin'
        # or just wait long enough
        time.sleep(8)
        
        # Now go to password change page
        page.goto("https://myaccount.google.com/signinoptions/password", timeout=30000)
        time.sleep(5)
        
        # Check if we need to re-auth
        if "signin" in page.url.lower() or "challenge" in page.url.lower():
            # Re-authenticate
            passwd = page.query_selector('input[name="Passwd"]')
            if passwd:
                page.evaluate('''(pw) => {
                    const input = document.querySelector('input[name="Passwd"]');
                    if (input) { input.value = pw; input.dispatchEvent(new Event('input', { bubbles: true })); }
                }''', old_pw)
                try:
                    passwd.focus()
                    page.keyboard.press("Control+a")
                    page.keyboard.type(old_pw, delay=50)
                except:
                    pass
                page.keyboard.press("Enter")
                time.sleep(8)
                
                # Try navigating again
                if "signinoptions/password" not in page.url:
                    page.goto("https://myaccount.google.com/signinoptions/password", timeout=30000)
                    time.sleep(5)
        
        # Now fill in new password
        # Find all password inputs
        pw_inputs = page.query_selector_all('input[type="password"]')
        visible_inputs = [inp for inp in pw_inputs if inp.is_visible()]
        
        if len(visible_inputs) < 2:
            # Try with name selectors
            new_field = page.query_selector('input[name="password"]')
            confirm_field = page.query_selector('input[name="confirmation_password"]')
            if new_field and confirm_field:
                visible_inputs = [new_field, confirm_field]
            else:
                raise Exception(f"Only found {len(visible_inputs)} visible pw fields. URL: {page.url}")
        
        # Fill new password
        visible_inputs[0].click()
        visible_inputs[0].fill(new_pw)
        time.sleep(0.3)
        
        # Fill confirm
        visible_inputs[1].click()
        visible_inputs[1].fill(new_pw)
        time.sleep(0.3)
        
        # Click Change password
        change_btn = page.query_selector('button:has-text("Change password")')
        if change_btn:
            change_btn.click()
        else:
            page.keyboard.press("Enter")
        
        time.sleep(6)
        
        print(f"✅ {email} — password changed! (URL: {page.url[:80]})", flush=True)
        results.append({"email": email, "new_pw": new_pw, "status": "success"})
            
    except Exception as e:
        err = str(e)[:300]
        print(f"❌ {email} — ERROR: {err}", flush=True)
        # Take screenshot for debug
        try:
            page.screenshot(path=f"/tmp/pw_error_{email.split('@')[0]}.png")
        except:
            pass
        results.append({"email": email, "new_pw": new_pw, "status": f"error: {err}"})
    finally:
        context.close()

print("Starting password changes for 15 accounts...", flush=True)
print("=" * 60, flush=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    
    for i, account in enumerate(ACCOUNTS):
        print(f"\n[{i+1}/15] {account['email']}...", flush=True)
        change_password(account, browser)
        time.sleep(1)
    
    browser.close()

# Add already-changed accounts
all_results = [
    {"email": "mark@trykuriosbrand.com", "new_pw": "vkWU!1ogzEsz%oGa", "status": "already_changed"},
] + results + [
    {"email": "sales@getkuriosbrand.com", "new_pw": "5YY6DeqTUaxVxphQE3f#", "status": "changed_by_marko"},
]

print(f"\n{'='*60}", flush=True)
success = sum(1 for r in all_results if 'error' not in r['status'])
print(f"RESULTS: {success}/{len(all_results)} successful", flush=True)
print(f"{'='*60}", flush=True)

# Save to file
with open("/home/ec2-user/.config/instantly/new-passwords.json", "w") as f:
    json.dump(all_results, f, indent=2)

# Print final table
print("\nFinal credentials:", flush=True)
for r in all_results:
    status = "✅" if 'error' not in r["status"] else "❌"
    print(f"{status} {r['email']} — {r['new_pw']}", flush=True)

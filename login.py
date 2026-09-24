"""
One-time interactive login. Opens a real browser window pointed at Zomato.
Log in yourself (phone number + OTP) like you normally would. Once logged in,
press Enter in this terminal and the session cookies get saved to cookies.json
for the scraper to reuse. Cookies expire eventually -- just rerun this when
fetch_orders.py starts getting empty results.
"""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

COOKIE_FILE = Path("cookies.json")
REQUIRED_COOKIES = {"cid", "PHPSESSID", "zat"}


def main() -> bool:
    """Runs the interactive login flow. Returns True if it looks like login succeeded."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        page.goto("https://www.zomato.com/", wait_until="domcontentloaded", timeout=60000)

        print("\nA browser window has opened.")
        print("If a location/city popup or banner is covering the page, close it first.")
        print("Then look for a small profile/person icon in the top-right corner and")
        print("click it to log in with your phone number and OTP.")
        input("Once you're logged in and can see your account, press Enter here...\n")

        cookies = context.cookies()
        found = {c["name"] for c in cookies}
        missing = REQUIRED_COOKIES - found
        if missing:
            print(f"Warning: didn't find cookies {missing}. Login may not have completed.")
            print("Make sure you're fully logged in, then try again.")

        COOKIE_FILE.write_text(json.dumps(cookies, indent=2))
        print(f"Saved {len(cookies)} cookies to {COOKIE_FILE.resolve()}")

        browser.close()
        return not missing


if __name__ == "__main__":
    main()

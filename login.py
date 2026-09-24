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


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.zomato.com/", wait_until="domcontentloaded", timeout=60000)

        print("\nA browser window has opened.")
        print("Log in to Zomato with your phone number and OTP as usual.")
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


if __name__ == "__main__":
    main()

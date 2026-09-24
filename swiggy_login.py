"""
One-time interactive login for Swiggy.

Swiggy's bot-protection blocks Playwright when it drives the navigation
and login itself (a 403 on the homepage), regardless of which Chrome
build runs -- the automation signal itself is what gets flagged. So this
script never automates the actual browsing: it launches a plain, separate
Chrome window that you use normally by hand, and only attaches afterward
(via the DevTools protocol) to read out the session cookies once you've
logged in yourself.

Cookies expire eventually -- just rerun this when swiggy_fetch_orders.py
starts getting empty results.
"""

import json
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

COOKIE_FILE = Path("swiggy_cookies.json")
REQUIRED_COOKIES = {"__SW"}
DEBUG_PORT = 9222
PROFILE_DIR = Path.home() / ".swiggy-analytics-chrome-profile"


def launch_chrome():
    subprocess.Popen(
        [
            "open",
            "-na",
            "Google Chrome",
            "--args",
            f"--remote-debugging-port={DEBUG_PORT}",
            f"--user-data-dir={PROFILE_DIR}",
            "https://www.swiggy.com/",
        ]
    )


def main():
    print("Opening a plain Chrome window to swiggy.com (a separate profile,")
    print("not connected to your usual Chrome tabs/history).")
    launch_chrome()
    time.sleep(3)

    print("\nLog in yourself with your mobile number and OTP, as normal --")
    print("this window is not automated, so click and type as you always would.")
    input("Once you're logged in and can see your account, press Enter here...\n")

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://localhost:{DEBUG_PORT}")
        context = browser.contexts[0]
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

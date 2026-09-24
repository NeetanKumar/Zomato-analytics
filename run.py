"""
One-command entry point: logs in if needed, fetches your orders, and
prints the analytics. This is the easiest way to use the project --
`python3 run.py` and follow the prompts.
"""

import sys
from pathlib import Path

import analyze
import fetch_orders
import login

COOKIE_FILE = Path("cookies.json")


def main():
    if not COOKIE_FILE.exists():
        print("No saved Zomato session found -- let's log in first.\n")
        if not login.main():
            sys.exit("Login didn't complete successfully. Please try again.")

    print("\nFetching your order history...\n")
    if not fetch_orders.main():
        print("\nThat didn't return any orders -- your session may have expired.")
        print("Let's log in again.\n")
        if not login.main():
            sys.exit("Login didn't complete successfully. Please try again.")
        print("\nFetching your order history...\n")
        if not fetch_orders.main():
            sys.exit("Still couldn't fetch orders. Please check your account and try again.")

    print()
    analyze.main()


if __name__ == "__main__":
    main()

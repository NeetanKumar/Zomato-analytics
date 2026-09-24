# Zomato Analytics

Pulls your personal Zomato order history and summarizes it: total spend,
order count, top restaurants, monthly trends, and more.

Uses Zomato's internal (undocumented) order history endpoint, authenticated
with cookies from a real browser session you log into yourself. There's no
official API for this, so treat it as a personal tool for your own account —
not something to run at scale or share your session with.

## Requirements

- Python 3.9+
- A Zomato account with order history

## Quickstart

```bash
git clone https://github.com/NeetanKumar/Zomato-analytics.git
cd Zomato-analytics
./setup.sh
source venv/bin/activate
python3 run.py
```

`setup.sh` creates the virtual environment, installs everything, and sets
up the browser Playwright needs. `run.py` then does the rest for you in one
go: logs you in if there's no saved session (or if it's expired), fetches
your order history, and prints the analytics — no need to run each step by
hand.

## Manual setup / usage

If you'd rather run each step yourself (e.g. to just refresh `orders.json`
without re-printing the summary), you can call the scripts directly.

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

### 1. Log in

```bash
python3 login.py
```

A browser window opens to zomato.com. Log in yourself with your phone number
and OTP, as normal. Once you're logged in and can see your account, go back
to the terminal and press Enter. Your session cookies are saved to
`cookies.json`.

### 2. Fetch your orders

```bash
python3 fetch_orders.py
```

Uses the saved session to pull your full order history, page by page, into
`orders.json`.

If this returns no orders, your session has likely expired — rerun
`login.py` and try again.

### 3. Get the analytics

```bash
python3 analyze.py
```

Prints a summary to the terminal:

- Total orders, total spend, average order value, date range covered
- Top 10 restaurants by number of orders
- Top 10 restaurants by total spend
- Spend by month
- Orders by establishment type (restaurant, cafe, etc.)

It also writes `summary.csv`, a full per-restaurant breakdown (order count,
total spent, average order value) for further digging in a spreadsheet.

## Notes

- `cookies.json`, `orders.json`, and `summary.csv` are gitignored — they're
  your personal data, not project source.
- Cookies expire eventually. If `fetch_orders.py` stops returning data,
  rerun `login.py` to refresh the session.
- This relies on an internal endpoint that isn't a public API, so it may
  break if Zomato changes it.

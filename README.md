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

## Setup

```bash
git clone https://github.com/NeetanKumar/Zomato-analytics.git
cd Zomato-analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Usage

Run these three scripts in order.

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

# Food Delivery Analytics

Pulls your personal order history from Zomato and/or Swiggy and summarizes
it: total spend, order count, top restaurants, monthly trends, and more.

Uses each platform's internal (undocumented) order history endpoint,
authenticated with cookies from a real browser session you log into
yourself. There's no official API for this, so treat it as a personal tool
for your own account — not something to run at scale or share your session
with.

## Requirements

- Python 3.9+
- A Zomato and/or Swiggy account with order history

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

Each platform has its own set of three scripts, run in order. You can use
either or both independently.

### Zomato

#### 1. Log in

```bash
python3 login.py
```

A browser window opens to zomato.com. Log in yourself with your phone number
and OTP, as normal. Once you're logged in and can see your account, go back
to the terminal and press Enter. Your session cookies are saved to
`cookies.json`.

#### 2. Fetch your orders

```bash
python3 fetch_orders.py
```

Uses the saved session to pull your full order history, page by page, into
`orders.json`.

If this returns no orders, your session has likely expired — rerun
`login.py` and try again.

#### 3. Get the analytics

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

### Swiggy

#### 1. Log in

```bash
python3 swiggy_login.py
```

A browser window opens to swiggy.com. Log in yourself with your mobile
number and OTP, as normal. Once you're logged in, go back to the terminal
and press Enter. Your session cookies are saved to `swiggy_cookies.json`.

#### 2. Fetch your orders

```bash
python3 swiggy_fetch_orders.py
```

Uses the saved session to pull your full order history into
`swiggy_orders.json`. Swiggy's endpoint is cursor-paginated (each request
needs the last order ID from the previous one), so this can take a little
longer for accounts with a lot of orders.

If this returns no orders, your session has likely expired — rerun
`swiggy_login.py` and try again.

#### 3. Get the analytics

```bash
python3 swiggy_analyze.py
```

Prints the same kind of summary as Zomato's (delivered orders only), plus
a top-10 most-ordered-items breakdown since Swiggy's order data includes
line items. Also writes `swiggy_summary.csv`.

## Notes

- `cookies.json`/`swiggy_cookies.json`, `orders.json`/`swiggy_orders.json`,
  and the generated CSVs are gitignored — they're your personal data, not
  project source.
- Cookies expire eventually. If a fetch script stops returning data, rerun
  the matching login script to refresh the session.
- Both rely on internal endpoints that aren't public APIs, so they may
  break if either platform changes its frontend.

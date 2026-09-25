# Zomato Analytics

Pulls your Zomato order history and summarizes it: spend, top restaurants,
monthly trends. Uses Zomato's internal order-history endpoint via cookies
from a real browser login — personal use only, not a public API.

## Usage

1. `./setup.sh` — installs everything and runs the app
2. Log in with your phone/OTP when the browser opens, then press Enter
3. Open `order_summary.md` — that's your analytics report (spend, top
   restaurants, monthly trends). `summary.csv` has the same data per
   restaurant, for a spreadsheet.

Already set up? Just run `source venv/bin/activate && python3 run.py`.

Need to run a step on its own instead? `login.py` → `fetch_orders.py` →
`analyze.py`, in that order.

Prefer a browser popup over the terminal? See [`extension/`](extension) —
a Chrome extension version that shows the same analytics in a popup UI
using your browser's own logged-in Zomato session (no scripts to run).

## Notes

- `cookies.json`, `orders.json`, `summary.csv`, `order_summary.md` are
  gitignored — personal data, not project source.
- If fetching returns nothing, your session expired — rerun `login.py`.
- Relies on an undocumented endpoint, so it may break if Zomato changes it.

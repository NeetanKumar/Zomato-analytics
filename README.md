# Zomato Analytics

Pulls your Zomato order history and summarizes it: spend, top restaurants,
monthly trends. Uses Zomato's internal order-history endpoint via cookies
from a real browser login — personal use only, not a public API.

## Usage

1. `./setup.sh` — installs everything and runs the app
2. Log in with your phone/OTP when the browser opens, then press Enter
3. Check `order_summary.md` and `summary.csv` for the results

Already set up? Just run `source venv/bin/activate && python3 run.py`.

Need to run a step on its own instead? `login.py` → `fetch_orders.py` →
`analyze.py`, in that order.

## Notes

- `cookies.json`, `orders.json`, `summary.csv`, `order_summary.md` are
  gitignored — personal data, not project source.
- If fetching returns nothing, your session expired — rerun `login.py`.
- Relies on an undocumented endpoint, so it may break if Zomato changes it.

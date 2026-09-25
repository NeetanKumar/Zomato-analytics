# Zomato Analytics

See your Zomato order history at a glance: total spend, favorite
restaurants, monthly trends. Works by reading your own order history after
you log in — no official Zomato API for this exists, so this is a personal
tool for your own account, not something to share your login with.

There are two ways to use it — pick one.

## Option 1: Browser extension (easiest)

Shows your analytics as a page in your browser, with a print/PDF button.

1. Go to `chrome://extensions`, turn on **Developer mode**, click **Load
   unpacked**, and select the [`extension/`](extension) folder
2. Make sure you're logged into zomato.com in that browser
3. Click the extension icon, then **Analyze my orders**

## Option 2: Run it from the terminal

1. `./setup.sh`
2. Log in with your phone/OTP when the browser opens, then press Enter
3. Open `order_summary.md` for the report (`summary.csv` has the same
   numbers per restaurant, for a spreadsheet)

Already set up? Just run `source venv/bin/activate && python3 run.py`.

## Notes

- Both options only work with your own account and your own login — no
  data is sent anywhere else.
- This reads Zomato's internal order-history data, not an official API, so
  it may stop working if Zomato changes their site.
- If it stops returning orders, your login session has likely expired —
  just log in again.

"""
Pulls your full Swiggy order history using the session saved by
swiggy_login.py, and writes it to swiggy_orders.json. Run swiggy_login.py
first.

Swiggy's history endpoint is cursor-paginated: the first call returns a
batch of orders plus a total count, and each following call needs the
last order_id from the previous batch as an `order_id` offset param.
"""

import json
import time
from pathlib import Path

import requests

COOKIE_FILE = Path("swiggy_cookies.json")
ORDERS_FILE = Path("swiggy_orders.json")
ORDERS_ENDPOINT = "https://www.swiggy.com/dapi/order/all"

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://www.swiggy.com/",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ),
}


def load_cookie_header() -> str:
    if not COOKIE_FILE.exists():
        raise SystemExit("swiggy_cookies.json not found. Run swiggy_login.py first.")
    cookies = json.loads(COOKIE_FILE.read_text())
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


def normalize_order(order: dict) -> dict:
    items = order.get("order_items") or []
    return {
        "order_id": order.get("order_id"),
        "order_time": order.get("order_time"),
        "order_total": float(order.get("order_total") or 0),
        "order_status": order.get("order_status"),
        "restaurant_name": order.get("restaurant_name"),
        "restaurant_id": order.get("restaurant_id"),
        "items": [item.get("name") for item in items if item.get("name")],
    }


def main():
    cookie_header = load_cookie_header()
    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers["cookie"] = cookie_header

    print("Fetching first page...")
    resp = session.get(ORDERS_ENDPOINT)
    resp.raise_for_status()
    data = resp.json().get("data")
    if not data:
        raise SystemExit(
            "No data returned. Your session may have expired -- rerun swiggy_login.py."
        )

    orders = data.get("orders") or []
    total_orders = data.get("total_orders", len(orders))
    if not orders:
        print("No orders found on your account.")
        return

    all_orders = [normalize_order(o) for o in orders]
    print(f"Fetched {len(all_orders)}/{total_orders} so far...")

    offset_id = orders[-1]["order_id"]
    while len(all_orders) < total_orders:
        time.sleep(1.5)  # be polite
        resp = session.get(ORDERS_ENDPOINT, params={"order_id": offset_id})
        resp.raise_for_status()
        batch = resp.json().get("data", {}).get("orders") or []
        if not batch:
            break

        all_orders.extend(normalize_order(o) for o in batch)
        offset_id = batch[-1]["order_id"]
        print(f"Fetched {len(all_orders)}/{total_orders} so far...")

    ORDERS_FILE.write_text(json.dumps(all_orders, indent=2))
    print(f"Saved {len(all_orders)} orders to {ORDERS_FILE.resolve()}")


if __name__ == "__main__":
    main()

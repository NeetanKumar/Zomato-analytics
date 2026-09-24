"""
Pulls your full Zomato order history using the session saved by login.py,
and writes it to orders.json. Run login.py first.
"""

import json
import time
from pathlib import Path

import requests

COOKIE_FILE = Path("cookies.json")
ORDERS_FILE = Path("orders.json")
ORDERS_ENDPOINT = "https://www.zomato.com/webroutes/user/orders"

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://www.zomato.com/",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    ),
}


def load_cookie_header() -> str:
    if not COOKIE_FILE.exists():
        raise SystemExit("cookies.json not found. Run login.py first.")
    cookies = json.loads(COOKIE_FILE.read_text())
    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


def normalize_cost(raw: str) -> float:
    cleaned = raw.replace("₹", "").replace("₹", "").replace(",", "").strip()
    return float(cleaned)


def fetch_page(session: requests.Session, page: int) -> list[dict]:
    resp = session.get(ORDERS_ENDPOINT, params={"page": page})
    resp.raise_for_status()
    data = resp.json()

    entities = data.get("entities", {}).get("ORDER", {})
    # Zomato returns {} when there are orders and [] once the pages run out.
    order_values = entities.values() if isinstance(entities, dict) else entities
    orders = []
    for order in order_values:
        try:
            res_info = order.get("resInfo", {})
            establishment = res_info.get("establishment") or []
            orders.append(
                {
                    "order_id": order["orderId"],
                    "order_date": order["orderDate"],
                    "total_cost": normalize_cost(order["totalCost"]),
                    "restaurant_id": res_info.get("id"),
                    "restaurant_name": res_info.get("name"),
                    "establishment": establishment[0] if establishment else "",
                }
            )
        except (KeyError, ValueError) as e:
            print(f"Skipping malformed order: {e}")
    return orders


def main():
    cookie_header = load_cookie_header()
    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers["cookie"] = cookie_header

    all_orders = []
    page = 1
    while True:
        print(f"Fetching page {page}...")
        orders = fetch_page(session, page)
        if not orders:
            break
        all_orders.extend(orders)
        page += 1
        time.sleep(1)  # be polite

    if not all_orders:
        print(
            "No orders returned on the first page. Your session may have "
            "expired -- rerun login.py."
        )
        return

    ORDERS_FILE.write_text(json.dumps(all_orders, indent=2))
    print(f"Saved {len(all_orders)} orders to {ORDERS_FILE.resolve()}")


if __name__ == "__main__":
    main()

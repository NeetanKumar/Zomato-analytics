"""
Summarizes swiggy_orders.json into a spending/ordering report.
Run swiggy_fetch_orders.py first. Prints a summary and writes
swiggy_summary.csv (per-restaurant breakdown) for further digging.
"""

import json
from collections import Counter
from pathlib import Path

import pandas as pd

ORDERS_FILE = Path("swiggy_orders.json")
SUMMARY_CSV = Path("swiggy_summary.csv")


def main():
    if not ORDERS_FILE.exists():
        raise SystemExit("swiggy_orders.json not found. Run swiggy_fetch_orders.py first.")

    orders = json.loads(ORDERS_FILE.read_text())
    if not orders:
        raise SystemExit("swiggy_orders.json is empty.")

    df = pd.DataFrame(orders)
    df = df[df["order_status"] == "Delivered"].copy()
    if df.empty:
        raise SystemExit("No delivered orders found.")

    df["order_time"] = pd.to_datetime(df["order_time"], errors="coerce")
    df = df.dropna(subset=["order_time"])
    df["month"] = df["order_time"].dt.to_period("M")

    total_spent = df["order_total"].sum()
    total_orders = len(df)
    avg_order = df["order_total"].mean()
    date_range = f"{df['order_time'].min().date()} to {df['order_time'].max().date()}"

    print("=" * 50)
    print("SWIGGY ORDER SUMMARY")
    print("=" * 50)
    print(f"Date range:       {date_range}")
    print(f"Total orders:     {total_orders}")
    print(f"Total spent:      ₹{total_spent:,.0f}")
    print(f"Average order:    ₹{avg_order:,.0f}")

    print("\nTop 10 restaurants by number of orders:")
    top_by_count = df.groupby("restaurant_name").size().sort_values(ascending=False).head(10)
    for name, count in top_by_count.items():
        print(f"  {count:>3}x  {name}")

    print("\nTop 10 restaurants by total spend:")
    top_by_spend = (
        df.groupby("restaurant_name")["order_total"].sum().sort_values(ascending=False).head(10)
    )
    for name, spend in top_by_spend.items():
        print(f"  ₹{spend:>8,.0f}  {name}")

    print("\nSpend by month:")
    monthly = df.groupby("month")["order_total"].sum()
    for month, spend in monthly.items():
        print(f"  {month}: ₹{spend:,.0f}")

    item_counts = Counter()
    for items in df.get("items", []):
        item_counts.update(items or [])
    if item_counts:
        print("\nTop 10 items ordered:")
        for name, count in item_counts.most_common(10):
            print(f"  {count:>3}x  {name}")

    per_restaurant = (
        df.groupby("restaurant_name")
        .agg(orders=("order_id", "count"), total_spent=("order_total", "sum"))
        .sort_values("total_spent", ascending=False)
    )
    per_restaurant["avg_order"] = per_restaurant["total_spent"] / per_restaurant["orders"]
    per_restaurant.to_csv(SUMMARY_CSV)
    print(f"\nFull per-restaurant breakdown written to {SUMMARY_CSV.resolve()}")


if __name__ == "__main__":
    main()

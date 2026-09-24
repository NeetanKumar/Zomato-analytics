"""
Summarizes orders.json into a spending/ordering report.
Run fetch_orders.py first. Prints a summary and writes summary.csv
(per-restaurant breakdown) for further digging.
"""

import json
from pathlib import Path

import pandas as pd

ORDERS_FILE = Path("orders.json")
SUMMARY_CSV = Path("summary.csv")


def main():
    if not ORDERS_FILE.exists():
        raise SystemExit("orders.json not found. Run fetch_orders.py first.")

    orders = json.loads(ORDERS_FILE.read_text())
    if not orders:
        raise SystemExit("orders.json is empty.")

    df = pd.DataFrame(orders)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    df["month"] = df["order_date"].dt.to_period("M")

    total_spent = df["total_cost"].sum()
    total_orders = len(df)
    avg_order = df["total_cost"].mean()
    date_range = f"{df['order_date'].min().date()} to {df['order_date'].max().date()}"

    print("=" * 50)
    print("ZOMATO ORDER SUMMARY")
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
        df.groupby("restaurant_name")["total_cost"].sum().sort_values(ascending=False).head(10)
    )
    for name, spend in top_by_spend.items():
        print(f"  ₹{spend:>8,.0f}  {name}")

    print("\nSpend by month:")
    monthly = df.groupby("month")["total_cost"].sum()
    for month, spend in monthly.items():
        print(f"  {month}: ₹{spend:,.0f}")

    if "establishment" in df.columns:
        print("\nOrders by establishment type:")
        est_counts = df["establishment"].value_counts().head(10)
        for est, count in est_counts.items():
            label = est if est else "(unspecified)"
            print(f"  {count:>3}x  {label}")

    per_restaurant = (
        df.groupby("restaurant_name")
        .agg(orders=("order_id", "count"), total_spent=("total_cost", "sum"))
        .sort_values("total_spent", ascending=False)
    )
    per_restaurant["avg_order"] = per_restaurant["total_spent"] / per_restaurant["orders"]
    per_restaurant.to_csv(SUMMARY_CSV)
    print(f"\nFull per-restaurant breakdown written to {SUMMARY_CSV.resolve()}")


if __name__ == "__main__":
    main()

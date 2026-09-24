"""
Summarizes orders.json into a spending/ordering report.
Run fetch_orders.py first. Writes order_summary.md (the full readable
report) and summary.csv (per-restaurant breakdown); prints just a short
confirmation rather than dumping the whole report to the terminal.
"""

import json
from pathlib import Path

import pandas as pd

ORDERS_FILE = Path("orders.json")
SUMMARY_CSV = Path("summary.csv")
SUMMARY_MD = Path("order_summary.md")


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

    top_by_count = df.groupby("restaurant_name").size().sort_values(ascending=False).head(10)
    top_by_spend = (
        df.groupby("restaurant_name")["total_cost"].sum().sort_values(ascending=False).head(10)
    )
    monthly = df.groupby("month")["total_cost"].sum()
    if "establishment" in df.columns:
        est_counts = df["establishment"].value_counts().head(10)

    per_restaurant = (
        df.groupby("restaurant_name")
        .agg(orders=("order_id", "count"), total_spent=("total_cost", "sum"))
        .sort_values("total_spent", ascending=False)
    )
    per_restaurant["avg_order"] = per_restaurant["total_spent"] / per_restaurant["orders"]
    per_restaurant.to_csv(SUMMARY_CSV)

    md_lines = [
        "# Zomato Order Summary",
        "",
        f"Data range: {date_range} ({total_orders} orders)",
        "",
        "## Overview",
        "",
        f"- Total spent: ₹{total_spent:,.0f}",
        f"- Total orders: {total_orders}",
        f"- Average order: ₹{avg_order:,.0f}",
        "",
        "## Top restaurants by order count",
        "",
        "| Restaurant | Orders |",
        "|---|---|",
    ]
    md_lines += [f"| {name} | {count} |" for name, count in top_by_count.items()]
    md_lines += [
        "",
        "## Top restaurants by total spend",
        "",
        "| Restaurant | Spend |",
        "|---|---|",
    ]
    md_lines += [f"| {name} | ₹{spend:,.0f} |" for name, spend in top_by_spend.items()]
    md_lines += [
        "",
        "## Spend by month",
        "",
        "| Month | Spend |",
        "|---|---|",
    ]
    md_lines += [f"| {month} | ₹{spend:,.0f} |" for month, spend in monthly.items()]

    if "establishment" in df.columns:
        md_lines += [
            "",
            "## Orders by establishment type",
            "",
            "| Type | Orders |",
            "|---|---|",
        ]
        md_lines += [
            f"| {est if est else '(unspecified)'} | {count} |"
            for est, count in est_counts.items()
        ]

    SUMMARY_MD.write_text("\n".join(md_lines) + "\n")

    print(
        f"{total_orders} orders, ₹{total_spent:,.0f} total -- "
        f"full report written to {SUMMARY_MD.resolve()} "
        f"(and {SUMMARY_CSV.resolve()})"
    )


if __name__ == "__main__":
    main()

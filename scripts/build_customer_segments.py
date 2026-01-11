#!/usr/bin/env python3
"""
Build business-oriented customer segments from customer-level sales data.

Input:
  data/customer_sales_data.csv

Output:
  Printed customer segments and summary counts.

Usage:
  python scripts/build_customer_segments.py
"""

from pathlib import Path
import csv
from collections import defaultdict


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "customer_sales_data.csv"


def to_float(x: str) -> float:
    return float(x.strip())


def to_int(x: str) -> int:
    return int(float(x.strip()))


def assign_segment(revenue, invoices, months_active):
    if revenue >= 450 and invoices >= 4:
        return "Strategic Account"
    if revenue >= 300 and invoices >= 3:
        return "Growth Account"
    if revenue >= 150:
        return "Stable Account"
    return "At-Risk Account"


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing dataset: {DATA_PATH}")

    segments = defaultdict(list)

    with DATA_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            pharmacy_id = row["pharmacy_id"]
            revenue = to_float(row["total_revenue"])
            invoices = to_int(row["total_invoices"])
            months_active = to_int(row["months_active"])

            segment = assign_segment(revenue, invoices, months_active)
            segments[segment].append(pharmacy_id)

    print("=== Customer Segmentation Results ===")
    for segment, customers in segments.items():
        print(f"\n{segment} ({len(customers)} customers)")
        for cid in customers:
            print(f"  - {cid}")


if __name__ == "__main__":
    main()

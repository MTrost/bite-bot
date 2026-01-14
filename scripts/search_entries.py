#!/usr/bin/env python3
"""Search for entries in intake.csv"""

import argparse
import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"

def main():
    parser = argparse.ArgumentParser(description="Search intake entries")
    parser.add_argument("--food", type=str, help="Search by food name (partial match)")
    parser.add_argument("--date", type=str, help="Filter by date (YYYY-MM-DD)")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default 10)")

    args = parser.parse_args()

    if not DATA_FILE.exists():
        print("No intake data file found")
        return

    matches = []
    with open(DATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # start=2 because row 1 is header
            match = True

            if args.food:
                if args.food.lower() not in row.get("food_name", "").lower():
                    match = False

            if args.date:
                if not row.get("timestamp", "").startswith(args.date):
                    match = False

            if match:
                matches.append((row_num, row))

    if not matches:
        print("No matching entries found")
        return

    print(f"Found {len(matches)} entries:\n")
    for row_num, row in matches[:args.limit]:
        timestamp = row.get("timestamp", "N/A")
        food = row.get("food_name", "N/A")
        amount = row.get("amount_g", "?")
        calories = row.get("calories", "?")

        print(f"  ID {row_num}: {food} ({amount}g, {calories} cal)")
        print(f"           Logged: {timestamp}")

    if len(matches) > args.limit:
        print(f"\n  ... and {len(matches) - args.limit} more (use --limit to show more)")

if __name__ == "__main__":
    main()

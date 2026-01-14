#!/usr/bin/env python3
"""Delete an entry from intake.csv"""

import argparse
import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"

def main():
    parser = argparse.ArgumentParser(description="Delete intake entry")
    parser.add_argument("--id", type=int, required=True, help="Row ID to delete")
    parser.add_argument("--confirm", action="store_true", help="Skip confirmation")

    args = parser.parse_args()

    if not DATA_FILE.exists():
        print("No intake data file found")
        return

    # Read all data
    rows = []
    fieldnames = []
    with open(DATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)

    # Find the row (ID is 1-indexed with header as row 1)
    row_index = args.id - 2  # Convert to 0-indexed, accounting for header

    if row_index < 0 or row_index >= len(rows):
        print(f"Error: Row ID {args.id} not found")
        return

    to_delete = rows[row_index]
    food_name = to_delete.get("food_name", "entry")
    amount = to_delete.get("amount_g", "?")
    timestamp = to_delete.get("timestamp", "?")

    if not args.confirm:
        print(f"Will delete: {food_name} ({amount}g) logged at {timestamp}")
        print("Run with --confirm to execute deletion")
        return

    # Delete and write back
    del rows[row_index]

    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Deleted: {food_name} ({amount}g) logged at {timestamp}")

if __name__ == "__main__":
    main()

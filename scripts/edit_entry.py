#!/usr/bin/env python3
"""Edit an entry in intake.csv"""

import argparse
import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"

def main():
    parser = argparse.ArgumentParser(description="Edit intake entry")
    parser.add_argument("--id", type=int, required=True, help="Row ID to edit")
    parser.add_argument("--field", type=str, required=True, help="Field name to edit")
    parser.add_argument("--value", type=str, required=True, help="New value")
    parser.add_argument("--recalculate", action="store_true",
                        help="Recalculate nutrients if amount changed (not implemented)")

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

    if args.field not in fieldnames:
        print(f"Error: Unknown field '{args.field}'")
        print(f"Valid fields: {', '.join(fieldnames)}")
        return

    # Find and edit the row (ID is 1-indexed with header as row 1)
    row_index = args.id - 2  # Convert to 0-indexed, accounting for header

    if row_index < 0 or row_index >= len(rows):
        print(f"Error: Row ID {args.id} not found")
        return

    old_value = rows[row_index].get(args.field, "")
    rows[row_index][args.field] = args.value

    # Write back
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    food_name = rows[row_index].get("food_name", "entry")
    print(f"Updated {food_name}:")
    print(f"  {args.field}: {old_value} -> {args.value}")

    if args.recalculate:
        print("  Note: --recalculate flag set but automatic recalculation not implemented.")
        print("  Please manually update nutrient values proportionally.")

if __name__ == "__main__":
    main()

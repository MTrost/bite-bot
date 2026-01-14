#!/usr/bin/env python3
"""Edit an entry in intake.csv"""

import argparse
import csv
import json
import subprocess
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"
LOOKUP_SCRIPT = Path(__file__).parent / "lookup_usda.py"

# Nutrient columns that can be recalculated from USDA data
NUTRIENT_COLS = [
    "calories", "protein_g", "carbs_g", "fiber_g", "sugar_g", "fat_g",
    "saturated_fat_g", "trans_fat_g", "cholesterol_mg", "sodium_mg",
    "potassium_mg", "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
    "zinc_mg", "copper_mg", "manganese_mg", "selenium_mcg", "vitamin_a_mcg",
    "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg", "vitamin_k_mcg",
    "vitamin_b1_mg", "vitamin_b2_mg", "vitamin_b3_mg", "vitamin_b5_mg",
    "vitamin_b6_mg", "vitamin_b7_mcg", "vitamin_b9_mcg", "vitamin_b12_mcg"
]


def lookup_usda(fdc_id: int) -> dict:
    """Look up USDA data by FDC ID, returns per-100g values."""
    result = subprocess.run(
        ["python3", str(LOOKUP_SCRIPT), "--id", str(fdc_id), "--json"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return None
    data = json.loads(result.stdout)
    return data[0] if data else None


def recalculate_nutrients(row: dict, new_amount: float) -> dict:
    """Recalculate nutrients based on new amount using USDA data."""
    fdc_id = row.get("usda_fdc_id")
    if not fdc_id:
        return None

    try:
        fdc_id = int(fdc_id)
    except (ValueError, TypeError):
        return None

    usda_data = lookup_usda(fdc_id)
    if not usda_data:
        return None

    # Scale per-100g values to new amount
    scale = new_amount / 100.0
    updates = {}
    for col in NUTRIENT_COLS:
        if col in usda_data and usda_data[col] is not None:
            updates[col] = round(usda_data[col] * scale, 3)

    return updates


def main():
    parser = argparse.ArgumentParser(description="Edit intake entry")
    parser.add_argument("--id", type=int, required=True, help="Row ID to edit")
    parser.add_argument("--field", type=str, required=True, help="Field name to edit")
    parser.add_argument("--value", type=str, required=True, help="New value")
    parser.add_argument("--recalculate", action="store_true",
                        help="Recalculate nutrients when amount changes (requires usda_fdc_id)")

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

    # Find the row (ID is 1-indexed with header as row 1)
    row_index = args.id - 2  # Convert to 0-indexed, accounting for header

    if row_index < 0 or row_index >= len(rows):
        print(f"Error: Row ID {args.id} not found")
        return

    old_value = rows[row_index].get(args.field, "")
    rows[row_index][args.field] = args.value

    food_name = rows[row_index].get("food_name", "entry")
    print(f"Updated {food_name}:")
    print(f"  {args.field}: {old_value} -> {args.value}")

    # Handle recalculation if amount_g changed
    if args.recalculate and args.field == "amount_g":
        try:
            new_amount = float(args.value)
            updates = recalculate_nutrients(rows[row_index], new_amount)
            if updates:
                for col, val in updates.items():
                    old_val = rows[row_index].get(col, "")
                    rows[row_index][col] = val
                    if old_val:
                        print(f"  {col}: {old_val} -> {val}")
                print(f"  (Recalculated {len(updates)} nutrients from USDA data)")
            else:
                fdc_id = rows[row_index].get("usda_fdc_id")
                if not fdc_id:
                    print("  Warning: No usda_fdc_id - cannot recalculate nutrients")
                else:
                    print("  Warning: Could not fetch USDA data for recalculation")
        except ValueError:
            print("  Warning: Could not parse amount for recalculation")

    elif args.recalculate and args.field != "amount_g":
        print("  Note: --recalculate only works when editing amount_g")

    # Write back
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()

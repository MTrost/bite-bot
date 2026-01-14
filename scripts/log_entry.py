#!/usr/bin/env python3
"""Log a food entry to intake.csv"""

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import subprocess

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"
LOOKUP_SCRIPT = Path(__file__).parent / "lookup_usda.py"

COLUMNS = [
    "timestamp", "food_name", "amount_g", "usda_fdc_id", "calories", "protein_g", "carbs_g",
    "fiber_g", "sugar_g", "fat_g", "saturated_fat_g", "trans_fat_g",
    "cholesterol_mg", "sodium_mg", "potassium_mg", "calcium_mg", "iron_mg",
    "magnesium_mg", "phosphorus_mg", "zinc_mg", "copper_mg", "manganese_mg",
    "selenium_mcg", "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg",
    "vitamin_e_mg", "vitamin_k_mcg", "vitamin_b1_mg", "vitamin_b2_mg",
    "vitamin_b3_mg", "vitamin_b5_mg", "vitamin_b6_mg", "vitamin_b7_mcg",
    "vitamin_b9_mcg", "vitamin_b12_mcg", "omega3_g", "omega6_g", "water_g",
    "caffeine_mg", "alcohol_g", "notes"
]


def lookup_usda(fdc_id: int) -> dict:
    """Look up USDA data by FDC ID, returns per-100g values."""
    result = subprocess.run(
        ["python3", str(LOOKUP_SCRIPT), "--id", str(fdc_id), "--json"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise ValueError(f"USDA lookup failed: {result.stderr}")

    data = json.loads(result.stdout)
    if not data:
        raise ValueError(f"No food found with FDC ID {fdc_id}")
    return data[0]


def scale_nutrients(nutrients: dict, amount_g: float) -> dict:
    """Scale per-100g nutrients to actual amount."""
    scale = amount_g / 100.0
    scaled = {}
    for key, value in nutrients.items():
        if key in ("food_name", "fdcId", "portions"):
            scaled[key] = value
        elif isinstance(value, (int, float)):
            scaled[key] = round(value * scale, 3)
    return scaled


def main():
    parser = argparse.ArgumentParser(description="Log food to intake.csv")
    parser.add_argument("--food", required=True, help="Food name")
    parser.add_argument("--amount", type=float, required=True, help="Amount in grams")
    parser.add_argument("--usda-id", type=int, help="USDA FDC ID - auto-fetches and scales nutrients")
    parser.add_argument("--calories", type=float, help="Calories (kcal)")
    parser.add_argument("--protein", type=float, help="Protein (g)")
    parser.add_argument("--carbs", type=float, help="Carbohydrates (g)")
    parser.add_argument("--fat", type=float, help="Fat (g)")
    parser.add_argument("--fiber", type=float, help="Fiber (g)")
    parser.add_argument("--sugar", type=float, help="Sugar (g)")
    parser.add_argument("--saturated-fat", type=float, help="Saturated fat (g)")
    parser.add_argument("--trans-fat", type=float, help="Trans fat (g)")
    parser.add_argument("--cholesterol", type=float, help="Cholesterol (mg)")
    parser.add_argument("--sodium", type=float, help="Sodium (mg)")
    parser.add_argument("--potassium", type=float, help="Potassium (mg)")
    parser.add_argument("--calcium", type=float, help="Calcium (mg)")
    parser.add_argument("--iron", type=float, help="Iron (mg)")
    parser.add_argument("--magnesium", type=float, help="Magnesium (mg)")
    parser.add_argument("--phosphorus", type=float, help="Phosphorus (mg)")
    parser.add_argument("--zinc", type=float, help="Zinc (mg)")
    parser.add_argument("--copper", type=float, help="Copper (mg)")
    parser.add_argument("--manganese", type=float, help="Manganese (mg)")
    parser.add_argument("--selenium", type=float, help="Selenium (mcg)")
    parser.add_argument("--vitamin-a", type=float, help="Vitamin A (mcg)")
    parser.add_argument("--vitamin-c", type=float, help="Vitamin C (mg)")
    parser.add_argument("--vitamin-d", type=float, help="Vitamin D (mcg)")
    parser.add_argument("--vitamin-e", type=float, help="Vitamin E (mg)")
    parser.add_argument("--vitamin-k", type=float, help="Vitamin K (mcg)")
    parser.add_argument("--vitamin-b1", type=float, help="Vitamin B1/Thiamin (mg)")
    parser.add_argument("--vitamin-b2", type=float, help="Vitamin B2/Riboflavin (mg)")
    parser.add_argument("--vitamin-b3", type=float, help="Vitamin B3/Niacin (mg)")
    parser.add_argument("--vitamin-b5", type=float, help="Vitamin B5/Pantothenic acid (mg)")
    parser.add_argument("--vitamin-b6", type=float, help="Vitamin B6 (mg)")
    parser.add_argument("--vitamin-b7", type=float, help="Vitamin B7/Biotin (mcg)")
    parser.add_argument("--vitamin-b9", type=float, help="Vitamin B9/Folate (mcg)")
    parser.add_argument("--vitamin-b12", type=float, help="Vitamin B12 (mcg)")
    parser.add_argument("--omega3", type=float, help="Omega-3 (g)")
    parser.add_argument("--omega6", type=float, help="Omega-6 (g)")
    parser.add_argument("--water", type=float, help="Water (g)")
    parser.add_argument("--caffeine", type=float, help="Caffeine (mg)")
    parser.add_argument("--alcohol", type=float, help="Alcohol (g)")
    parser.add_argument("--notes", type=str, help="Optional notes")
    parser.add_argument("--timestamp", type=str, help="ISO timestamp (default: now)")

    args = parser.parse_args()

    # Build row
    timestamp = args.timestamp or datetime.now().isoformat(timespec='seconds')

    row = {col: "" for col in COLUMNS}
    row["timestamp"] = timestamp
    row["food_name"] = args.food
    row["amount_g"] = args.amount

    # If USDA ID provided, fetch and scale nutrients
    usda_nutrients = {}
    if args.usda_id:
        try:
            raw_nutrients = lookup_usda(args.usda_id)
            usda_nutrients = scale_nutrients(raw_nutrients, args.amount)
            row["usda_fdc_id"] = args.usda_id
        except Exception as e:
            print(f"Warning: USDA lookup failed: {e}")
            print("Continuing with manually provided values...")

    # USDA keys match CSV columns (both use protein_g, etc.)
    # Arg names use short forms (protein, carbs, etc.)
    arg_to_csv = {
        "calories": "calories",
        "protein": "protein_g",
        "carbs": "carbs_g",
        "fat": "fat_g",
        "fiber": "fiber_g",
        "sugar": "sugar_g",
        "saturated_fat": "saturated_fat_g",
        "trans_fat": "trans_fat_g",
        "cholesterol": "cholesterol_mg",
        "sodium": "sodium_mg",
        "potassium": "potassium_mg",
        "calcium": "calcium_mg",
        "iron": "iron_mg",
        "magnesium": "magnesium_mg",
        "phosphorus": "phosphorus_mg",
        "zinc": "zinc_mg",
        "copper": "copper_mg",
        "manganese": "manganese_mg",
        "selenium": "selenium_mcg",
        "vitamin_a": "vitamin_a_mcg",
        "vitamin_c": "vitamin_c_mg",
        "vitamin_d": "vitamin_d_mcg",
        "vitamin_e": "vitamin_e_mg",
        "vitamin_k": "vitamin_k_mcg",
        "vitamin_b1": "vitamin_b1_mg",
        "vitamin_b2": "vitamin_b2_mg",
        "vitamin_b3": "vitamin_b3_mg",
        "vitamin_b5": "vitamin_b5_mg",
        "vitamin_b6": "vitamin_b6_mg",
        "vitamin_b7": "vitamin_b7_mcg",
        "vitamin_b9": "vitamin_b9_mcg",
        "vitamin_b12": "vitamin_b12_mcg",
        "omega3": "omega3_g",
        "omega6": "omega6_g",
        "water": "water_g",
        "caffeine": "caffeine_mg",
        "alcohol": "alcohol_g",
    }

    # Apply USDA values (keys already match CSV columns)
    for csv_col in COLUMNS:
        if csv_col in usda_nutrients and csv_col != "food_name":
            val = usda_nutrients[csv_col]
            if val is not None and val != "":
                row[csv_col] = val

    # Override with manual values
    for arg_name, csv_col in arg_to_csv.items():
        arg_val = getattr(args, arg_name.replace("-", "_"), None)
        if arg_val is not None:
            row[csv_col] = arg_val

    row["notes"] = args.notes or ""

    # Append to CSV
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writerow(row)

    print(f"Logged: {args.food} ({args.amount}g)")
    if row.get("usda_fdc_id"):
        print(f"  Source: USDA FDC ID {row['usda_fdc_id']}")
    if row.get("calories"):
        print(f"  Calories: {row['calories']}")
    if row.get("protein_g"):
        print(f"  Protein: {row['protein_g']}g")
    if row.get("carbs_g"):
        print(f"  Carbs: {row['carbs_g']}g")
    if row.get("fat_g"):
        print(f"  Fat: {row['fat_g']}g")


if __name__ == "__main__":
    main()

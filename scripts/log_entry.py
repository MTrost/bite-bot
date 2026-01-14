#!/usr/bin/env python3
"""Log a food entry to intake.csv"""

import argparse
import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"

COLUMNS = [
    "timestamp", "food_name", "amount_g", "calories", "protein_g", "carbs_g",
    "fiber_g", "sugar_g", "fat_g", "saturated_fat_g", "trans_fat_g",
    "cholesterol_mg", "sodium_mg", "potassium_mg", "calcium_mg", "iron_mg",
    "magnesium_mg", "phosphorus_mg", "zinc_mg", "copper_mg", "manganese_mg",
    "selenium_mcg", "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg",
    "vitamin_e_mg", "vitamin_k_mcg", "vitamin_b1_mg", "vitamin_b2_mg",
    "vitamin_b3_mg", "vitamin_b5_mg", "vitamin_b6_mg", "vitamin_b7_mcg",
    "vitamin_b9_mcg", "vitamin_b12_mcg", "omega3_g", "omega6_g", "water_g",
    "caffeine_mg", "alcohol_g", "notes"
]

def main():
    parser = argparse.ArgumentParser(description="Log food to intake.csv")
    parser.add_argument("--food", required=True, help="Food name")
    parser.add_argument("--amount", type=float, required=True, help="Amount in grams")
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
    row["calories"] = args.calories if args.calories is not None else ""
    row["protein_g"] = args.protein if args.protein is not None else ""
    row["carbs_g"] = args.carbs if args.carbs is not None else ""
    row["fat_g"] = args.fat if args.fat is not None else ""
    row["fiber_g"] = args.fiber if args.fiber is not None else ""
    row["sugar_g"] = args.sugar if args.sugar is not None else ""
    row["saturated_fat_g"] = getattr(args, 'saturated_fat', None) or ""
    row["trans_fat_g"] = getattr(args, 'trans_fat', None) or ""
    row["cholesterol_mg"] = args.cholesterol if args.cholesterol is not None else ""
    row["sodium_mg"] = args.sodium if args.sodium is not None else ""
    row["potassium_mg"] = args.potassium if args.potassium is not None else ""
    row["calcium_mg"] = args.calcium if args.calcium is not None else ""
    row["iron_mg"] = args.iron if args.iron is not None else ""
    row["magnesium_mg"] = args.magnesium if args.magnesium is not None else ""
    row["phosphorus_mg"] = args.phosphorus if args.phosphorus is not None else ""
    row["zinc_mg"] = args.zinc if args.zinc is not None else ""
    row["copper_mg"] = args.copper if args.copper is not None else ""
    row["manganese_mg"] = args.manganese if args.manganese is not None else ""
    row["selenium_mcg"] = args.selenium if args.selenium is not None else ""
    row["vitamin_a_mcg"] = getattr(args, 'vitamin_a', None) or ""
    row["vitamin_c_mg"] = getattr(args, 'vitamin_c', None) or ""
    row["vitamin_d_mcg"] = getattr(args, 'vitamin_d', None) or ""
    row["vitamin_e_mg"] = getattr(args, 'vitamin_e', None) or ""
    row["vitamin_k_mcg"] = getattr(args, 'vitamin_k', None) or ""
    row["vitamin_b1_mg"] = getattr(args, 'vitamin_b1', None) or ""
    row["vitamin_b2_mg"] = getattr(args, 'vitamin_b2', None) or ""
    row["vitamin_b3_mg"] = getattr(args, 'vitamin_b3', None) or ""
    row["vitamin_b5_mg"] = getattr(args, 'vitamin_b5', None) or ""
    row["vitamin_b6_mg"] = getattr(args, 'vitamin_b6', None) or ""
    row["vitamin_b7_mcg"] = getattr(args, 'vitamin_b7', None) or ""
    row["vitamin_b9_mcg"] = getattr(args, 'vitamin_b9', None) or ""
    row["vitamin_b12_mcg"] = getattr(args, 'vitamin_b12', None) or ""
    row["omega3_g"] = args.omega3 if args.omega3 is not None else ""
    row["omega6_g"] = args.omega6 if args.omega6 is not None else ""
    row["water_g"] = args.water if args.water is not None else ""
    row["caffeine_mg"] = args.caffeine if args.caffeine is not None else ""
    row["alcohol_g"] = args.alcohol if args.alcohol is not None else ""
    row["notes"] = args.notes or ""

    # Append to CSV
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writerow(row)

    print(f"Logged: {args.food} ({args.amount}g)")
    if args.calories:
        print(f"  Calories: {args.calories}")
    if args.protein:
        print(f"  Protein: {args.protein}g")
    if args.carbs:
        print(f"  Carbs: {args.carbs}g")
    if args.fat:
        print(f"  Fat: {args.fat}g")

if __name__ == "__main__":
    main()

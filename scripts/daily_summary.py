#!/usr/bin/env python3
"""Get daily nutritional summary from intake.csv"""

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"
TARGETS_FILE = Path(__file__).parent.parent / "data" / "targets.csv"

MACRO_FIELDS = ["calories", "protein_g", "carbs_g", "fiber_g", "sugar_g", "fat_g"]
MINERAL_FIELDS = ["sodium_mg", "potassium_mg", "calcium_mg", "iron_mg", "magnesium_mg", "zinc_mg"]
VITAMIN_FIELDS = ["vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_b12_mcg"]

def load_targets():
    """Load daily targets from targets.csv"""
    targets = {}
    if TARGETS_FILE.exists():
        with open(TARGETS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                targets[row["nutrient"]] = float(row["daily_target"])
    return targets

def get_entries_for_date(date_str):
    """Get all entries for a specific date"""
    entries = []
    with open(DATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["timestamp"].startswith(date_str):
                entries.append(row)
    return entries

def sum_nutrients(entries, fields):
    """Sum nutrient values across entries"""
    totals = {field: 0 for field in fields}
    for entry in entries:
        for field in fields:
            val = entry.get(field, "")
            if val and val.strip():
                try:
                    totals[field] += float(val)
                except ValueError:
                    pass
    return totals

def format_pct(value, target):
    """Format as percentage of target"""
    if target and target > 0:
        pct = (value / target) * 100
        return f"{pct:.0f}%"
    return "N/A"

def main():
    parser = argparse.ArgumentParser(description="Daily nutritional summary")
    parser.add_argument("--date", type=str, help="Date (YYYY-MM-DD), default today")
    parser.add_argument("--range", type=int, help="Show last N days")
    parser.add_argument("--all", action="store_true", help="Show all nutrients, not just macros")

    args = parser.parse_args()

    targets = load_targets()

    if args.range:
        # Multi-day summary
        dates = []
        for i in range(args.range):
            d = datetime.now() - timedelta(days=i)
            dates.append(d.strftime("%Y-%m-%d"))
        dates.reverse()

        print(f"Last {args.range} days:\n")
        all_totals = {field: 0 for field in MACRO_FIELDS}
        days_with_data = 0

        for date_str in dates:
            entries = get_entries_for_date(date_str)
            if entries:
                days_with_data += 1
                totals = sum_nutrients(entries, MACRO_FIELDS)
                for field in MACRO_FIELDS:
                    all_totals[field] += totals[field]
                print(f"{date_str}: {totals['calories']:.0f} cal, {totals['protein_g']:.0f}g protein, {totals['carbs_g']:.0f}g carbs, {totals['fat_g']:.0f}g fat")
            else:
                print(f"{date_str}: No entries")

        if days_with_data > 0:
            print(f"\nAverages ({days_with_data} days with data):")
            for field in MACRO_FIELDS:
                avg = all_totals[field] / days_with_data
                target = targets.get(field, 0)
                pct = format_pct(avg, target)
                print(f"  {field}: {avg:.1f} ({pct} of target)")
    else:
        # Single day
        date_str = args.date or datetime.now().strftime("%Y-%m-%d")
        entries = get_entries_for_date(date_str)

        if not entries:
            print(f"No entries for {date_str}")
            return

        print(f"Summary for {date_str}:\n")

        # Foods logged
        print("Foods logged:")
        for entry in entries:
            time = entry["timestamp"].split("T")[1] if "T" in entry["timestamp"] else ""
            print(f"  - {entry['food_name']} ({entry['amount_g']}g) {time}")
        print()

        # Macros
        print("Macros:")
        macro_totals = sum_nutrients(entries, MACRO_FIELDS)
        for field in MACRO_FIELDS:
            val = macro_totals[field]
            target = targets.get(field, 0)
            pct = format_pct(val, target)
            unit = "g" if field.endswith("_g") else "kcal"
            name = field.replace("_g", "").replace("_", " ").title()
            print(f"  {name}: {val:.1f}{unit} ({pct})")

        if args.all:
            print("\nMinerals:")
            mineral_totals = sum_nutrients(entries, MINERAL_FIELDS)
            for field in MINERAL_FIELDS:
                val = mineral_totals[field]
                if val > 0:
                    target = targets.get(field, 0)
                    pct = format_pct(val, target)
                    name = field.replace("_mg", "").replace("_", " ").title()
                    print(f"  {name}: {val:.1f}mg ({pct})")

            print("\nVitamins:")
            vitamin_totals = sum_nutrients(entries, VITAMIN_FIELDS)
            for field in VITAMIN_FIELDS:
                val = vitamin_totals[field]
                if val > 0:
                    target = targets.get(field, 0)
                    pct = format_pct(val, target)
                    unit = "mcg" if field.endswith("_mcg") else "mg"
                    name = field.replace("_mcg", "").replace("_mg", "").replace("_", " ").title()
                    print(f"  {name}: {val:.1f}{unit} ({pct})")

        # Warnings
        print("\nFlags:")
        has_flags = False
        for field in MACRO_FIELDS + MINERAL_FIELDS:
            target = targets.get(field, 0)
            if target > 0:
                totals = macro_totals if field in MACRO_FIELDS else sum_nutrients(entries, [field])
                val = totals.get(field, 0)
                pct = (val / target) * 100
                name = field.replace("_g", "").replace("_mg", "").replace("_", " ").title()
                if pct < 50:
                    print(f"  LOW: {name} at {pct:.0f}% of target")
                    has_flags = True
                elif pct > 150:
                    print(f"  HIGH: {name} at {pct:.0f}% of target")
                    has_flags = True

        if not has_flags:
            print("  None - all tracked nutrients within normal range")

if __name__ == "__main__":
    main()

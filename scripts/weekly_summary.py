#!/usr/bin/env python3
"""Weekly and monthly nutritional analysis with trends and insights."""

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

DATA_FILE = Path(__file__).parent.parent / "data" / "intake.csv"
TARGETS_FILE = Path(__file__).parent.parent / "data" / "targets.csv"

ALL_NUTRIENT_FIELDS = [
    "calories", "protein_g", "carbs_g", "fiber_g", "sugar_g", "fat_g",
    "saturated_fat_g", "trans_fat_g", "cholesterol_mg",
    "sodium_mg", "potassium_mg", "calcium_mg", "iron_mg", "magnesium_mg", "zinc_mg",
    "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg", "vitamin_k_mcg",
    "vitamin_b1_mg", "vitamin_b2_mg", "vitamin_b3_mg", "vitamin_b5_mg",
    "vitamin_b6_mg", "vitamin_b7_mcg", "vitamin_b9_mcg", "vitamin_b12_mcg"
]

def load_targets():
    """Load daily targets from targets.csv"""
    targets = {}
    if TARGETS_FILE.exists():
        with open(TARGETS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                targets[row["nutrient"]] = float(row["daily_target"])
    return targets

def get_entries_in_range(start_date, end_date):
    """Get all entries between start and end dates (inclusive)"""
    entries_by_date = defaultdict(list)
    with open(DATA_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_str = row["timestamp"].split("T")[0]
            if start_date <= date_str <= end_date:
                entries_by_date[date_str].append(row)
    return entries_by_date

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

def calculate_daily_totals(entries_by_date, fields):
    """Calculate totals for each day"""
    daily_totals = {}
    for date, entries in entries_by_date.items():
        daily_totals[date] = sum_nutrients(entries, fields)
    return daily_totals

def analyze_trends(daily_totals, field):
    """Analyze trend for a specific nutrient (increasing, decreasing, stable)"""
    if len(daily_totals) < 3:
        return "insufficient data"

    dates = sorted(daily_totals.keys())
    values = [daily_totals[d].get(field, 0) for d in dates]

    # Simple linear trend: compare first half to second half
    mid = len(values) // 2
    first_half_avg = sum(values[:mid]) / len(values[:mid])
    second_half_avg = sum(values[mid:]) / len(values[mid:])

    if first_half_avg == 0:
        return "stable"

    change_pct = ((second_half_avg - first_half_avg) / first_half_avg) * 100

    if change_pct > 10:
        return f"increasing (+{change_pct:.0f}%)"
    elif change_pct < -10:
        return f"decreasing ({change_pct:.0f}%)"
    else:
        return "stable"

def main():
    parser = argparse.ArgumentParser(description="Weekly/monthly nutritional analysis")
    parser.add_argument("--days", type=int, default=7, help="Number of days to analyze (default: 7)")
    parser.add_argument("--all-nutrients", action="store_true", help="Show all tracked nutrients")

    args = parser.parse_args()

    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=args.days - 1)

    end_str = end_date.strftime("%Y-%m-%d")
    start_str = start_date.strftime("%Y-%m-%d")

    print(f"{'='*60}")
    print(f"Nutritional Analysis: {start_str} to {end_str} ({args.days} days)")
    print(f"{'='*60}\n")

    # Load data
    targets = load_targets()
    entries_by_date = get_entries_in_range(start_str, end_str)

    if not entries_by_date:
        print("No entries found in this date range.")
        return

    days_with_data = len(entries_by_date)
    print(f"Days with logged food: {days_with_data}/{args.days}\n")

    # Calculate daily totals for key nutrients
    key_fields = ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g"]
    daily_totals = calculate_daily_totals(entries_by_date, ALL_NUTRIENT_FIELDS)

    # === DAILY BREAKDOWN ===
    print("DAILY BREAKDOWN")
    print("-" * 60)
    for date in sorted(entries_by_date.keys()):
        totals = daily_totals[date]
        print(f"{date}: {totals['calories']:.0f} cal | "
              f"P:{totals['protein_g']:.0f}g C:{totals['carbs_g']:.0f}g F:{totals['fat_g']:.0f}g")
    print()

    # === AVERAGES ===
    print("DAILY AVERAGES")
    print("-" * 60)
    averages = {}
    for field in ALL_NUTRIENT_FIELDS:
        total = sum(daily_totals[d].get(field, 0) for d in daily_totals)
        averages[field] = total / days_with_data if days_with_data > 0 else 0

    # Print macros
    for field in ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g"]:
        avg = averages[field]
        target = targets.get(field, 0)
        unit = "" if field == "calories" else "g"
        name = field.replace("_g", "").replace("_", " ").title()

        if target > 0:
            pct = (avg / target) * 100
            status = "✓" if 80 <= pct <= 120 else "!"
            print(f"  {status} {name:15s}: {avg:6.1f}{unit:3s} (Target: {target:.0f}, {pct:.0f}%)")
        else:
            print(f"    {name:15s}: {avg:6.1f}{unit}")

    if args.all_nutrients:
        print("\nMicronutrients:")
        for field in ALL_NUTRIENT_FIELDS:
            if field in ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g"]:
                continue

            avg = averages[field]
            if avg > 0:
                target = targets.get(field, 0)
                unit = "mcg" if field.endswith("_mcg") else "mg"
                name = field.replace("_mcg", "").replace("_mg", "").replace("_g", "").replace("_", " ").title()

                if target > 0:
                    pct = (avg / target) * 100
                    status = "✓" if 80 <= pct <= 120 else "!"
                    print(f"  {status} {name:20s}: {avg:6.1f}{unit:3s} (Target: {target:.0f}, {pct:.0f}%)")
                else:
                    print(f"    {name:20s}: {avg:6.1f}{unit}")

    # === TRENDS ===
    if days_with_data >= 3:
        print("\nTRENDS")
        print("-" * 60)
        for field in key_fields:
            trend = analyze_trends(daily_totals, field)
            name = field.replace("_g", "").replace("_", " ").title()
            print(f"  {name:15s}: {trend}")

    # === NUTRIENT GAPS & EXCESSES ===
    print("\nNUTRIENT GAPS & EXCESSES")
    print("-" * 60)
    gaps = []
    excesses = []

    for field, target in targets.items():
        if target > 0 and field in averages:
            avg = averages[field]
            pct = (avg / target) * 100
            name = field.replace("_g", "").replace("_mg", "").replace("_mcg", "").replace("_", " ").title()

            if pct < 70:
                gaps.append((name, pct, avg, target))
            elif pct > 150:
                excesses.append((name, pct, avg, target))

    if gaps:
        print("\nConsistently LOW (< 70% of target):")
        for name, pct, avg, target in sorted(gaps, key=lambda x: x[1]):
            print(f"  • {name}: {pct:.0f}% (avg {avg:.1f}, target {target:.0f})")

    if excesses:
        print("\nConsistently HIGH (> 150% of target):")
        for name, pct, avg, target in sorted(excesses, key=lambda x: -x[1]):
            print(f"  • {name}: {pct:.0f}% (avg {avg:.1f}, target {target:.0f})")

    if not gaps and not excesses:
        print("  ✓ All tracked nutrients within healthy range (70-150% of target)")

    print()

if __name__ == "__main__":
    main()

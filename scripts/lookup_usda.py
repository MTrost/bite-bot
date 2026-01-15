#!/usr/bin/env python3
"""Search USDA Foundation Foods database for nutritional information."""

import argparse
import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "usda" / "FoodData_Central_foundation_food_json_2025-12-18.json"

# Map USDA nutrient names to our CSV columns
NUTRIENT_MAP = {
    "Energy": "calories",  # We'll pick kcal version
    "Protein": "protein_g",
    "Carbohydrate, by difference": "carbs_g",
    "Fiber, total dietary": "fiber_g",
    "Sugars, total including NLEA": "sugar_g",
    "Total lipid (fat)": "fat_g",
    "Fatty acids, total saturated": "saturated_fat_g",
    "Fatty acids, total trans": "trans_fat_g",
    "Cholesterol": "cholesterol_mg",
    "Sodium, Na": "sodium_mg",
    "Potassium, K": "potassium_mg",
    "Calcium, Ca": "calcium_mg",
    "Iron, Fe": "iron_mg",
    "Magnesium, Mg": "magnesium_mg",
    "Zinc, Zn": "zinc_mg",
    "Vitamin A, RAE": "vitamin_a_mcg",
    "Vitamin C, total ascorbic acid": "vitamin_c_mg",
    "Vitamin D (D2 + D3)": "vitamin_d_mcg",
    "Vitamin E (alpha-tocopherol)": "vitamin_e_mg",
    "Vitamin K (phylloquinone)": "vitamin_k_mcg",
    "Thiamin": "vitamin_b1_mg",
    "Riboflavin": "vitamin_b2_mg",
    "Niacin": "vitamin_b3_mg",
    "Pantothenic acid": "vitamin_b5_mg",
    "Vitamin B-6": "vitamin_b6_mg",
    "Biotin": "vitamin_b7_mcg",
    "Folate, total": "vitamin_b9_mcg",
    "Vitamin B-12": "vitamin_b12_mcg",
    "Phosphorus, P": "phosphorus_mg",
    "Selenium, Se": "selenium_mcg",
    "Copper, Cu": "copper_mg",
    "Manganese, Mn": "manganese_mg",
    "Caffeine": "caffeine_mg",
    "Fatty acids, total monounsaturated": "monounsaturated_fat_g",
    "Fatty acids, total polyunsaturated": "polyunsaturated_fat_g",
    "SFA 18:0": "stearic_acid_g",
    "PUFA 18:2": "omega_6_g",
    "PUFA 18:3": "omega_3_ala_g",
    "PUFA 20:5 n-3 (EPA)": "omega_3_epa_g",
    "PUFA 22:6 n-3 (DHA)": "omega_3_dha_g",
}

_data_cache = None

def load_data():
    global _data_cache
    if _data_cache is None:
        with open(DATA_FILE) as f:
            _data_cache = json.load(f)["FoundationFoods"]
    return _data_cache

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def search_foods(query: str, limit: int = 10) -> list:
    """Search foods by name with improved matching.

    Scoring prioritizes:
    1. Exact matches
    2. Word boundary matches (query words match whole words in description)
    3. All query words present (substring)
    4. Fuzzy matches (for single-word queries)
    5. Partial word matches
    """
    foods = load_data()
    query_lower = query.lower()
    query_words = query_lower.split()

    scored = []
    for food in foods:
        desc = food["description"].lower()
        desc_words = re.split(r'[\s,]+', desc)

        # Exact match scores highest
        if query_lower == desc:
            score = 10000
        # Check for word boundary matches
        elif all(w in desc_words for w in query_words):
            # All query words match whole words in description
            score = 1000 - len(desc)  # Prefer shorter matches
        # All words present as substrings
        elif all(w in desc for w in query_words):
            score = 100 - len(desc)
        # Fuzzy matching for single-word queries
        elif len(query_words) == 1:
            min_dist = min(levenshtein_distance(query_lower, dw) for dw in desc_words)
            # Allow fuzzy match if distance is small relative to word length
            if min_dist <= max(2, len(query_lower) // 3):
                score = 50 - min_dist * 5 - len(desc) / 100
            # Check if any query word is a substring match
            elif any(w in desc for w in query_words):
                score = 10 - len(desc) / 100
            else:
                continue
        # Any word present
        elif any(w in desc for w in query_words):
            score = 10 - len(desc) / 100
        else:
            continue

        scored.append((score, food))

    scored.sort(key=lambda x: -x[0])
    return [f for _, f in scored[:limit]]

def extract_nutrients(food: dict) -> dict:
    """Extract nutrient values mapped to our CSV columns."""
    result = {
        "food_name": food["description"],
        "fdcId": food["fdcId"],
    }

    for fn in food.get("foodNutrients", []):
        nutrient = fn.get("nutrient", {})
        name = nutrient.get("name", "")
        amount = fn.get("amount")

        if amount is None:
            continue

        # Handle Energy specially - we want kcal
        if name == "Energy":
            unit = nutrient.get("unitName", "")
            if unit == "kcal":
                result["calories"] = round(amount, 1)
        elif name in NUTRIENT_MAP:
            col = NUTRIENT_MAP[name]
            result[col] = round(amount, 3)

    return result

def get_portions(food: dict) -> list:
    """Get portion size options for a food."""
    portions = []
    for p in food.get("foodPortions", []):
        name = p.get("portionDescription") or p.get("measureUnit", {}).get("name", "portion")
        grams = p.get("gramWeight")
        if grams:
            portions.append({"name": name, "grams": round(grams, 1)})
    return portions

def main():
    parser = argparse.ArgumentParser(description="Search USDA food database")
    parser.add_argument("query", nargs="?", help="Food to search for")
    parser.add_argument("--id", type=int, help="Look up by FDC ID")
    parser.add_argument("--limit", type=int, default=5, help="Max results")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--portions", action="store_true", help="Include portion sizes")

    args = parser.parse_args()

    if not args.query and not args.id:
        parser.print_help()
        return

    if args.id:
        foods = load_data()
        matches = [f for f in foods if f["fdcId"] == args.id]
    else:
        matches = search_foods(args.query, args.limit)

    if not matches:
        print(f"No foods found matching '{args.query or args.id}'")
        return

    results = []
    for food in matches:
        nutrients = extract_nutrients(food)
        if args.portions:
            nutrients["portions"] = get_portions(food)
        results.append(nutrients)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"\n{r['food_name']} (FDC ID: {r['fdcId']})")
            print("-" * 40)

            # Print macros first
            macros = ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g"]
            for m in macros:
                if m in r:
                    print(f"  {m}: {r[m]}")

            # Then other nutrients
            print("  ---")
            for k, v in sorted(r.items()):
                if k not in macros and k not in ["food_name", "fdcId", "portions"]:
                    print(f"  {k}: {v}")

            if args.portions and "portions" in r:
                print("  ---")
                print("  Portions:")
                for p in r["portions"]:
                    print(f"    {p['name']}: {p['grams']}g")

if __name__ == "__main__":
    main()

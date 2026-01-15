#!/usr/bin/env python3
"""Unified nutrition lookup - searches USDA and Open Food Facts databases.

This script provides a single interface to search multiple nutrition databases:
- USDA Foundation Foods (bundled, ~365 whole foods)
- Open Food Facts (online, millions of packaged products, barcodes)

Prioritizes USDA for whole foods, Open Food Facts for branded/packaged items.
"""

import argparse
import json
import sys
from pathlib import Path

# Import the individual lookup modules
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

import lookup_usda
import lookup_openfoodfacts as off


def search_all(query: str, limit: int = 5, source: str = None, country: str = None) -> list:
    """Search all available databases.

    Args:
        query: Search terms
        limit: Max results per source (default 5)
        source: Limit to specific source ('usda' or 'off')
        country: Country filter for Open Food Facts

    Returns:
        List of results with source information
    """
    results = []

    # Search USDA first (local, faster, better for whole foods)
    if source in (None, "usda"):
        try:
            usda_results = lookup_usda.search_foods(query, limit)
            for food in usda_results:
                nutrients = lookup_usda.extract_nutrients(food)
                nutrients["source"] = "usda"
                nutrients["portions"] = lookup_usda.get_portions(food)
                results.append(nutrients)
        except Exception as e:
            print(f"USDA search error: {e}", file=sys.stderr)

    # Then search Open Food Facts (online, slower, but millions of products)
    if source in (None, "off"):
        try:
            off_results = off.search_by_text(query, limit, country)
            for product in off_results:
                nutrients = off.extract_nutrients(product)
                results.append(nutrients)
        except Exception as e:
            print(f"Open Food Facts search error: {e}", file=sys.stderr)

    return results


def lookup_barcode(barcode: str) -> dict:
    """Look up a product by barcode."""
    product = off.search_by_barcode(barcode)
    if product:
        return off.extract_nutrients(product)
    return None


def lookup_usda_id(fdc_id: int) -> dict:
    """Look up a USDA food by FDC ID."""
    foods = lookup_usda.load_data()
    for food in foods:
        if food["fdcId"] == fdc_id:
            nutrients = lookup_usda.extract_nutrients(food)
            nutrients["source"] = "usda"
            nutrients["portions"] = lookup_usda.get_portions(food)
            return nutrients
    return None


def format_result(r: dict, show_portions: bool = False) -> str:
    """Format a result for display."""
    lines = []

    name = r["food_name"]
    if r.get("brand"):
        name = f"{r['brand']} - {name}"
    if r.get("quantity"):
        name = f"{name} ({r['quantity']})"

    source_label = "USDA" if r.get("source") == "usda" else "OFF"
    id_info = f"FDC:{r['fdcId']}" if r.get("fdcId") else f"BC:{r.get('barcode', 'N/A')}"

    lines.append(f"\n{name}")
    lines.append(f"[{source_label}] {id_info}")
    if r.get("nutriscore"):
        lines.append(f"Nutri-Score: {r['nutriscore']}")
    lines.append("-" * 40)

    # Macros first
    macros = ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g"]
    for m in macros:
        if m in r:
            lines.append(f"  {m}: {r[m]}")

    # Other nutrients
    lines.append("  ---")
    skip = {"food_name", "fdcId", "barcode", "brand", "quantity", "source", "nutriscore", "portions"} | set(macros)
    for k, v in sorted(r.items()):
        if k not in skip:
            lines.append(f"  {k}: {v}")

    # Portions
    if show_portions and r.get("portions"):
        lines.append("  ---")
        lines.append("  Portions:")
        for p in r["portions"]:
            lines.append(f"    {p['name']}: {p['grams']}g")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search USDA and Open Food Facts for nutrition info",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "chicken breast"                  # Search both databases
  %(prog)s "gruyere" --country switzerland   # Include Swiss products
  %(prog)s --barcode 3017620422003           # Look up by barcode
  %(prog)s --id 171705                       # Look up by USDA FDC ID
  %(prog)s "eggs" --source usda              # Only search USDA
  %(prog)s "nutella" --source off            # Only search Open Food Facts
        """
    )
    parser.add_argument("query", nargs="?", help="Food to search for")
    parser.add_argument("--barcode", "-b", help="Look up by barcode (EAN/UPC)")
    parser.add_argument("--id", type=int, help="Look up by USDA FDC ID")
    parser.add_argument("--source", "-s", choices=["usda", "off"], help="Search only this source")
    parser.add_argument("--country", "-c", help="Country filter for Open Food Facts")
    parser.add_argument("--limit", type=int, default=5, help="Max results per source (default 5)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--portions", action="store_true", help="Include portion sizes (USDA only)")

    args = parser.parse_args()

    if not args.query and not args.barcode and not args.id:
        parser.print_help()
        return

    results = []

    if args.barcode:
        result = lookup_barcode(args.barcode)
        if result:
            results = [result]
        else:
            print(f"No product found with barcode: {args.barcode}")
            return
    elif args.id:
        result = lookup_usda_id(args.id)
        if result:
            results = [result]
        else:
            print(f"No food found with USDA FDC ID: {args.id}")
            return
    else:
        results = search_all(args.query, args.limit, args.source, args.country)
        if not results:
            print(f"No foods found matching: {args.query}")
            return

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(format_result(r, args.portions))


if __name__ == "__main__":
    main()

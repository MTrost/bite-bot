#!/usr/bin/env python3
"""Search Open Food Facts database for nutritional information.

Open Food Facts is a free, open database with millions of food products
from around the world, including European foods, barcodes, and branded items.
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
from typing import Optional

BASE_URL = "https://world.openfoodfacts.org"
USER_AGENT = "BiteBot/1.0 (nutrition-tracker)"

# Map Open Food Facts nutrient fields to our CSV columns
NUTRIENT_MAP = {
    "energy-kcal_100g": "calories",
    "proteins_100g": "protein_g",
    "carbohydrates_100g": "carbs_g",
    "fiber_100g": "fiber_g",
    "sugars_100g": "sugar_g",
    "fat_100g": "fat_g",
    "saturated-fat_100g": "saturated_fat_g",
    "trans-fat_100g": "trans_fat_g",
    "cholesterol_100g": "cholesterol_mg",
    "sodium_100g": "sodium_mg",
    "potassium_100g": "potassium_mg",
    "calcium_100g": "calcium_mg",
    "iron_100g": "iron_mg",
    "magnesium_100g": "magnesium_mg",
    "zinc_100g": "zinc_mg",
    "vitamin-a_100g": "vitamin_a_mcg",
    "vitamin-c_100g": "vitamin_c_mg",
    "vitamin-d_100g": "vitamin_d_mcg",
    "vitamin-e_100g": "vitamin_e_mg",
    "vitamin-b1_100g": "vitamin_b1_mg",
    "vitamin-b2_100g": "vitamin_b2_mg",
    "vitamin-b6_100g": "vitamin_b6_mg",
    "vitamin-b12_100g": "vitamin_b12_mcg",
    "folates_100g": "vitamin_b9_mcg",
    "caffeine_100g": "caffeine_mg",
}


def fetch_url(url: str) -> dict:
    """Fetch JSON from URL with proper headers."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"status": 0, "products": []}
        raise
    except urllib.error.URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def search_by_barcode(barcode: str) -> Optional[dict]:
    """Look up a product by barcode (EAN/UPC)."""
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    data = fetch_url(url)

    if data.get("status") == 1 and "product" in data:
        return data["product"]
    return None


def search_by_text(query: str, limit: int = 10, country: str = None) -> list:
    """Search products by text query.

    Args:
        query: Search terms
        limit: Max results (default 10)
        country: Filter by country code (e.g., 'switzerland', 'germany', 'france')
    """
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": limit,
        "fields": "code,product_name,brands,quantity,nutriments,nutriscore_grade,categories_tags",
    }

    base = BASE_URL
    if country:
        # Use country-specific subdomain for better results
        country_codes = {
            "switzerland": "ch",
            "swiss": "ch",
            "germany": "de",
            "german": "de",
            "france": "fr",
            "french": "fr",
            "italy": "it",
            "italian": "it",
            "uk": "uk",
            "united kingdom": "uk",
            "us": "us",
            "usa": "us",
        }
        code = country_codes.get(country.lower(), country.lower())
        base = f"https://{code}.openfoodfacts.org"

    url = f"{base}/cgi/search.pl?" + urllib.parse.urlencode(params)
    data = fetch_url(url)

    return data.get("products", [])


def extract_nutrients(product: dict) -> dict:
    """Extract nutrient values mapped to our CSV columns."""
    nutriments = product.get("nutriments", {})

    result = {
        "food_name": product.get("product_name", "Unknown"),
        "barcode": product.get("code", ""),
        "brand": product.get("brands", ""),
        "quantity": product.get("quantity", ""),
        "source": "openfoodfacts",
    }

    # Add nutriscore if available
    if product.get("nutriscore_grade"):
        result["nutriscore"] = product["nutriscore_grade"].upper()

    # Extract nutrients - values are per 100g
    for off_key, our_key in NUTRIENT_MAP.items():
        value = nutriments.get(off_key)
        if value is not None:
            try:
                result[our_key] = round(float(value), 3)
            except (ValueError, TypeError):
                pass

    # Handle sodium -> mg conversion if stored in g
    if "sodium_mg" not in result and "sodium_100g" in nutriments:
        try:
            # OFF stores sodium in g, we want mg
            result["sodium_mg"] = round(float(nutriments["sodium_100g"]) * 1000, 1)
        except (ValueError, TypeError):
            pass

    return result


def format_product(product: dict, show_json: bool = False) -> str:
    """Format a product for display."""
    nutrients = extract_nutrients(product)

    if show_json:
        return json.dumps(nutrients, indent=2)

    lines = []
    name = nutrients["food_name"]
    if nutrients.get("brand"):
        name = f"{nutrients['brand']} - {name}"
    if nutrients.get("quantity"):
        name = f"{name} ({nutrients['quantity']})"

    lines.append(f"\n{name}")
    if nutrients.get("barcode"):
        lines.append(f"Barcode: {nutrients['barcode']}")
    if nutrients.get("nutriscore"):
        lines.append(f"Nutri-Score: {nutrients['nutriscore']}")
    lines.append("-" * 40)

    # Macros first
    macros = ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g"]
    for m in macros:
        if m in nutrients:
            lines.append(f"  {m}: {nutrients[m]}")

    # Then other nutrients
    lines.append("  ---")
    skip = {"food_name", "barcode", "brand", "quantity", "source", "nutriscore"} | set(macros)
    for k, v in sorted(nutrients.items()):
        if k not in skip:
            lines.append(f"  {k}: {v}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search Open Food Facts database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "greek yogurt"                    # Search by name
  %(prog)s --barcode 7613035844674           # Look up by barcode
  %(prog)s "gruyere" --country switzerland   # Search Swiss products
  %(prog)s "nutella" --json                  # Output as JSON
        """
    )
    parser.add_argument("query", nargs="?", help="Food to search for")
    parser.add_argument("--barcode", "-b", help="Look up by barcode (EAN/UPC)")
    parser.add_argument("--country", "-c", help="Filter by country (e.g., switzerland, germany)")
    parser.add_argument("--limit", type=int, default=5, help="Max results (default 5)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.query and not args.barcode:
        parser.print_help()
        return

    results = []

    if args.barcode:
        product = search_by_barcode(args.barcode)
        if product:
            results = [product]
        else:
            print(f"No product found with barcode: {args.barcode}")
            return
    else:
        results = search_by_text(args.query, args.limit, args.country)
        if not results:
            print(f"No products found matching: {args.query}")
            return

    if args.json:
        output = [extract_nutrients(p) for p in results]
        print(json.dumps(output, indent=2))
    else:
        for product in results:
            print(format_product(product))


if __name__ == "__main__":
    main()

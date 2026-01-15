# Look Up Nutritional Information

Find accurate nutritional data for foods using multiple databases.

## Available Data Sources

1. **USDA Foundation Foods** (local) - ~365 whole foods, high accuracy
2. **Open Food Facts** (online) - Millions of packaged products, barcodes, European foods

## Unified Lookup (Recommended)

Search both databases at once:

```bash
python3 scripts/lookup_nutrition.py "food name"
```

Options:
- `--limit N` - Max results per source (default 5)
- `--portions` - Include standard portion sizes (USDA only)
- `--json` - Output as JSON for easier parsing
- `--source usda|off` - Search only one database
- `--country NAME` - Filter Open Food Facts by country (e.g., switzerland, germany)

### Barcode Lookup

Look up packaged products by barcode (EAN/UPC):

```bash
python3 scripts/lookup_nutrition.py --barcode 3017620422003
```

### USDA ID Lookup

Look up by specific USDA FDC ID:

```bash
python3 scripts/lookup_nutrition.py --id 171705
```

## Individual Scripts

For specific databases only:

```bash
# USDA only (local, offline)
python3 scripts/lookup_usda.py "chicken breast" --portions

# Open Food Facts only (online, European foods, barcodes)
python3 scripts/lookup_openfoodfacts.py "gruyere" --country switzerland
python3 scripts/lookup_openfoodfacts.py --barcode 7613035844674
```

## Examples

```bash
# Search all databases
python3 scripts/lookup_nutrition.py "eggs" --limit 3

# Swiss cheeses and European foods
python3 scripts/lookup_nutrition.py "emmental" --country switzerland

# Packaged product by barcode
python3 scripts/lookup_nutrition.py --barcode 3017620422003

# Only local USDA data
python3 scripts/lookup_nutrition.py "salmon" --source usda --portions
```

## Scaling to Portion Size

Values are per 100g. To scale:
- Get the amount in grams
- Multiply each nutrient by (amount_g / 100)

Use `--portions` to see common serving sizes with gram weights (USDA only).

## Process

1. Search local USDA database first for whole foods
2. Search Open Food Facts for packaged/branded items
3. If user has a barcode, use barcode lookup
4. If no match or ambiguous, ask for clarification:
   - Preparation method (raw, cooked, fried)
   - Specific variety
   - Brand (for packaged foods)
5. Return breakdown with source noted

## What to Return

At minimum:
- Calories
- Protein (g)
- Carbohydrates (g)
- Fat (g)

If available:
- Fiber, sugar
- Saturated fat, trans fat
- Sodium, potassium
- Vitamins and minerals
- Nutri-Score (Open Food Facts)

## Handling Uncertainty

- If multiple matches, show options: "Did you mean X or Y?"
- If portion unclear, use standard serving from `--portions`
- For home-cooked meals, break into ingredients and sum
- Note the source (USDA vs Open Food Facts) in responses

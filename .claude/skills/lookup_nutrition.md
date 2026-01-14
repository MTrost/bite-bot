# Look Up Nutritional Information

Find accurate nutritional data for foods using the local USDA database.

## Primary Source: Local USDA Database

Use the lookup script to search Foundation Foods:

```bash
python3 scripts/lookup_usda.py "food name"
```

Options:
- `--limit N` - Return top N matches (default 5)
- `--portions` - Include standard portion sizes
- `--json` - Output as JSON for easier parsing
- `--id FDC_ID` - Look up by specific FDC ID

### Example

```bash
python3 scripts/lookup_usda.py "chicken breast" --portions
```

Returns per-100g nutrient values plus portion options.

## Fallback Sources (when not in USDA data)

1. **User-provided info** - Nutrition labels, specific values
2. **Brand websites** - For packaged/branded foods
3. **Web search** - Last resort, cite source

## Process

1. Search local USDA database first
2. If no match or ambiguous, ask for clarification:
   - Preparation method (raw, cooked, fried)
   - Specific variety
   - Brand (for packaged foods)
3. If not in USDA, fall back to other sources
4. Return breakdown with source noted

## Scaling to Portion Size

USDA values are per 100g. To scale:
- Get the amount in grams
- Multiply each nutrient by (amount_g / 100)

The `--portions` flag shows common serving sizes with gram weights.

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

## Handling Uncertainty

- If multiple matches, show options: "Did you mean X or Y?"
- If portion unclear, use standard serving from `--portions`
- For home-cooked meals, break into ingredients and sum

## Example Interaction

User: "One chicken breast"

```bash
python3 scripts/lookup_usda.py "chicken breast" --portions --json
```

Response: "A raw chicken breast with skin (FDC ID: 2727569) per 100g:
- Calories: not listed (estimate ~165 kcal)
- Protein: 21.4g
- Fat: 4.78g
- Carbs: ~0g

The USDA shows this without calorie data. A typical breast is ~175g.
Should I log 175g chicken breast?"

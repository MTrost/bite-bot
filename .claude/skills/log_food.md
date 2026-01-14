# Log Food Intake

Add a food entry to the intake log.

## Usage

When the user reports eating something, use this skill to log it.

## Preferred Method: Use USDA ID

If the food is in the USDA database, use `--usda-id` for automatic nutrient lookup and scaling:

```bash
# First find the food
python3 scripts/lookup_usda.py "chicken breast"

# Then log with the FDC ID - nutrients auto-populated
python3 scripts/log_entry.py \
  --food "Chicken breast" \
  --amount 175 \
  --usda-id 2727569
```

This stores the USDA ID so you can recalculate nutrients later if the amount changes.

## Manual Method

If USDA data isn't available (packaged foods, restaurant meals), provide values manually:

```bash
python3 scripts/log_entry.py \
  --food "FOOD_NAME" \
  --amount AMOUNT_IN_GRAMS \
  --calories CALORIES \
  --protein PROTEIN_G \
  --carbs CARBS_G \
  --fat FAT_G \
  [--fiber FIBER_G] \
  [--notes "OPTIONAL_NOTES"]
```

You can mix: use `--usda-id` for base values and override specific fields.

## Available Nutrient Flags

Macros: `--protein`, `--carbs`, `--fiber`, `--sugar`, `--fat`, `--saturated-fat`, `--trans-fat`

Minerals: `--cholesterol`, `--sodium`, `--potassium`, `--calcium`, `--iron`, `--magnesium`, `--phosphorus`, `--zinc`, `--copper`, `--manganese`, `--selenium`

Vitamins: `--vitamin-a`, `--vitamin-c`, `--vitamin-d`, `--vitamin-e`, `--vitamin-k`, `--vitamin-b1` through `--vitamin-b12`

Other: `--omega3`, `--omega6`, `--water`, `--caffeine`, `--alcohol`, `--notes`, `--timestamp`

## Example Workflow

User says: "I ate 150g of chicken breast"

```bash
# Look up in USDA
python3 scripts/lookup_usda.py "chicken breast" --portions

# Output shows FDC ID 2727569 for "Chicken, breast, meat and skin, raw"

# Log with USDA ID
python3 scripts/log_entry.py --food "Chicken breast" --amount 150 --usda-id 2727569
```

## Confirmation

After logging, tell the user what was recorded:
- Food name and amount
- Key macros (calories, protein, carbs, fat)
- Note if data came from USDA

# Log Food Intake

Add a food entry to the intake log.

## Usage

When the user reports eating something, use this skill to log it.

## Process

1. First, get nutritional data using the `lookup_nutrition` skill
2. Then run the logging script:

```bash
python3 scripts/log_entry.py \
  --food "FOOD_NAME" \
  --amount AMOUNT_IN_GRAMS \
  --calories CALORIES \
  --protein PROTEIN_G \
  --carbs CARBS_G \
  --fat FAT_G \
  [--fiber FIBER_G] \
  [--sugar SUGAR_G] \
  [--sodium SODIUM_MG] \
  [--notes "OPTIONAL_NOTES"] \
  [--timestamp "YYYY-MM-DDTHH:MM:SS"]
```

All micronutrient flags are optional. Only include what you have data for.

## Available Nutrient Flags

Macros: `--protein`, `--carbs`, `--fiber`, `--sugar`, `--fat`, `--saturated-fat`, `--trans-fat`

Minerals: `--cholesterol`, `--sodium`, `--potassium`, `--calcium`, `--iron`, `--magnesium`, `--phosphorus`, `--zinc`, `--copper`, `--manganese`, `--selenium`

Vitamins: `--vitamin-a`, `--vitamin-c`, `--vitamin-d`, `--vitamin-e`, `--vitamin-k`, `--vitamin-b1`, `--vitamin-b2`, `--vitamin-b3`, `--vitamin-b5`, `--vitamin-b6`, `--vitamin-b7`, `--vitamin-b9`, `--vitamin-b12`

Other: `--omega3`, `--omega6`, `--water`, `--caffeine`, `--alcohol`

## Example

User says: "I ate 150g of chicken breast"

After looking up nutrition:
```bash
python3 scripts/log_entry.py \
  --food "chicken breast, cooked" \
  --amount 150 \
  --calories 231 \
  --protein 43.5 \
  --carbs 0 \
  --fat 5 \
  --sodium 104
```

## Confirmation

After logging, tell the user what was recorded with the key macros.

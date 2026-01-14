# Daily Summary

Get aggregated nutritional totals for a specific day.

## Usage

When the user asks about their daily intake, what they've eaten today, or progress toward goals.

## Process

Run the summary script:

```bash
python3 scripts/daily_summary.py [--date YYYY-MM-DD]
```

If no date is provided, defaults to today.

## Output

The script returns:
- Total calories and macros
- Percentage of daily targets met
- List of foods logged that day
- Any nutrients significantly over/under target

## Presenting Results

1. **Lead with macros**: Calories, protein, carbs, fat
2. **Highlight concerns**: Anything <50% or >150% of target
3. **Skip the noise**: Don't list every micronutrient unless asked

## Example Output Format

"Today's intake (so far):
- Calories: 1,450 / 2,000 (73%)
- Protein: 95g / 50g (190%)
- Carbs: 120g / 250g (48%)
- Fat: 55g / 65g (85%)

Logged: chicken breast (150g), rice (200g), orange (1 medium), coffee (2 cups)

Notes: Protein is high, carbs are low. On track overall."

## Comparisons

If user asks "how am I doing this week", run the script for each day and aggregate, or use:

```bash
python3 scripts/daily_summary.py --range 7
```

This shows the last 7 days with averages.

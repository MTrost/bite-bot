# Weekly/Monthly Summary Skill

Use this skill to get longer-term nutritional analysis with trends and insights.

## When to use
- User asks for weekly, monthly, or multi-day summary
- User wants to see trends over time
- User asks about consistent nutrient gaps or excesses
- User wants to compare their intake to targets over a period

## Script usage

```bash
# Weekly summary (default: last 7 days)
python3 scripts/weekly_summary.py

# Custom number of days
python3 scripts/weekly_summary.py --days 14
python3 scripts/weekly_summary.py --days 30

# Include all micronutrients (not just macros)
python3 scripts/weekly_summary.py --days 7 --all-nutrients
```

## Output includes

1. **Daily Breakdown**: Quick view of each day's macros
2. **Daily Averages**: Average intake compared to targets
3. **Trends**: Whether key nutrients are increasing, decreasing, or stable
4. **Nutrient Gaps & Excesses**: Nutrients consistently below 70% or above 150% of target

## Example

```bash
# Get monthly summary with all nutrients
python3 scripts/weekly_summary.py --days 30 --all-nutrients
```

## Notes

- Requires at least 1 day of logged data
- Trend analysis requires at least 3 days of data
- Only days with logged entries are included in averages
- Targets are loaded from data/targets.csv

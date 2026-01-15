# Meal Templates Skill

Use this skill to manage and log common meals or recipes. Templates let users quickly log frequently eaten meal combinations.

## When to use
- User wants to save a common meal for future use
- User says they ate a meal they've previously saved (e.g., "I had my morning oatmeal")
- User wants to see available templates
- User wants to delete or modify a template

## Managing Templates

### List available templates
```bash
python3 scripts/manage_templates.py --list
```

### Add a new template
```bash
# Template with USDA IDs (preferred - auto-calculates nutrients)
python3 scripts/manage_templates.py --add "morning_oatmeal" --foods '[
  {"food_name": "Oats, uncooked", "amount_g": 50, "usda_fdc_id": 173904},
  {"food_name": "Milk, whole", "amount_g": 200, "usda_fdc_id": 746778},
  {"food_name": "Banana", "amount_g": 100, "usda_fdc_id": 173944},
  {"food_name": "Honey", "amount_g": 15, "usda_fdc_id": 169640}
]'

# Template without USDA IDs (manual nutrient entry when logging)
python3 scripts/manage_templates.py --add "protein_shake" --foods '[
  {"food_name": "Protein powder", "amount_g": 30},
  {"food_name": "Almond milk", "amount_g": 300},
  {"food_name": "Peanut butter", "amount_g": 15}
]'
```

### Get template details
```bash
python3 scripts/manage_templates.py --get "morning_oatmeal"
```

### Delete a template
```bash
python3 scripts/manage_templates.py --delete "morning_oatmeal"
```

## Logging from Templates

### Log a template (current time)
```bash
python3 scripts/log_template.py "morning_oatmeal"
```

### Log with custom timestamp
```bash
python3 scripts/log_template.py "morning_oatmeal" --timestamp "2026-01-15T07:30:00"
```

### Log with additional notes
```bash
python3 scripts/log_template.py "morning_oatmeal" --notes "Pre-workout meal"
```

## Template Format

Templates are stored in `data/templates.json` as:
```json
{
  "morning_oatmeal": {
    "description": "Template with 4 items",
    "foods": [
      {
        "food_name": "Oats, uncooked",
        "amount_g": 50,
        "usda_fdc_id": 173904
      },
      ...
    ]
  }
}
```

## Workflow Example

**User:** "I have the same breakfast every day - oats with banana and milk. Can you save that?"

**You:**
1. Look up USDA IDs for each food
2. Ask user for amounts
3. Create template with: `python3 scripts/manage_templates.py --add "morning_breakfast" --foods '[...]'`
4. Confirm template saved

**User:** "I had my morning breakfast"

**You:**
1. Use `python3 scripts/log_template.py "morning_breakfast"`
2. All items logged automatically

## Notes

- Templates with USDA IDs automatically populate nutrients when logged
- Templates without USDA IDs will need manual nutrient entry
- Each food in a template is logged as a separate entry in intake.csv
- Templates are saved per repository (not user-specific)

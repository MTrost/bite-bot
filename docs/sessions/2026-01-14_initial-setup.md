# Session: Initial Setup

**Date:** 2026-01-14
**Participants:** User (MTrost), Claude (Opus 4.5)

## Summary

Set up the core structure for Bite-bot, an AI-assisted macro/micronutrient tracking "app" where the LLM serves as the interface.

## Discussion

### Initial Concept

User's vision:
- Fork the repo, connect to an LLM
- Input food in any format (natural language, photos, voice)
- LLM breaks down input into nutrients and stores in CSV
- Interface is the chat itself, not a traditional app

User's initial requirements:
1. CSV database with header row (timestamp, food name, nutrients...)
2. CLAUDE.md to instruct LLM behavior
3. Skills for: looking up nutritional values, reading/writing CSV, calculations

### Claude's Honest Assessment

**Liked:**
- "LLM as interface" concept - natural language beats form-filling
- CSV + git is pragmatic - human-readable, version-controlled, no infrastructure
- Low barrier to entry

**Concerns raised:**
1. **Nutritional data accuracy** - LLMs have inconsistent knowledge. "One orange" - what size? Variance matters.
2. **LLMs are bad at math** - Summing daily totals needs scripts, not LLM arithmetic
3. **CSV schema** - Need to decide macros-only vs full micronutrients upfront

### Decisions Made

1. **Full nutrient tracking** - 40+ columns, users can choose what to track during setup
2. **Python scripts for calculations** - LLM calls scripts, doesn't do math
3. **Skills for structured operations** - log, lookup, summary, edit
4. **Never read full CSV directly** - Use scripts to aggregate/search to avoid context explosion

### USDA Database Integration

**Problem:** LLM guessing nutritional values is unreliable.

**Solution discussed:** Download USDA data directly instead of API calls.

**Implemented:**
- Downloaded USDA Foundation Foods (December 2025)
- 365 foods, 6.5MB JSON
- Created `lookup_usda.py` for local search
- Added `--usda-id` flag to auto-populate nutrients
- Store FDC ID for recalculation when amounts change

**Why JSON smaller than CSV:**
User asked good question - typically JSON is larger. Answer: USDA JSON is nested (nutrients under each food), CSV would be denormalized with massive repetition.

### Limitations Identified

**US-focused data:**
User is from Switzerland. Foundation Foods lacks:
- Swiss cheeses (Gruyère, Emmental, Appenzeller)
- European sausages (Cervelat, Bratwurst)
- Regional preparations

**Only 365 foods** - covers staples but not packaged/branded items.

### Future Work (documented in ISSUES.md)

1. Add European/Swiss nutritional database (naehrwertdaten.ch)
2. Expand beyond 365 foods (SR Legacy, Open Food Facts)
3. Improve food search/matching (fuzzy matching)
4. Barcode/photo support for packaged foods
5. Weekly/monthly summary reports
6. Meal templates ("morning oatmeal" = oats + milk + banana)

## Files Created

```
├── CLAUDE.md                 # LLM behavior instructions
├── CHANGELOG.md              # Version history
├── ISSUES.md                 # Future improvements
├── README.md                 # Updated with structure
├── data/
│   ├── intake.csv            # Food log (header only)
│   ├── targets.csv           # Daily nutritional targets
│   └── usda/
│       └── FoodData_Central_foundation_food_json_2025-12-18.json
├── scripts/
│   ├── log_entry.py          # Add entries (with --usda-id support)
│   ├── lookup_usda.py        # Search USDA database
│   ├── daily_summary.py      # Aggregate daily totals
│   ├── search_entries.py     # Find entries
│   ├── edit_entry.py         # Modify entries (with --recalculate)
│   └── delete_entry.py       # Remove entries
└── .claude/skills/
    ├── log_food.md
    ├── lookup_nutrition.md
    ├── daily_summary.md
    └── edit_entry.md
```

## Key Technical Details

### intake.csv Schema
- timestamp (ISO 8601)
- food_name
- amount_g
- usda_fdc_id (for recalculation)
- calories, protein_g, carbs_g, fat_g...
- 40+ nutrient columns total
- notes (free text)

### Workflow Example
```bash
# Search USDA
python3 scripts/lookup_usda.py "chicken breast" --portions

# Log with auto-nutrients
python3 scripts/log_entry.py --food "Chicken breast" --amount 175 --usda-id 2727569

# Later, change amount with recalculation
python3 scripts/edit_entry.py --id 2 --field amount_g --value 200 --recalculate
```

## Commits

1. `Set up macro tracking app structure` - Core files, scripts, skills
2. `Add local USDA nutritional database` - Foundation Foods, lookup script, recalculation
3. `Add ISSUES.md with planned improvements` - Future work documented

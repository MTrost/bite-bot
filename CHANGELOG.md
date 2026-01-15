# Changelog

All notable changes to Bite-bot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- **Enhanced food search algorithm** - Word boundary matching, fuzzy search (Levenshtein distance), improved relevance scoring
- **Weekly/monthly summary reports** (`scripts/weekly_summary.py`) - Trend analysis, nutrient gap detection, customizable time periods
- **Meal templates system** - Save and quickly log common meal combinations
  - `scripts/manage_templates.py` - Create, list, delete meal templates
  - `scripts/log_template.py` - Log all foods from a template at once
  - `.claude/skills/meal_templates.md` - Template management skill
  - `.claude/skills/weekly_summary.md` - Long-term analysis skill
  - Templates stored in `data/templates.json`
- **Local USDA nutritional database** - Foundation Foods dataset (365 foods) bundled in `data/usda/`
- **Nutritional lookup script** (`scripts/lookup_usda.py`) - Search foods, get per-100g values, portion sizes
- **Auto-population from USDA** - Use `--usda-id` flag in `log_entry.py` to auto-fetch and scale nutrients
- **Working recalculation** - `edit_entry.py --recalculate` now properly scales nutrients when amount changes
- **USDA FDC ID tracking** - New `usda_fdc_id` column in intake.csv enables recalculation
- **Core application structure**:
  - `CLAUDE.md` - LLM behavior instructions
  - `data/intake.csv` - Food log with 40+ nutrient columns
  - `data/targets.csv` - Customizable daily nutritional targets
  - Python scripts for all CSV operations (log, search, edit, delete, summary)
  - Skills in `.claude/skills/` for structured LLM operations
- `ISSUES.md` - Documented future improvements

### Improved
- Food search now prioritizes word boundaries (e.g., "egg" returns egg products, not eggplant)
- Fuzzy matching handles typos and misspellings
- Better scoring system for more relevant search results

### Data Sources
- USDA FoodData Central Foundation Foods (December 2025 release)

## [0.1.0] - 2026-01-14

### Added
- Initial project structure
- README with concept explanation

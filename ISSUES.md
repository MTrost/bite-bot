# Issues

## Recently Completed ✓

### ~~3. Improve food search/matching~~ ✓ Completed 2026-01-15

**Labels:** enhancement

Enhanced `lookup_usda.py` with:
- **Word boundary matching** - "egg" now correctly returns egg products, not eggplant
- **Fuzzy matching** - Handles typos using Levenshtein distance for single-word queries
- **Better scoring system** - Prioritizes exact matches, then word boundaries, then substrings
- Prefer shorter, more relevant matches

Implementation in: `scripts/lookup_usda.py:64-132`

---

### ~~5. Weekly/monthly summary reports~~ ✓ Completed 2026-01-15

**Labels:** enhancement, feature

Created `weekly_summary.py` script and skill with:
- Daily breakdown view
- Average daily intake with target comparison
- **Trend analysis** - Shows if nutrients are increasing, decreasing, or stable
- **Nutrient gap detection** - Flags consistently low (<70%) or high (>150%) nutrients
- Supports custom time periods (7, 14, 30 days, etc.)
- Optional all-nutrients view

Files added:
- `scripts/weekly_summary.py`
- `.claude/skills/weekly_summary.md`

---

### ~~6. Meal templates / recipes~~ ✓ Completed 2026-01-15

**Labels:** enhancement, feature

Implemented full meal template system:
- **Save common meals** - Store frequently eaten combinations
- **Quick logging** - Log entire meal with one command
- **Flexible format** - Supports both USDA IDs (auto-nutrients) and manual entry
- Template management (add, list, get, delete)

Files added:
- `scripts/manage_templates.py` - Create, list, delete templates
- `scripts/log_template.py` - Log all foods from a template
- `.claude/skills/meal_templates.md` - Usage guide

Templates stored in: `data/templates.json`

---

## Open Issues

Copy these to GitHub Issues when ready.

---

## 1. Add European/Swiss nutritional database

**Labels:** enhancement, data

### Problem
The current USDA Foundation Foods dataset is US-focused. Missing:
- Swiss cheeses (Gruyère, Emmental, Appenzeller, Raclette)
- European sausages (Cervelat, Bratwurst)
- Regional foods and preparations

### Potential sources
- **Swiss Food Composition Database** (Schweizer Nährwertdatenbank) - https://naehrwertdaten.ch/
- **German BLS** (Bundeslebensmittelschlüssel)
- **Open Food Facts** - crowdsourced, international coverage

### Implementation
- Download and integrate additional database(s)
- Update `lookup_usda.py` to search multiple sources (or create unified `lookup_nutrition.py`)
- Add source field to track where data came from

---

## 2. Expand food database beyond 365 items

**Labels:** enhancement, data

### Problem
USDA Foundation Foods only has 365 foods. Missing many common items.

### Options
- **USDA SR Legacy** - ~8,000 foods, older but more comprehensive
- **USDA Branded Foods** - 300k+ items but 3GB (too large to bundle)
- **Open Food Facts** - millions of products, crowdsourced

### Consideration
Trade-off between database size and repo size. Could offer download script instead of bundling.

---

## 3. Add barcode/packaging photo support

**Labels:** enhancement, feature

### Description
When user photographs food packaging:
1. Extract barcode or product name
2. Look up in Open Food Facts or similar
3. Auto-populate nutritional values

### Dependencies
- Requires vision-capable LLM
- Open Food Facts API or local database

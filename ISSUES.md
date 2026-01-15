# Issues

## Recently Completed ✓

### ~~1. Add European/Swiss nutritional database~~ ✓ Completed 2026-01-15

**Labels:** enhancement, data

Integrated Open Food Facts API with country-specific filtering:
- **International coverage** - Millions of products from around the world
- **Swiss/European foods** - Use `--country switzerland` (or germany, france, etc.)
- **Country-specific subdomains** - Routes to regional OFF databases for better results

Files added:
- `scripts/lookup_openfoodfacts.py` - Open Food Facts API integration
- `scripts/lookup_nutrition.py` - Unified lookup across all databases

Example: `python3 scripts/lookup_nutrition.py "gruyere" --country switzerland`

---

### ~~2. Expand food database beyond 365 items~~ ✓ Completed 2026-01-15

**Labels:** enhancement, data

Added Open Food Facts integration providing access to millions of products:
- **No bundling required** - Uses Open Food Facts API (online)
- **Unified search** - Single command searches both USDA and OFF
- **Source tracking** - Results show [USDA] or [OFF] labels

Files added:
- `scripts/lookup_openfoodfacts.py`
- `scripts/lookup_nutrition.py`

Updated: `.claude/skills/lookup_nutrition.md`

---

### ~~3. Add barcode/packaging photo support~~ ✓ Completed 2026-01-15

**Labels:** enhancement, feature

Implemented barcode lookup via Open Food Facts:
- **EAN/UPC support** - Look up any barcode in OFF database
- **Nutri-Score included** - Shows grade when available
- **Brand and quantity** - Displays product details

Usage:
```bash
python3 scripts/lookup_nutrition.py --barcode 3017620422003
# or
python3 scripts/lookup_openfoodfacts.py --barcode 3017620422003
```

Note: Photo/OCR extraction requires vision-capable LLM to read barcode from image first.

Files added:
- `scripts/lookup_openfoodfacts.py`
- `scripts/lookup_nutrition.py`

---

### ~~4. Improve food search/matching~~ ✓ Completed 2026-01-15

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

## 7. Add dedicated Swiss database integration

**Labels:** enhancement, data

### Problem
While Open Food Facts provides some Swiss products, the official Swiss Food Composition Database (Schweizer Nährwertdatenbank) at https://naehrwertdaten.ch/ has more accurate data for traditional Swiss foods.

### Potential sources
- **Swiss Food Composition Database** - Official government data
- **German BLS** (Bundeslebensmittelschlüssel) - Comprehensive German database

### Implementation
- Download official Swiss database
- Create `lookup_swiss.py` script
- Integrate into unified `lookup_nutrition.py`

---

## 8. Image recognition for meals

**Labels:** enhancement, feature

### Description
Allow users to photograph a meal and have it analyzed:
1. Vision LLM identifies food items in the photo
2. Estimates portions based on visual cues
3. Looks up nutrition and logs the meal

### Dependencies
- Requires multimodal LLM with vision capabilities
- Good portion estimation logic

---

## 9. Goal tracking and recommendations

**Labels:** enhancement, feature

### Description
Provide actionable recommendations based on intake patterns:
- Suggest foods to fill nutrient gaps
- Alert when approaching daily limits
- Weekly goal progress tracking

### Implementation
- Analyze weekly_summary data
- Build recommendation engine
- Add notification/alert system

# Open Issues

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

## 3. Improve food search/matching

**Labels:** enhancement

### Problem
Current search is basic substring matching. "egg" returns "Eggplant" before "Egg, whole".

### Improvements
- Fuzzy matching (Levenshtein distance)
- Word boundary preference
- Common name aliases ("chicken" → "Chicken, breast, boneless...")
- User's recent foods weighted higher

---

## 4. Add barcode/packaging photo support

**Labels:** enhancement, feature

### Description
When user photographs food packaging:
1. Extract barcode or product name
2. Look up in Open Food Facts or similar
3. Auto-populate nutritional values

### Dependencies
- Requires vision-capable LLM
- Open Food Facts API or local database

---

## 5. Weekly/monthly summary reports

**Labels:** enhancement, feature

### Description
Add skill/script for longer-term analysis:
- Average daily intake over period
- Trends (protein going up/down)
- Nutrients consistently under/over target
- Visual charts (if terminal supports)

---

## 6. Meal templates / recipes

**Labels:** enhancement, feature

### Description
Save common meals as templates:
```
"morning oatmeal" = oats 50g + milk 200ml + banana 100g + honey 15g
```

User says "I had my morning oatmeal" → logs all components.

### Implementation
- `data/templates.csv` or `data/recipes.json`
- New skill for managing templates

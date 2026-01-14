# Edit or Delete Entry

Modify or remove existing entries from the intake log.

## Usage

When the user needs to:
- Correct a mistake ("That should have been 200g not 100g")
- Delete an entry ("I didn't actually eat that")
- Update notes on an entry

## Finding Entries

First, search for the entry:

```bash
python3 scripts/search_entries.py --food "FOOD_NAME" [--date YYYY-MM-DD]
```

This returns matching entries with their row IDs.

## Editing

```bash
python3 scripts/edit_entry.py --id ROW_ID --field FIELD_NAME --value NEW_VALUE
```

Example: Change amount from 100g to 200g:
```bash
python3 scripts/edit_entry.py --id 42 --field amount_g --value 200
```

To recalculate nutrients after changing amount, use `--recalculate`:
```bash
python3 scripts/edit_entry.py --id 42 --field amount_g --value 200 --recalculate
```

## Deleting

```bash
python3 scripts/delete_entry.py --id ROW_ID
```

Always confirm before deleting: "Delete 'chicken breast (150g)' logged at 12:30? (y/n)"

## Process

1. Confirm which entry the user means (show them the match)
2. Confirm the change they want
3. Execute the edit/delete
4. Confirm what was changed

## Example Interaction

User: "Actually that orange was a large one, not medium"

1. Search: `python3 scripts/search_entries.py --food "orange" --date 2024-01-15`
2. Show: "Found: orange (130g) logged at 10:15. Update to large (184g)?"
3. User confirms
4. Edit: `python3 scripts/edit_entry.py --id 15 --field amount_g --value 184 --recalculate`
5. Confirm: "Updated orange to 184g. New calories: 87 (was 62)"

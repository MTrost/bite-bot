#!/usr/bin/env python3
"""Manage meal templates (recipes/common meals)."""

import argparse
import json
from pathlib import Path

TEMPLATES_FILE = Path(__file__).parent.parent / "data" / "templates.json"

def load_templates():
    """Load templates from JSON file"""
    if TEMPLATES_FILE.exists():
        with open(TEMPLATES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_templates(templates):
    """Save templates to JSON file"""
    TEMPLATES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TEMPLATES_FILE, "w") as f:
        json.dump(templates, f, indent=2)

def add_template(name, foods):
    """Add a new template

    Args:
        name: Template name (e.g., "morning_oatmeal")
        foods: List of dicts with 'food_name', 'amount_g', and optional 'usda_fdc_id'
    """
    templates = load_templates()
    templates[name] = {
        "foods": foods,
        "description": f"Template with {len(foods)} items"
    }
    save_templates(templates)
    print(f"Added template '{name}' with {len(foods)} foods")

def list_templates():
    """List all templates"""
    templates = load_templates()
    if not templates:
        print("No templates found. Create one with --add")
        return

    print(f"Available templates ({len(templates)}):\n")
    for name, data in templates.items():
        foods = data.get("foods", [])
        print(f"  {name}:")
        for food in foods:
            fdc = f" (FDC: {food['usda_fdc_id']})" if food.get('usda_fdc_id') else ""
            print(f"    - {food['food_name']}: {food['amount_g']}g{fdc}")
        print()

def get_template(name):
    """Get a specific template"""
    templates = load_templates()
    if name not in templates:
        print(f"Template '{name}' not found")
        return None
    return templates[name]

def delete_template(name):
    """Delete a template"""
    templates = load_templates()
    if name not in templates:
        print(f"Template '{name}' not found")
        return False

    del templates[name]
    save_templates(templates)
    print(f"Deleted template '{name}'")
    return True

def main():
    parser = argparse.ArgumentParser(description="Manage meal templates")
    parser.add_argument("--list", action="store_true", help="List all templates")
    parser.add_argument("--get", type=str, help="Get template details by name")
    parser.add_argument("--add", type=str, help="Add new template (name)")
    parser.add_argument("--foods", type=str, help="Foods JSON for --add: [{\"food_name\": \"...\", \"amount_g\": 100}]")
    parser.add_argument("--delete", type=str, help="Delete template by name")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.list:
        if args.json:
            templates = load_templates()
            print(json.dumps(templates, indent=2))
        else:
            list_templates()

    elif args.get:
        template = get_template(args.get)
        if template:
            if args.json:
                print(json.dumps(template, indent=2))
            else:
                print(f"\nTemplate: {args.get}")
                for food in template.get("foods", []):
                    fdc = f" (FDC: {food['usda_fdc_id']})" if food.get('usda_fdc_id') else ""
                    print(f"  - {food['food_name']}: {food['amount_g']}g{fdc}")

    elif args.add:
        if not args.foods:
            print("Error: --foods required with --add")
            print("Example: --foods '[{\"food_name\": \"Oats\", \"amount_g\": 50, \"usda_fdc_id\": 173904}]'")
            return

        try:
            foods = json.loads(args.foods)
            if not isinstance(foods, list):
                print("Error: --foods must be a JSON array")
                return

            # Validate each food has required fields
            for food in foods:
                if "food_name" not in food or "amount_g" not in food:
                    print("Error: Each food must have 'food_name' and 'amount_g'")
                    return

            add_template(args.add, foods)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")

    elif args.delete:
        delete_template(args.delete)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

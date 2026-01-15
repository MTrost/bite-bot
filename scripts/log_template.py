#!/usr/bin/env python3
"""Log all foods from a meal template."""

import argparse
import json
import subprocess
from pathlib import Path
from datetime import datetime

TEMPLATES_FILE = Path(__file__).parent.parent / "data" / "templates.json"
LOG_SCRIPT = Path(__file__).parent / "log_entry.py"

def load_templates():
    """Load templates from JSON file"""
    if TEMPLATES_FILE.exists():
        with open(TEMPLATES_FILE, "r") as f:
            return json.load(f)
    return {}

def log_template(template_name, timestamp=None, notes=None):
    """Log all foods from a template

    Args:
        template_name: Name of the template to log
        timestamp: Optional timestamp (ISO format), defaults to now
        notes: Optional notes to add to each entry
    """
    templates = load_templates()

    if template_name not in templates:
        print(f"Error: Template '{template_name}' not found")
        print("\nAvailable templates:")
        for name in templates.keys():
            print(f"  - {name}")
        return False

    template = templates[template_name]
    foods = template.get("foods", [])

    if not foods:
        print(f"Error: Template '{template_name}' has no foods")
        return False

    # Use provided timestamp or current time
    if not timestamp:
        timestamp = datetime.now().isoformat(timespec="seconds")

    print(f"Logging template '{template_name}' ({len(foods)} items)...\n")

    # Log each food
    success_count = 0
    for food in foods:
        food_name = food["food_name"]
        amount_g = food["amount_g"]
        usda_fdc_id = food.get("usda_fdc_id")

        # Build command
        cmd = [
            "python3", str(LOG_SCRIPT),
            food_name,
            "--amount", str(amount_g),
            "--timestamp", timestamp
        ]

        if usda_fdc_id:
            cmd.extend(["--usda-id", str(usda_fdc_id)])

        if notes:
            combined_notes = f"{template_name} - {notes}"
            cmd.extend(["--notes", combined_notes])
        else:
            cmd.extend(["--notes", f"Template: {template_name}"])

        # Run log_entry.py
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✓ {food_name} ({amount_g}g)")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to log {food_name}: {e.stderr}")

    print(f"\nLogged {success_count}/{len(foods)} items from '{template_name}'")
    return success_count == len(foods)

def main():
    parser = argparse.ArgumentParser(description="Log meal from template")
    parser.add_argument("template", help="Template name to log")
    parser.add_argument("--timestamp", type=str, help="Timestamp (ISO format, default: now)")
    parser.add_argument("--notes", type=str, help="Additional notes")

    args = parser.parse_args()

    log_template(args.template, args.timestamp, args.notes)

if __name__ == "__main__":
    main()

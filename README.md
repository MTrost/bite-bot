# Bite-bot

AI-assisted macro and micronutrient tracker. The interface is natural language - just tell the LLM what you ate.

## How It Works

1. Fork this repo
2. Connect to an LLM (Claude Code, etc.)
3. Log food in natural language in writing or speech: "I had two eggs and toast for breakfast", or just send a picture
4. The LLM looks up nutritional data, logs it to CSV, tracks against your goals

## Structure

```
├── CLAUDE.md              # LLM behavior instructions
├── data/
│   ├── intake.csv         # Food log (your data)
│   └── targets.csv        # Daily nutritional targets
├── scripts/               # CSV operations (called by LLM)
│   ├── log_entry.py
│   ├── daily_summary.py
│   ├── search_entries.py
│   ├── edit_entry.py
│   └── delete_entry.py
└── .claude/skills/        # Skill definitions
    ├── log_food.md
    ├── lookup_nutrition.md
    ├── daily_summary.md
    └── edit_entry.md
```

## Setup

1. Edit `data/targets.csv` to match your nutritional goals. Ask the LLM to do it!
2. Start chatting: "Log 200g chicken breast for lunch"

## Example Interactions

- "I ate an orange"
- "What did I eat today?"
- "How's my protein intake this week?"
- "Delete that last entry, I didn't actually eat it"

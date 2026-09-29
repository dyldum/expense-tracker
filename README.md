# Expense Tracker

A small command-line tool for logging personal expenses and seeing where your money goes, broken down by category. Built as a Stage 1 project while working through Python fundamentals — functions, data structures, file I/O, and exception handling.

## Features

- Add expenses with a description, amount, and category
- View all logged expenses
- See totals grouped by category
- Find the single largest expense
- Data persists between runs via a local JSON file

## Requirements

- Python 3.8+
- No external dependencies — everything here uses the standard library

## Running it

```bash
python expense_tracker.py
```

You'll get a menu:

```
1. Add expense
2. View all expenses
3. View spending by category
4. Show largest expense
5. Save and exit
```

Expenses are saved to `expenses.json` in the same folder when you exit. If the file doesn't exist yet, it's created automatically on first save.

## Running the tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```
expense-tracker/
├── expense_tracker.py       # main program
├── tests/
│   └── test_expense_tracker.py
├── .gitignore
└── README.md
```

## Notes on design choices

- Categories are restricted to a fixed set (`Food`, `Transport`, `Entertainment`, `Bills`, `Other`) rather than free text, mainly so the category totals stay meaningful and don't end up with ten variations of "food"/"Food"/"FOOD".
- A custom `InvalidAmountError` is used instead of a generic `ValueError` for negative/zero amounts — it made more sense to distinguish "bad number format" from "technically a number but not a valid amount" when handling input.
- `load_expenses` returns an empty list rather than raising if the JSON file doesn't exist or is corrupted, since the program should still be usable on a first run with no existing data.

## Possible extensions

- Filter expenses by date range (would need a `date` field added when logging)
- Export a summary to CSV
- Swap the JSON file for a proper SQLite database once the file gets large

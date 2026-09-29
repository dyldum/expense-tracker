"""
Simple command-line expense tracker.

Stores expenses in a JSON file and lets the user add expenses,
view them, and see totals broken down by category.
"""

import json
import os


VALID_CATEGORIES = {"Food", "Transport", "Entertainment", "Bills", "Other"}
DEFAULT_FILE = "expenses.json"


class InvalidAmountError(Exception):
    """Raised when an expense amount is zero or negative."""
    pass


def load_expenses(filename=DEFAULT_FILE):
    """Load expenses from a JSON file. Returns an empty list if the file doesn't exist yet."""
    if not os.path.exists(filename):
        return []

    with open(filename, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # file exists but is empty or corrupted - don't crash, just start fresh
            return []


def save_expenses(expenses, filename=DEFAULT_FILE):
    with open(filename, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses, description, amount, category):
    if amount <= 0:
        raise InvalidAmountError(f"Amount must be positive, got {amount}")

    if category not in VALID_CATEGORIES:
        raise ValueError(f"Category must be one of {VALID_CATEGORIES}")

    expenses.append({
        "description": description,
        "amount": amount,
        "category": category,
    })
    return expenses


def total_by_category(expenses):
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def largest_expense(expenses):
    if not expenses:
        return None
    return max(expenses, key=lambda e: e["amount"])


def filter_above(expenses, threshold):
    return [e for e in expenses if e["amount"] > threshold]


def prompt_for_amount():
    """Keep asking until the user enters a valid, positive number."""
    while True:
        raw = input("Amount: £")
        try:
            amount = float(raw)
        except ValueError:
            print("That's not a valid number, try again.")
            continue

        if amount <= 0:
            print("Amount has to be positive.")
            continue

        return amount


def prompt_for_category():
    while True:
        category = input(f"Category ({'/'.join(sorted(VALID_CATEGORIES))}): ").strip().title()
        if category in VALID_CATEGORIES:
            return category
        print(f"Not a valid category. Choose from: {', '.join(sorted(VALID_CATEGORIES))}")


def print_menu():
    print("\n1. Add expense")
    print("2. View all expenses")
    print("3. View spending by category")
    print("4. Show largest expense")
    print("5. Save and exit")


def main():
    expenses = load_expenses()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            description = input("Description: ").strip()
            amount = prompt_for_amount()
            category = prompt_for_category()
            add_expense(expenses, description, amount, category)
            print("Added.")

        elif choice == "2":
            if not expenses:
                print("No expenses yet.")
            for e in expenses:
                print(f"  {e['description']:<20} £{e['amount']:>8.2f}  ({e['category']})")

        elif choice == "3":
            totals = total_by_category(expenses)
            if not totals:
                print("No expenses yet.")
            for category, total in totals.items():
                print(f"  {category:<15} £{total:.2f}")

        elif choice == "4":
            biggest = largest_expense(expenses)
            if biggest is None:
                print("No expenses yet.")
            else:
                print(f"  {biggest['description']} - £{biggest['amount']:.2f}")

        elif choice == "5":
            save_expenses(expenses)
            print(f"Saved {len(expenses)} expenses to {DEFAULT_FILE}. Bye.")
            break

        else:
            print("Not a valid option, pick 1-5.")


if __name__ == "__main__":
    main()

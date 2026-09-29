import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from expense_tracker import (
    add_expense,
    total_by_category,
    largest_expense,
    filter_above,
    save_expenses,
    load_expenses,
    InvalidAmountError,
)


class TestAddExpense(unittest.TestCase):

    def test_adds_valid_expense(self):
        expenses = []
        add_expense(expenses, "Coffee", 3.50, "Food")
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["description"], "Coffee")

    def test_rejects_negative_amount(self):
        expenses = []
        with self.assertRaises(InvalidAmountError):
            add_expense(expenses, "Refund?", -5, "Food")

    def test_rejects_zero_amount(self):
        expenses = []
        with self.assertRaises(InvalidAmountError):
            add_expense(expenses, "Nothing", 0, "Food")

    def test_rejects_unknown_category(self):
        expenses = []
        with self.assertRaises(ValueError):
            add_expense(expenses, "Mystery", 10, "Not A Real Category")


class TestTotalByCategory(unittest.TestCase):

    def test_sums_correctly(self):
        expenses = [
            {"description": "Bus", "amount": 2.50, "category": "Transport"},
            {"description": "Train", "amount": 12.00, "category": "Transport"},
            {"description": "Pizza", "amount": 8.00, "category": "Food"},
        ]
        totals = total_by_category(expenses)
        self.assertEqual(totals["Transport"], 14.50)
        self.assertEqual(totals["Food"], 8.00)

    def test_empty_list_returns_empty_dict(self):
        self.assertEqual(total_by_category([]), {})


class TestLargestExpense(unittest.TestCase):

    def test_finds_the_biggest(self):
        expenses = [
            {"description": "Rent", "amount": 500, "category": "Bills"},
            {"description": "Snack", "amount": 2, "category": "Food"},
        ]
        biggest = largest_expense(expenses)
        self.assertEqual(biggest["description"], "Rent")

    def test_returns_none_when_empty(self):
        self.assertIsNone(largest_expense([]))


class TestFilterAbove(unittest.TestCase):

    def test_filters_correctly(self):
        expenses = [
            {"description": "Small", "amount": 5, "category": "Food"},
            {"description": "Big", "amount": 50, "category": "Bills"},
        ]
        result = filter_above(expenses, 10)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["description"], "Big")


class TestSaveAndLoad(unittest.TestCase):

    TEST_FILE = "test_expenses_temp.json"

    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_save_then_load_round_trip(self):
        expenses = [{"description": "Book", "amount": 15, "category": "Other"}]
        save_expenses(expenses, self.TEST_FILE)
        loaded = load_expenses(self.TEST_FILE)
        self.assertEqual(loaded, expenses)

    def test_load_missing_file_returns_empty_list(self):
        loaded = load_expenses("this_file_does_not_exist.json")
        self.assertEqual(loaded, [])


if __name__ == "__main__":
    unittest.main()

"""
Personal Expense Tracker
A menu-driven command-line application for recording and reviewing expenses.

Run:
    python expense_tracker.py

Data is stored in data/expenses.csv and remains available after the program closes.
"""

import csv
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


def ensure_data_file():
    """Create the data folder and CSV file with a header if needed."""
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=FIELDS).writeheader()


def load_expenses():
    """Return all saved expenses from the CSV file."""
    ensure_data_file()
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def get_amount():
    """Ask for a positive amount and reject invalid input."""
    while True:
        raw_amount = input("Amount (Rs.): ").strip()
        try:
            amount = float(raw_amount)
            if amount <= 0:
                print("Please enter an amount greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Invalid amount. Enter a number, for example 125.50.")


def add_expense():
    """Collect and save one expense."""
    print("\n--- Add Expense ---")
    category = input("Category (Food/Travel/Shopping/Bills/Other): ").strip()
    while not category:
        print("Category cannot be empty.")
        category = input("Category: ").strip()

    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    amount = get_amount()
    expense = {
        "date": date.today().isoformat(),
        "category": category.title(),
        "description": description,
        "amount": f"{amount:.2f}",
    }

    ensure_data_file()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=FIELDS).writerow(expense)

    print("Expense saved successfully.")


def view_expenses():
    """Display all saved expenses in a readable table."""
    expenses = load_expenses()
    print("\n--- All Expenses ---")
    if not expenses:
        print("No expenses found. Add an expense first.")
        return

    print(f"{'No.':<5}{'Date':<13}{'Category':<15}{'Description':<25}{'Amount (Rs.)':>14}")
    print("-" * 72)
    for number, item in enumerate(expenses, start=1):
        print(
            f"{number:<5}{item['date']:<13}{item['category']:<15}"
            f"{item['description'][:24]:<25}{float(item['amount']):>14.2f}"
        )


def total_expenditure():
    """Calculate and display total spending."""
    expenses = load_expenses()
    total = sum(float(item["amount"]) for item in expenses)
    print(f"\nTotal expenditure: Rs. {total:.2f}")


def expense_summary():
    """Show category-wise spending totals."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses available for a summary.")
        return

    totals = {}
    for item in expenses:
        category = item["category"]
        totals[category] = totals.get(category, 0) + float(item["amount"])

    print("\n--- Category-wise Summary ---")
    for category in sorted(totals):
        print(f"{category:<18} Rs. {totals[category]:.2f}")


def main():
    """Display the application menu until the user chooses Exit."""
    ensure_data_file()
    while True:
        print("\n========== PERSONAL EXPENSE TRACKER ==========")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenditure")
        print("4. Expense Summary")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expenditure()
        elif choice == "4":
            expense_summary()
        elif choice == "5":
            print("Thank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()

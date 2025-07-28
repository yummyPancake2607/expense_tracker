import json
import os
from datetime import datetime

# Function to load expenses from the JSON file
def load_expenses():
    if os.path.exists('expenses.json') and os.path.getsize('expenses.json') > 0:  # Check if file exists and is not empty
        with open('expenses.json', 'r') as file:
            return json.load(file)
    return []  # Return an empty list if the file is empty or doesn't exist

# Function to save expenses to the JSON file
def save_expenses(expenses):  # Fixed: Added 'expenses' parameter
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)

# Function to add a new expense with error handling
def add_expense(description, amount):
    # Check if description is empty
    if not description:
        print("Provide a description")
        return

    # Check if amount is valid (greater than 0)
    if amount <= 0:
        print("How are you printing -ve amount?")
        return

    # Load existing expenses from JSON file
    expenses = load_expenses()

    # Create the new expense
    expense = {
        "id": len(expenses) + 1,  # Generate new unique ID
        "date": str(datetime.now().date()),  # Current date
        "description": description,
        "amount": amount
    }

    # Add new expense to the list
    expenses.append(expense)

    # Save the updated list of expenses
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense['id']})")

# Function to list all expenses
def list_expenses():
    expenses = load_expenses()  # Fixed: Added parentheses to call load_expenses()
    if not expenses:
        print("No expenses found!")
    else:
        print("\nID  Date       Description  Amount")
        for expense in expenses:
            # Fixed: Corrected print formatting to use single quotes for keys
            print(f"{expense['id']}  {expense['date']}  {expense['description']}   ${expense['amount']}")

# Function to delete an expense by ID
def delete_expense(expense_id):
    expenses = load_expenses()

    # Find the expense by ID
    expense_to_delete = None
    for expense in expenses:
        if expense["id"] == expense_id:
            expense_to_delete = expense
            break

    if expense_to_delete:
        expenses.remove(expense_to_delete)
        save_expenses(expenses)
        print(f"Expense with ID {expense_id} deleted successfully.")
    else:
        print(f"Expense with ID {expense_id} not found.")

# Function to see summary of all expenses
def summary_expenses(month =None):
    expenses = load_expenses()
    total = 0
    if not expenses:
        print("No expeneses found!")
        return
    if month:
        filtered_expenses = [expense for expense in expenses if expense['date'].split('-')[1] == str(month).zfill(2)]
        if filtered_expenses:
            total = sum(expense['amount'] for expense in filtered_expenses)
            print(f"\nSummary for month {month}:")
            for expense in filtered_expenses:
                print(f"{expense['id']}  {expense['date']}  {expense['description']}   ${expense['amount']}")
            print(f"\nTotal for month {month}: ${total:.2f}")
        else:
            print(f"No expenses found for month {month}!")
    else:
        # Calculate the total for all expenses
        total = sum(expense['amount'] for expense in expenses)
        print("\nSummary of all expenses:")
        for expense in expenses:
            print(f"{expense['id']}  {expense['date']}  {expense['description']}   ${expense['amount']}")
        print(f"\nTotal expenses: ${total:.2f}")

# Main function to interact with the user
def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add expense")
        print("2. List expenses")
        print("3. Delete expense")
        print("4. Summary")
        print("5. Exit")

        try:
            # User chooses an option
            choice = input("Enter your choice (1/2/3/4/5): ")

            # Option 1: Add expense
            if choice == "1":
                description = input("Enter expense description: ")
                try:
                    amount = float(input("Enter expense amount: "))
                except ValueError:
                    print("Please provide a valid number for the amount.")
                    continue
                add_expense(description, amount)

            # Option 2: List expenses
            elif choice == "2":
                list_expenses()

            # Option 3: Delete expense
            elif choice == "3":
                try:
                    expense_id = int(input("Enter the ID of the expense to delete: "))
                    delete_expense(expense_id)
                except ValueError:
                    print("Please enter a valid integer ID.")

            # Option 4: View summary of expenses
            elif choice == "4":
                month_input = input("Enter the month to view summary (or press enter to view all): ")
                if month_input:
                    try:
                        month = int(month_input)
                        summary_expenses(month)
                    except ValueError:
                        print("Invalid month. Please enter a valid number.")
                else:
                    summary_expenses()

            # Option 5: Exit
            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid choice")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

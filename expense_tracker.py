import json
import os
from datetime import datetime

# Function to load expenses from the JSON file
def load_expenses():
    if os.path.exists('expenses.json') and os.path.getsize('expenses.json') > 0:  # Check if file exists and is not empty
        with open('expenses.json', 'r') as file:
            return json.load(file)
    return {"expenses": [], "budget": {}}  # Return an empty list and budget dictionary if the file is empty or doesn't exist

# Function to save expenses to the JSON file
def save_expenses(expenses_data):  # Modified to take a dictionary that includes expenses and budget
    with open("expenses.json", "w") as file:
        json.dump(expenses_data, file, indent=4)

# Function to add a new expense with error handling
def add_expense(description, amount, category, month):
    # Check if description is empty
    if not description:
        print("Provide a description")
        return

    # Check if amount is valid (greater than 0)
    if amount <= 0:
        print("How are you printing -ve amount?")
        return

    # Load existing expenses and budget from JSON file
    data = load_expenses()
    expenses = data["expenses"]
    budget = data["budget"]

    # Check if the current month's expense exceeds the budget
    if month in budget and (sum(expense['amount'] for expense in expenses if expense['date'].split('-')[1] == str(month).zfill(2)) + amount) > budget[month]:
        print(f"Warning: You are exceeding your budget for month {month}!")
        return

    # Create the new expense
    expense = {
        "id": len(expenses) + 1,  # Generate new unique ID
        "date": str(datetime.now().date()),  # Current date
        "description": description,
        "amount": amount,
        "category": category
    }

    # Add new expense to the list
    expenses.append(expense)

    # Save the updated list of expenses and the budget
    data["expenses"] = expenses
    save_expenses(data)
    print(f"Expense added successfully (ID: {expense['id']})")

# Function to list all expenses, with optional category filter
def list_expenses(category=None):
    expenses_data = load_expenses()
    expenses = expenses_data["expenses"]

    if not expenses:
        print("No expenses found!")
        return

    # If a category is provided, filter the expenses
    if category:
        expenses = [expense for expense in expenses if expense['category'].lower() == category.lower()]

    if not expenses:
        print(f"No expenses found for category '{category}'!")
        return

    # Printing the formatted list of expenses
    print("\nID   Date       Description  Amount  Category")
    print("-" * 50)  # Line separator for better readability
    for expense in expenses:
        print(f"{expense['id']: <5} {expense['date']}  {expense['description']: <15} ${expense['amount']: >7.2f}  {expense['category']}")

# Function to delete an expense by ID
def delete_expense(expense_id):
    expenses_data = load_expenses()
    expenses = expenses_data["expenses"]

    # Find the expense by ID
    expense_to_delete = None
    for expense in expenses:
        if expense["id"] == expense_id:
            expense_to_delete = expense
            break

    if expense_to_delete:
        expenses.remove(expense_to_delete)
        expenses_data["expenses"] = expenses
        save_expenses(expenses_data)
        print(f"Expense with ID {expense_id} deleted successfully.")
    else:
        print(f"Expense with ID {expense_id} not found.")

# Function to see summary of all expenses or by category, with budget info
def summary_expenses(month=None, category=None):
    expenses_data = load_expenses()
    expenses = expenses_data["expenses"]
    budget = expenses_data["budget"]
    total = 0
    if not expenses:
        print("No expenses found!")
        return

    # Filter by month if provided
    if month:
        expenses = [expense for expense in expenses if expense['date'].split('-')[1] == str(month).zfill(2)]

    # Filter by category if provided
    if category:
        expenses = [expense for expense in expenses if expense['category'].lower() == category.lower()]

    if expenses:
        print("\nID   Date       Description  Amount  Category")
        print("-" * 50)
        for expense in expenses:
            print(f"{expense['id']: <5} {expense['date']}  {expense['description']: <15} ${expense['amount']: >7.2f}  {expense['category']}")
        total = sum(expense['amount'] for expense in expenses)
        if month:
            print(f"\nTotal for month {month}: ${total:.2f}")
        elif category:
            print(f"\nTotal for category {category}: ${total:.2f}")
        else:
            print(f"\nTotal expenses: ${total:.2f}")
    else:
        print(f"No expenses found for the given filters!")

    # Display budget for the month if available
    if month in budget:
        print(f"Budget for month {month}: ${budget[month]:.2f}")
        print(f"Remaining budget: ${budget[month] - total:.2f}")
    else:
        print(f"No budget set for month {month}.")

# Function to set a budget for a month
def set_budget(month, amount):
    expenses_data = load_expenses()
    budget = expenses_data["budget"]
    
    # Set or update the budget for the month
    budget[month] = amount
    expenses_data["budget"] = budget
    save_expenses(expenses_data)
    print(f"Budget for month {month} set to ${amount:.2f}")

# Main function to interact with the user
def main():
    while True:
        print("\nExpense Tracker")
        print("1. Add expense")
        print("2. List expenses")
        print("3. Delete expense")
        print("4. Summary")
        print("5. Set budget")
        print("6. Exit")

        try:
            # User chooses an option
            choice = input("Enter your choice (1/2/3/4/5/6): ")

            # Option 1: Add expense
            if choice == "1":
                description = input("Enter expense description: ")
                try:
                    amount = float(input("Enter expense amount: "))
                    category = input("Enter expense category (e.g., Food, Transport, Utilities): ")
                    month = input("Enter month (numeric): ")
                    add_expense(description, amount, category, month)
                except ValueError:
                    print("Please provide a valid number for the amount.")
                    continue

            # Option 2: List expenses
            elif choice == "2":
                category = input("Enter category to filter by (or press enter to list all): ")
                if category:
                    list_expenses(category)
                else:
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
                category_input = input("Enter category to view summary (or press enter to view all): ")
                if month_input:
                    try:
                        month = int(month_input)
                        summary_expenses(month, category_input)
                    except ValueError:
                        print("Invalid month. Please enter a valid number.")
                else:
                    summary_expenses(category=category_input)

            # Option 5: Set a budget for a month
            elif choice == "5":
                try:
                    month = input("Enter the month to set the budget for (numeric): ")
                    budget = float(input("Enter the budget amount: "))
                    set_budget(month, budget)
                except ValueError:
                    print("Invalid budget amount. Please enter a valid number.")

            # Option 6: Exit
            elif choice == "6":
                print("Exiting...")
                break

            else:
                print("Invalid choice")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

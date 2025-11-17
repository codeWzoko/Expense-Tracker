from database import DB
from expense_manager import ExpenseManager
from report import Report
from charts import Charts
import auth  # <-- Import the authentication module

def prompt_credentials():
    username = input("Username: ")
    password = input("Password: ")
    return username, password

def main():
    # Authentication step
    logged_in = False
    while not logged_in:
        print("\n--- Expense Tracker Authentication ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        action = input("Choose: ")
        if action == "1":
            username, password = prompt_credentials()
            if auth.login(username, password):
                print(f"Welcome, {username}!")
                logged_in = True
            else:
                print("❌ Login failed. Try again.")
        elif action == "2":
            username, password = prompt_credentials()
            if auth.register(username, password):
                print("✅ Registration successful!")
            else:
                print("❌ Username already exists.")
        elif action == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice!")

    db = DB()
    mgr = ExpenseManager(db)
    rep = Report(db)

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Report by Category (bar chart)")
        print("4. Report by Month (pie chart)")
        print("5. Logout & Exit")
        choice = input("Choose: ")

        if choice == "1":
            date = input("Date (YYYY-MM-DD): ")
            category = input("Category: ")
            amount = float(input("Amount: "))
            desc = input("Description: ")
            mgr.add_expense(date, category, amount, desc)
            print("✅ Expense added.")
        elif choice == "2":
            df = mgr.get_all()
            print(df)
        elif choice == "3":
            df = rep.total_by_category()
            Charts.bar_by_category(df)
        elif choice == "4":
            df = rep.total_by_month()
            Charts.pie_by_month(df)
        elif choice == "5":
            print("Logging out. Goodbye!")
            break
        else:
            print("Invalid choice!")

if _name_ == "_main_":
    main()
from datetime import datetime

class ExpenseManager:
    def __init__(self, db):
        self.db = db

    def add_expense(self, user, date, category, amount, description=""):
        if isinstance(date, str):
            date = datetime.fromisoformat(date).date()
        # NEW: Pass 'user' to db.insert_expense
        self.db.insert_expense(user.strip(), date, category.strip().title(), float(amount), description.strip())

    def get_all(self):
        # NOTE: This function is primarily for CLI or internal use. API uses filtered queries.
        return self.db.query("SELECT * FROM expenses ORDER BY date")
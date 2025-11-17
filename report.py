class Report:
    def __init__(self, db):
        self.db = db

    def total_by_category(self, user):
        # NEW: Filter by user
        return self.db.query("""
            SELECT category, SUM(amount) as total
            FROM expenses WHERE user = ? GROUP BY category ORDER BY total DESC
        """, params=(user,))

    def total_by_month(self, user):
        # NEW: Filter by user
        return self.db.query("""
            SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
            FROM expenses WHERE user = ? GROUP BY month ORDER BY month
        """, params=(user,))
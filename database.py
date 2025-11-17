# database.py - Please ensure this is the entire, correct content

import sqlite3
import pandas as pd

class DB:
    def __init__(self, path="expenses.db"):
        # Ensure expenses.db exists or is created
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                user TEXT NOT NULL  -- New column for user separation
            )
        """)
        self.conn.commit()

    # FIX: This function signature now correctly accepts 'user' as the first argument
    def insert_expense(self, user, date, category, amount, description=""): 
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO expenses (user, date, category, amount, description) 
            VALUES (?, ?, ?, ?, ?)
        """, (user, date, category, amount, description)) 
        self.conn.commit()

    def query(self, sql, params=()):
        # Utility function to run any SQL query and return a DataFrame
        return pd.read_sql_query(sql, self.conn, params=params, parse_dates=["date"])
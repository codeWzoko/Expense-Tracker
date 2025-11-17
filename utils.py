from datetime import datetime

def parse_date(date_str):
    return datetime.fromisoformat(date_str).date()

def format_currency(amount):
    return f"₹{amount:,.2f}"

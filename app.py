from flask import Flask, request, jsonify
from database import DB
from expense_manager import ExpenseManager
from report import Report
import auth
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

db = DB()
mgr = ExpenseManager(db)
rep = Report(db)

# --- HELPER FUNCTION: Get User from Header ---
def get_auth_user():
    # We rely on the client (index.html) to send the username in a custom header
    user = request.headers.get("X-Username")
    if not user:
        # If header is missing, block access
        return None, jsonify({"status": "failed", "message": "Authentication required: X-Username header missing"}), 401
    return user, None, None
# ---------------------------------------------


@app.route("/api/register", methods=["POST"])
def register_user():
    payload = request.get_json()
    username = payload.get("username")
    password = payload.get("password")
    
    if not username or not password:
        return jsonify({"status": "failed", "message": "Username and password required"}), 400

    if auth.register(username, password):
        return jsonify({"status": "ok", "message": "User registered successfully"}), 201
    else:
        return jsonify({"status": "failed", "message": "Username already exists"}), 409

@app.route("/api/login", methods=["POST"])
def login_user():
    payload = request.get_json()
    username = payload.get("username")
    password = payload.get("password")
    
    if not username or not password:
        return jsonify({"status": "failed", "message": "Username and password required"}), 400

    # auth.login now returns the username on success, or None on failure
    logged_in_user = auth.login(username, password)
    
    if logged_in_user:
        # Pass the username back to the client to store and send in subsequent requests
        return jsonify({"status": "ok", "message": "Login successful", "username": logged_in_user}), 200
    else:
        return jsonify({"status": "failed", "message": "Invalid credentials"}), 401


# --- Data Routes: Now Filtered by User ---

@app.route("/api/expenses", methods=["GET"])
def get_expenses():
    user, error_response, status = get_auth_user()
    if error_response: return error_response, status
    
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 8))
    
    # Query only this user's expenses by filtering the database query
    sql_query = "SELECT * FROM expenses WHERE user = ? ORDER BY date DESC"
    df = db.query(sql_query, params=(user,))
    
    total = len(df)
    start = (page - 1) * per_page
    end = start + per_page
    data = df.iloc[start:end].to_dict(orient="records")
    return jsonify({"data": data, "total": total})


@app.route("/api/expenses", methods=["POST"])
def add_expense():
    user, error_response, status = get_auth_user()
    if error_response: return error_response, status
    
    payload = request.get_json()
    mgr.add_expense(
        user, # <-- Pass the user
        payload["date"],
        payload["category"],
        payload["amount"],
        payload.get("description", "")
    )
    return jsonify({"status": "ok"}), 201


@app.route("/api/reports/category")
def report_category():
    user, error_response, status = get_auth_user()
    if error_response: return error_response, status
    
    df = rep.total_by_category(user) # <-- Pass the user
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/reports/month")
def report_month():
    user, error_response, status = get_auth_user()
    if error_response: return error_response, status
    
    df = rep.total_by_month(user) # <-- Pass the user
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from db import init_db, add_expense, get_expenses, delete_expense, get_summary
from auth import login_user, register_user

app = Flask(__name__)
app.secret_key = 'super-secret-key'
CORS(app)

init_db()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_user(data["username"], data["password"])

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_user(data["username"], data["password"])

@app.route("/add_expense", methods=["POST"])
def add():
    data = request.json
    return add_expense(data)

@app.route("/expenses/<username>")
def list_expenses(username):
    return get_expenses(username)

@app.route("/delete_expense/<int:id>", methods=["DELETE"])
def delete(id):
    return delete_expense(id)

@app.route("/summary/<username>")
def summary(username):
    return get_summary(username)

if __name__ == "__main__":
    app.run(debug=True)

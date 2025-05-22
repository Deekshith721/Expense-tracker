import sqlite3
from flask import jsonify

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        category TEXT,
        type TEXT,
        amount REAL,
        description TEXT)''')
    conn.commit()
    conn.close()

def add_expense(data):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (username, date, category, type, amount, description) VALUES (?, ?, ?, ?, ?, ?)",
              (data["username"], data["date"], data["category"], data["type"], data["amount"], data["description"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

def update_expense(data):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("""
        UPDATE expenses SET date=?, category=?, type=?, amount=?, description=?
        WHERE id=? AND username=?
    """, (data["date"], data["category"], data["type"], data["amount"], data["description"], data["id"], data["username"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "updated"})

def get_expenses(username):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT id, username, date, category, type, amount, description FROM expenses WHERE username=?", (username,))
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)


def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

def get_summary(username):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT category, SUM(amount) FROM expenses WHERE username=? GROUP BY category", (username,))
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

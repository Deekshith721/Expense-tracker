import sqlite3
from flask import jsonify

def register_user(username, password):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"status": "registered"})
    except:
        return jsonify({"status": "error", "message": "Username already exists"})
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    if result:
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Invalid credentials"})

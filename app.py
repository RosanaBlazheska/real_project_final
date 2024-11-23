import flask
from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Поврзување со  sqlite databazata

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


# users=cursor.execute("select * from user_info")
# users_data=users.fetchall()
# for users in users_data:
#     print(users)

# 1.Преземање на вкупните трошоци по корисник

@app.route('/total_spent/<int:user_id>', methods=['GET'])
def total_spent(user_id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query Преземање на вкупните трошоци за специфичен корисник според неговиот ID.
    cursor.execute('SELECT SUM(money_spent) as total_spent FROM user_spending WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    conn.close()

    total_spent = result['total_spent'] if result['total_spent'] is not None else 0
    return jsonify({"user_id": user_id, "total_spent": total_spent})


# 2 Пресметување на просечните трошоци по возрасни групи

# Endpoint 2: Calculate Average Spending by Age Range
@app.route('/average_spending_by_age', methods=['GET'])
def average_spending_by_age():
    age_ranges = [(18, 24), (25, 30), (31, 36), (37, 47), (48, None)]
    results = {}
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    for start, end in age_ranges:
        if end:
            cursor.execute("""
                SELECT AVG(money_spent) AS avg_spending
                FROM user_spending
                JOIN user_info ON user_spending.user_id = user_info.user_id
                WHERE user_info.age BETWEEN ? AND ?
            """, (start, end))
        else:
            cursor.execute("""
                SELECT AVG(money_spent) AS avg_spending
                FROM user_spending
                JOIN user_info ON user_spending.user_id = user_info.user_id
                WHERE user_info.age >= ?
            """, (start,))

        avg_spent = cursor.fetchone()["avg_spending"]
        range_label = f"{start}-{end}" if end else f">{start}"
        results[range_label] = avg_spent or 0

    conn.close()
    return jsonify(results)

@app.route('/write_high_spending_user', methods=['POST'])
def write_high_spending_user():
    data = request.get_json()
    user_id = data.get('user_id')
    total_spending = data.get('total_spending')

    if not user_id or not total_spending:
        return jsonify({"error": "Missing user_id or total_spending"}), 400

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #
    cursor.execute('INSERT INTO high_spending_user (user_id, total_spending) VALUES (?, ?)',
                   (user_id, total_spending))
    conn.commit()
    conn.close()

    return jsonify({"message": "User recorded successfully"}), 201


# Тестирање на апликацијата

if __name__ == '__main__':
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_info (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_spending (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        money_spent REAL,
        year INTEGER,
        FOREIGN KEY (user_id) REFERENCES user_info (user_id)
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS high_spending_user (
        user_id INTEGER PRIMARY KEY,
        total_spending REAL
    )''')

    conn.commit()
    conn.close()

    app.run(debug=True)

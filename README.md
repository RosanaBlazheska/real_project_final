# Python project
This is a Flask-based web application that manages user spending data. It connects to an SQLite database and provides endpoints to:  Retrieve the total spending of a user. Calculate average spending based on age groups. Save and manage high-spending users. The application is designed as a final project for a Python development course .

# Flask API for User Spending Management

## Description
This application is built using Flask and SQLite database. It provides the following functionalities:
- Retrieve total spending per user
- Calculate average spending by age groups
- Save high-spending users

## Installation
1. Clone the repository:
   
bash
   git clone https://github.com/RosanaBlazheska/real_project_final.git
   cd real_project_final
Install dependencies:

pip install flask
Run the application:

python app.py
Code
Here is the source code of the application:

import flask
from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Connecting to the SQLite database

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 1. Retrieve total spending per user
@app.route('/total_spent/<int:user_id>', methods=['GET'])
def total_spent(user_id):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Query to retrieve total spending for a specific user by their ID
    cursor.execute('SELECT SUM(money_spent) as total_spent FROM user_spending WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()

    conn.close()

    total_spent = result['total_spent'] if result['total_spent'] is not None else 0
    return jsonify({"user_id": user_id, "total_spent": total_spent})


# 2. Calculate average spending by age groups
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

# 3. Save high-spending users
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


# Running the application
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

API Endpoints
1. GET /total_spent/<user_id>
Retrieves the total spending for a specific user.

2. GET /average_spending_by_age
Calculates the average spending by age groups.

3. POST /write_high_spending_user
Saves users with high spending.












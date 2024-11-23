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


# Connecting to the SQLite database
conn = sqlite3.connect("name-database.db")

# 1. Retrieve total spending per user
1. GET /total_spent/<user_id>
Retrieves the total spending for a specific user.

# 2. Calculate average spending by age groups
2. GET /average_spending_by_age
Calculates the average spending by age groups.

# 3. Save high-spending users
POST /write_high_spending_user-save users 
Saves users with high spending.

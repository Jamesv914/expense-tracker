from flask import Flask, render_template, request, redirect, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_PATH = 'data/expenses.db'

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    note = request.form['note']
    date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)',
              (amount, category, note, date))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/expenses', methods=['GET'])
def get_expenses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, amount, category, note, date FROM expenses ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()

    expenses = [
        {'id': r[0], 'amount': r[1], 'category': r[2], 'note': r[3], 'date': r[4]}
        for r in rows
    ]
    return jsonify(expenses)

@app.route('/summary', methods=['GET'])
def get_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    rows = c.fetchall()
    conn.close()

    summary = [{'category': r[0], 'total': r[1]} for r in rows]
    return jsonify(summary)

# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True)
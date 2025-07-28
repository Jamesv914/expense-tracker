from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
DB_PATH = 'data/expenses.db'

# ---------- DATABASE ----------
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
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get all expenses
    c.execute('SELECT date, amount, category, note FROM expenses ORDER BY date DESC')
    rows = c.fetchall()

    # Get category summary
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    summary = c.fetchall()

    conn.close()

    # Convert for chart
    chart_data = [{'category': r[0], 'total': r[1]} for r in summary]
    return render_template('index.html', expenses=rows, chart_data=json.dumps(chart_data))

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

# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True)
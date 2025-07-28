import sqlite3
from datetime import datetime

DB_PATH = 'data/expenses.db'

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect()
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

def add_expense(amount, category, note, date=None):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    conn = connect()
    c = conn.cursor()
    c.execute('INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)',
              (amount, category, note, date))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT date, amount, category, note FROM expenses ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_category_summary():
    conn = connect()
    c = conn.cursor()
    c.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
    rows = c.fetchall()
    conn.close()
    return [{'category': r[0], 'total': r[1]} for r in rows]
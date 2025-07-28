# Expense Tracker App

A sleek, D3-powered Expense Tracker built with **Python + Flask + SQLite + Bootstrap**.  
Track your spending, visualize trends, and manage your budget — all in one lightweight app.


## Features

- Add expenses (amount, category, note, date)
- View recent expenses in a responsive table
- Interactive D3.js bar chart: spending by category
- Persistent local storage via SQLite
- Clean UI styled with Bootstrap & custom CSS


## Project Structure
```
expense-tracker/
│
├── app.py                  # Main Flask app
├── requirements.txt        # Dependencies
│
├── templates/
│   └── index.html          # Dashboard view
│
├── static/
│   ├── style.css           # Custom CSS
│
├── data/
│   └── expenses.db         # SQLite database
│
└── utils/
└── db_utils.py         # DB interaction functions
```

## Installation

1. Clone this repo:
   cd expense-tracker
2. python3 -m venv venv
   source venv/bin/activate
3. pip install -r requirements.txt
4. mkdir data
5. python app.py
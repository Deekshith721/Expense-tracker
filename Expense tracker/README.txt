# 💰 Expense Tracker App

A full-stack Expense Tracker web app with a Flask backend and Streamlit frontend. This app allows users to register, login, add expenses, view and delete their history, and see a summary of their spending.

---

##  Features

-  User Registration & Login
- Add Expenses (date, category, amount, description)
- View Expense History
- Delete Expenses
- Expense Summary (category-wise)
- Basic Authentication
- Streamlit-based clean UI
- SQLite database for persistence

---

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: [Flask](https://flask.palletsprojects.com/)
- **Database**: SQLite
- **API Communication**: `requests`, `flask-cors`

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker


1. install packages
    pip install -r requirements.txt
2.run Backend
    cd backend
    python app.py
3.run frontend
    cd frontend
    streamlit run app.py
import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5000"

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        res = requests.post(f"{API}/login", json={"username": username, "password": password})
        if res.json().get("status") == "success":
            st.session_state.username = username
            st.success("Logged in")
        else:
            st.error("Invalid credentials")

def register():
    st.subheader("Register")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type='password')
    if st.button("Register"):
        res = requests.post(f"{API}/register", json={"username": username, "password": password})
        st.write(res.json())

def dashboard():
    st.title("Expense Tracker")

    if "username" not in st.session_state:
        st.warning("Login first")
        return

    # Add Expense
    st.subheader("Add Expense")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Other"])
    amount = st.number_input("Amount", step=0.01)
    description = st.text_input("Description")
    if st.button("Add Expense"):
        data = {
            "username": st.session_state.username,
            "date": str(date),
            "category": category,
            "amount": amount,
            "description": description
        }
        res = requests.post(f"{API}/add_expense", json=data)
        st.success("Expense Added")

    # View Expenses
    st.subheader("Your Expenses")
    res = requests.get(f"{API}/expenses/{st.session_state.username}")
    df = pd.DataFrame(res.json(), columns=["ID", "Username", "Date", "Category", "Amount", "Description"])
    st.dataframe(df)

    # Delete
    del_id = st.number_input("Delete Expense ID", step=1)
    if st.button("Delete"):
        requests.delete(f"{API}/delete_expense/{int(del_id)}")
        st.success("Deleted")

    # Summary
    st.subheader("Summary")
    res = requests.get(f"{API}/summary/{st.session_state.username}")
    summary = res.json()
    summary_df = pd.DataFrame(summary, columns=["Category", "Total"])
    st.bar_chart(summary_df.set_index("Category"))

def main():
    st.sidebar.title("Menu")
    choice = st.sidebar.radio("Go to", ["Login", "Register", "Dashboard"])
    if choice == "Login":
        login()
    elif choice == "Register":
        register()
    elif choice == "Dashboard":
        dashboard()

if __name__ == '__main__':
    main()

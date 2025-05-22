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
    type_ = st.radio("Transaction Type", ["Debit", "Credit"])
    category = st.selectbox("Category", ["Food", "Transport", "Rent", "Utilities", "Other"])
    amount = st.number_input("Amount", step=0.01)
    description = st.text_input("Description")
    if st.button("Add Expense"):
        data = {
        "username": st.session_state.username,
        "date": str(date),
        "category": category,
        "type": type_,
        "amount": amount,
        "description": description
    }

        res = requests.post(f"{API}/add_expense", json=data)
        st.success("Expense Added")

    
    st.subheader("Edit Transaction")
    edit_id = st.number_input("Transaction ID to Edit", step=1)

    with st.form("edit_form"):
        new_date = st.date_input("New Date")
        new_category = st.selectbox("New Category", ["Food", "Transport", "Rent", "Utilities", "Other"])
        new_type = st.radio("New Type", ["Debit", "Credit"])
        new_amount = st.number_input("New Amount", step=0.01)
        new_desc = st.text_input("New Description")
        submit_edit = st.form_submit_button("Update")

    if submit_edit:
        edit_data = {
            "id": int(edit_id),
            "username": st.session_state.username,
            "date": str(new_date),
            "category": new_category,
            "type": new_type,
            "amount": new_amount,
            "description": new_desc
        }
        res = requests.put(f"{API}/update_expense", json=edit_data)
        st.success("Transaction Updated!")
        # Delete
        del_id = st.number_input("Delete Expense ID", step=1)
        if st.button("Delete"):
            requests.delete(f"{API}/delete_expense/{int(del_id)}")
            st.success("Deleted")
        

    # View Expenses
    st.subheader("Your Expenses")
    res = requests.get(f"{API}/expenses/{st.session_state.username}")
    st.write("Status code:", res.status_code)
    st.write("Raw response text:", res.text)
    df = pd.DataFrame(res.json(), columns=["ID", "Username", "Date", "Category", "Type", "Amount", "Description"])
    st.dataframe(df)


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

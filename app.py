import streamlit as st
import sqlite3
import random
import pandas as pd

# Database connection
conn = sqlite3.connect("bank.db", check_same_thread=False)
c = conn.cursor()

# Create tables
c.execute("""CREATE TABLE IF NOT EXISTS users(
username TEXT,
password TEXT
)""")

c.execute("""CREATE TABLE IF NOT EXISTS accounts(
name TEXT,
account_no INTEGER,
balance INTEGER
)""")

c.execute("""CREATE TABLE IF NOT EXISTS transactions(
account_no INTEGER,
type TEXT,
amount INTEGER
)""")

conn.commit()

# Create default admin only once
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO users VALUES('admin','1234')")
    conn.commit()

st.title("🏦 Bank Management System")

menu = [
"Login",
"Create Account",
"Deposit",
"Withdraw",
"Check Balance",
"Transaction History",
"Customer List",
"Dashboard"
]

choice = st.sidebar.selectbox("Menu", menu)

# LOGIN
if choice == "Login":

    st.subheader("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()

        if result:
            st.success("Login Successful ✅")
            st.balloons()
        else:
            st.error("Wrong Username or Password ❌")

# CREATE ACCOUNT
elif choice == "Create Account":

    st.subheader("Create Bank Account")

    name = st.text_input("Customer Name")

    if st.button("Create Account"):
        acc = random.randint(10000, 99999)

        c.execute("INSERT INTO accounts VALUES(?,?,?)", (name, acc, 0))
        conn.commit()

        st.success(f"Account Created Successfully! Account Number: {acc}")

# DEPOSIT
elif choice == "Deposit":

    st.subheader("Deposit Money")

    acc = st.number_input("Account Number")
    amt = st.number_input("Amount")

    if st.button("Deposit"):
        c.execute("UPDATE accounts SET balance = balance + ? WHERE account_no = ?", (amt, acc))
        c.execute("INSERT INTO transactions VALUES(?,?,?)", (acc, "Deposit", amt))
        conn.commit()

        st.success("Money Deposited Successfully")

# WITHDRAW
elif choice == "Withdraw":

    st.subheader("Withdraw Money")

    acc = st.number_input("Account Number")
    amt = st.number_input("Amount")

    if st.button("Withdraw"):
        c.execute("UPDATE accounts SET balance = balance - ? WHERE account_no = ?", (amt, acc))
        c.execute("INSERT INTO transactions VALUES(?,?,?)", (acc, "Withdraw", amt))
        conn.commit()

        st.success("Money Withdrawn Successfully")

# CHECK BALANCE
elif choice == "Check Balance":

    st.subheader("Check Balance")

    acc = st.number_input("Account Number")

    if st.button("Check Balance"):

        c.execute("SELECT balance FROM accounts WHERE account_no=?", (acc,))
        data = c.fetchone()

        if data:
            st.success(f"Current Balance: ₹{data[0]}")
        else:
            st.error("Account Not Found")

# TRANSACTION HISTORY
elif choice == "Transaction History":

    st.subheader("Transaction History")

    acc = st.number_input("Account Number")

    if st.button("View History"):

        c.execute("SELECT * FROM transactions WHERE account_no=?", (acc,))
        data = c.fetchall()

        df = pd.DataFrame(data, columns=["Account No", "Type", "Amount"])

        st.table(df)

# CUSTOMER LIST
elif choice == "Customer List":

    st.subheader("Customer List")

    c.execute("SELECT * FROM accounts")
    data = c.fetchall()

    df = pd.DataFrame(data, columns=["Name", "Account No", "Balance"])

    st.table(df)

# DASHBOARD
elif choice == "Dashboard":

    st.subheader("Bank Dashboard")

    c.execute("SELECT COUNT(*) FROM accounts")
    total_accounts = c.fetchone()[0]

    c.execute("SELECT SUM(balance) FROM accounts")
    total_balance = c.fetchone()[0]

    st.metric("Total Accounts", total_accounts)

    if total_balance:
        st.metric("Total Bank Balance", f"₹{total_balance}")
    else:
        st.metric("Total Bank Balance", "₹0")
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Expense Tracker", page_icon="💰")

st.title("💰 Personal Finance Expense Tracker")

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state["expenses"] = pd.DataFrame(columns=["Category", "Amount"])

# Input fields
st.header("➕ Add New Expense")

category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Education", "Health", "Other"])
amount = st.number_input("Amount (₹)", min_value=0.0, format="%.2f")

if st.button("Add Expense"):
    new_entry = {"Category": category, "Amount": amount}
    st.session_state["expenses"] = pd.concat(
        [st.session_state["expenses"], pd.DataFrame([new_entry])],
        ignore_index=True
    )
    st.success("Expense added successfully!")
    st.rerun()

st.divider()

# Expense History Section
st.header("📄 Expense History")

if not st.session_state["expenses"].empty:

    # Make sure Category is left & Amount right
    st.session_state["expenses"] = st.session_state["expenses"][["Category", "Amount"]]

    # Dropdown to select a row to delete
    selected_row = st.selectbox(
        "Select a row to delete:",
        range(len(st.session_state["expenses"])),
        format_func=lambda x: f"{st.session_state['expenses'].iloc[x]['Category']} → ₹{st.session_state['expenses'].iloc[x]['Amount']}"
    )

    # Delete selected row
    if st.button("Delete Selected Expense 🗑️"):
        st.session_state["expenses"].drop(index=selected_row, inplace=True)
        st.session_state["expenses"].reset_index(drop=True, inplace=True)
        st.success("Selected expense deleted!")
        st.rerun()

    # Clear all expenses
    if st.button("Clear All Expenses ❌"):
        st.session_state["expenses"] = pd.DataFrame(columns=["Category", "Amount"])
        st.success("All expenses cleared!")
        st.rerun()

# Display updated table
st.dataframe(st.session_state["expenses"], use_container_width=True)

# Summary Section
st.header("📊 Summary")
total = st.session_state["expenses"]["Amount"].sum()
st.metric(label="Total Amount Spent", value=f"₹ {total:.2f}")

# Category-wise chart
if not st.session_state["expenses"].empty:
    chart_data = st.session_state["expenses"].groupby("Category")["Amount"].sum()
    st.bar_chart(chart_data)

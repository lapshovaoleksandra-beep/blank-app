
import streamlit as st
import pandas as pd
from datetime import date
import altair as alt

# ------------------------------------------------
# 1. PAGE CONFIGURATION
# ------------------------------------------------

st.set_page_config(
    page_title="FinanceWise",
    page_icon="💰",
    layout="wide"
)

# ------------------------------------------------
# 2. INITIALIZE APPLICATION DATA
# ------------------------------------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=[
            "Date",
            "Description",
            "Category",
            "Amount"
        ]
    )

# ------------------------------------------------
# 3. APPLICATION TITLE
# ------------------------------------------------

st.title("💰 FinanceWise")
st.subheader("Personal Expense Tracker")

st.write(
    "Track your spending, understand your habits, "
    "and take control of your finances."
)

st.divider()

# ------------------------------------------------
# 4. SIDEBAR - ADD NEW EXPENSE
# ------------------------------------------------

st.sidebar.header("Add a New Expense")

with st.sidebar.form("expense_form"):

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    description = st.text_input(
        "Description",
        placeholder="Example: Grocery shopping"
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transportation",
            "Entertainment",
            "Bills",
            "Shopping",
            "Education",
            "Healthcare",
            "Other"
        ]
    )

    amount = st.number_input(
        "Amount ($)",
        min_value=0.0,
        value=0.0,
        step=1.0,
        format="%.2f"
    )

    submitted = st.form_submit_button(
        "Add Expense",
        use_container_width=True
    )

    if submitted:

        if amount <= 0:
            st.sidebar.error(
                "Please enter an amount greater than zero."
            )

        elif not description.strip():
            st.sidebar.error(
                "Please enter an expense description."
            )

        else:

            new_expense = pd.DataFrame([{
                "Date": pd.Timestamp(expense_date),
                "Description": description.strip(),
                "Category": category,
                "Amount": float(amount)
            }])

            st.session_state.expenses = pd.concat(
                [
                    st.session_state.expenses,
                    new_expense
                ],
                ignore_index=True
            )

            st.sidebar.success(
                "Expense added successfully!"
            )

# ------------------------------------------------
# 5. MONTH FILTER
# ------------------------------------------------

expenses = st.session_state.expenses.copy()

if not expenses.empty:

    expenses["Date"] = pd.to_datetime(
        expenses["Date"]
    )

    months = sorted(
        expenses["Date"].dt.strftime("%Y-%m").unique(),
        reverse=True
    )

    selected_month = st.selectbox(
        "Select Month",
        ["All Months"] + months
    )

    if selected_month != "All Months":

        expenses = expenses[
            expenses["Date"].dt.strftime("%Y-%m")
            == selected_month
        ]

else:
    st.info(
        "No expenses recorded yet. "
        "Use the sidebar to add your first expense."
    )

# ------------------------------------------------
# 6. FINANCIAL SUMMARY
# ------------------------------------------------

total_expenses = expenses["Amount"].sum()

number_of_expenses = len(expenses)

average_expense = (
    total_expenses / number_of_expenses
    if number_of_expenses > 0
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Expenses",
    f"${total_expenses:,.2f}"
)

col2.metric(
    "Number of Transactions",
    f"{number_of_expenses}"
)

col3.metric(
    "Average Expense",
    f"${average_expense:,.2f}"
)

st.divider()

# ------------------------------------------------
# 7. SPENDING BY CATEGORY
# ------------------------------------------------

st.subheader("Spending by Category")

if not expenses.empty:

    category_totals = (
        expenses.groupby("Category")["Amount"]
        .sum()
        .reset_index()
        .sort_values("Amount", ascending=False)
    )

    chart = alt.Chart(category_totals).mark_bar(
        cornerRadiusEnd=5
    ).encode(
        x=alt.X(
            "Amount:Q",
            title="Amount Spent ($)"
        ),
        y=alt.Y(
            "Category:N",
            sort="-x",
            title="Category"
        ),
        tooltip=[
            "Category",
            alt.Tooltip(
                "Amount:Q",
                format="$.2f"
            )
        ]
    ).properties(
        height=300
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )

    st.dataframe(
        category_totals,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Add expenses to see your spending chart.")

st.divider()

# ------------------------------------------------
# 8. TRANSACTION HISTORY
# ------------------------------------------------

st.subheader("Transaction History")

if not expenses.empty:

    display_expenses = expenses.sort_values(
        "Date",
        ascending=False
    )

    st.dataframe(
        display_expenses,
        use_container_width=True,
        hide_index=True
    )

    # Download transaction data as CSV
    csv_data = display_expenses.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Expenses (CSV)",
        data=csv_data,
        file_name="financewise_expenses.csv",
        mime="text/csv"
    )

else:
    st.write("No transactions available.")

# ------------------------------------------------
# 9. RESET APPLICATION DATA
# ------------------------------------------------

st.divider()

st.subheader("Manage Your Data")

if st.button(
    "Clear All Expenses",
    type="secondary"
):

    st.session_state.expenses = pd.DataFrame(
        columns=[
            "Date",
            "Description",
            "Category",
            "Amount"
        ]
    )

    st.rerun()

# ------------------------------------------------
# 10. FOOTER
# ------------------------------------------------

st.divider()

st.caption(
    "FinanceWise | Personal Finance Management "
    "| Educational purposes only"
)

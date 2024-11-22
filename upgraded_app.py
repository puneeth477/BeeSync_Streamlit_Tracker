import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="BeeSync Streamlit Tracker",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styling for background, table, and buttons
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #e6f7ff, #b3e6ff);
            font-family: 'Sans-serif';
        }
        .stButton button {
            background-color: #33b073;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
            border: none;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #004d99;
        }
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #004d99;
            text-align: center;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table th {
            background-color: #33b073;
            color: white;
            padding: 12px;
            text-align: left;
        }
        table td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
            text-align: left;
        }
        table tr:hover {
            background-color: #f1f1f1;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Load the Excel file
file_path = Path("BeeSync _ Streamlit_Tracker.xlsx")

try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"File not found: {file_path}. Please ensure it is in the correct location.")
    st.stop()

# Sidebar
st.sidebar.header("BeeSync Tracker")
account_list = df["Account Name"].unique().tolist()
selected_account = st.sidebar.selectbox("Select an Account", account_list)

# Display page title
st.markdown("<div class='main-title'>BeeSync Tracker</div>", unsafe_allow_html=True)

# Display account-specific data
account_data = df[df["Account Name"] == selected_account]

# Format dates to exclude time
if "Meeting Date" in account_data.columns:
    account_data["Meeting Date"] = pd.to_datetime(account_data["Meeting Date"], errors="coerce").dt.date

if "Follow-Up Date" in account_data.columns:
    account_data["Follow-Up Date"] = pd.to_datetime(account_data["Follow-Up Date"], errors="coerce").dt.date

# Display account details title
st.markdown(
    f"<h3 style='color: #004d99;'>BeeSync Details for Account: {selected_account}</h3>",
    unsafe_allow_html=True,
)

# Display the table
if not account_data.empty:
    st.markdown(
        account_data.to_html(index=False, escape=False, justify="left"),
        unsafe_allow_html=True,
    )
else:
    st.write("No data available for this account.")

# Add a Plotly Chart
st.subheader("Feedback Score Trend")
if "Meeting Date" in account_data.columns and "Feedback Score (1-10)" in account_data.columns:
    account_data["Meeting Month-Year"] = pd.to_datetime(account_data["Meeting Date"], errors="coerce").dt.strftime("%b-%Y")
    score_chart = px.line(
        account_data,
        x="Meeting Month-Year",
        y="Feedback Score (1-10)",
        title="Feedback Score Over Time",
        markers=True,
    )
    score_chart.update_layout(xaxis_title="Month-Year", yaxis_title="Feedback Score")
    st.plotly_chart(score_chart)

# Add Fun Icons
st.markdown(
    """
    <div style="text-align: center;">
        <span class="icon">🐝</span>
        <span class="icon">📊</span>
        <span class="icon">✅</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add a Refresh Button
if st.button("Refresh Data"):
    st.experimental_rerun()

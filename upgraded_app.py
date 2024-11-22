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

# Set up styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(135deg, #86c7f3, #33b073);
            color: white;
            font-family: 'Sans-serif';
        }
        .css-1h6j0fc {
            color: black !important;
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

# Display account-specific data
account_data = df[df["Account Name"] == selected_account]

# Display Account Info
st.title(f"Account Details for {selected_account}")
st.write(account_data)

# Add a Plotly Chart
st.subheader("Feedback Score Trend")
if "Meeting Date" in account_data.columns and "Feedback Score (1-10)" in account_data.columns:
    account_data["Meeting Date"] = pd.to_datetime(account_data["Meeting Date"])
    score_chart = px.line(
        account_data,
        x="Meeting Date",
        y="Feedback Score (1-10)",
        title="Feedback Score Over Time",
        markers=True,
    )
    st.plotly_chart(score_chart)

# Add a Refresh Button
if st.button("Refresh Data"):
    st.experimental_rerun()

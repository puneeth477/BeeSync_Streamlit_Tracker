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
        .icon {
            font-size: 50px;
            margin: 10px;
            color: #33b073;
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
    # Format Meeting Date to display Month-Year
    account_data["Meeting Month-Year"] = account_data["Meeting Date"].dt.strftime("%b-%Y")
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

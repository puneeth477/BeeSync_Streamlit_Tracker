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
        .styled-table {
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 16px;
            text-align: left;
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .styled-table th {
            background-color: #004d99;
            color: white;
            text-align: left;
            padding: 12px 15px;
        }
        .styled-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #ddd;
        }
        .styled-table tr:hover {
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

# Display account-specific data
account_data = df[df["Account Name"] == selected_account]

# Format dates to exclude time
if "Meeting Date" in account_data.columns:
    account_data["Meeting Date"] = pd.to_datetime(account_data["Meeting Date"]).dt.date

if "Follow-Up Date" in account_data.columns:
    account_data["Follow-Up Date"] = pd.to_datetime(account_data["Follow-Up Date"]).dt.date

st.title(f"Account Details for {selected_account}")

# Render account data as a styled table
st.markdown("<h3 style='color: #004d99;'>Meeting Details</h3>", unsafe_allow_html=True)
if not account_data.empty:
    table_html = """
    <table class="styled-table">
        <thead>
            <tr>
                <th>Meeting Date</th>
                <th>Status</th>
                <th>Feedback Score</th>
                <th>Follow-Up Date</th>
                <th>Next Meeting Planned</th>
                <th>Escalations</th>
                <th>CSM Owner</th>
            </tr>
        </thead>
        <tbody>
    """
    for _, row in account_data.iterrows():
        table_html += f"""
        <tr>
            <td>{row['Meeting Date']}</td>
            <td>{row['Meeting Status']}</td>
            <td>{row['Feedback Score (1-10)']}</td>
            <td>{row['Follow-Up Date']}</td>
            <td>{row['Next Meeting Planned (Yes/No)']}</td>
            <td>{row['Escalations (Yes/No)']}</td>
            <td>{row['CSM Owner']}</td>
        </tr>
        """
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.write("No data available for this account.")

# Add a Plotly Chart
st.subheader("Feedback Score Trend")
if "Meeting Date" in account_data.columns and "Feedback Score (1-10)" in account_data.columns:
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
        <span class="

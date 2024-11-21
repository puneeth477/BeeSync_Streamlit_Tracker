import streamlit as st
import pandas as pd

# Load data from a local file
@st.cache
def load_data_from_local(file_path):
    return pd.read_excel(file_path)

# Local Excel file path
FILE_PATH = "//home/bhlp0125/CSM-Streamlit/BeeSync _ Streamlit_Tracker.xlsx"

# Streamlit App
st.title("CSM Tracker Dashboard")

try:
    # Load the data
    data = load_data_from_local(FILE_PATH)

    # Sidebar: Select Account
    st.sidebar.header("Select an Account")
    account_names = data["Account Name"].unique()
    selected_account = st.sidebar.selectbox("Accounts", account_names)

    # Filter data for the selected account
    account_data = data[data["Account Name"] == selected_account]

    # Display account details
    st.subheader(f"Details for Account: {selected_account}")
    st.table(account_data[[
        "Quarter", "Meeting Date", "Meeting Status", "Meeting Cadence",
        "Follow-Up Date", "Feedback Score (1-10)", "MoM Notes",
        "Next Meeting Planned (Yes/No)", "Date of Next Meeting", 
        "Escalations (Yes/No)", "CSM Owner"
    ]])

    # Display metrics for the selected account
    st.subheader("Account Metrics")
    total_meetings = len(account_data)
    completed_meetings = len(account_data[account_data["Meeting Status"] == "Completed"])
    average_feedback = account_data["Feedback Score (1-10)"].mean()
    next_meeting_count = len(account_data[account_data["Next Meeting Planned (Yes/No)"] == "Yes"])
    escalations_count = len(account_data[account_data["Escalations (Yes/No)"] == "Yes"])

    # Show metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Meetings", total_meetings)
    col2.metric("Completed Meetings", completed_meetings)
    col3.metric("Avg. Feedback Score", f"{average_feedback:.1f}" if pd.notna(average_feedback) else "N/A")
    col4.metric("Next Meetings", next_meeting_count)
    col5.metric("Escalations", escalations_count)

    # Add notes
    st.subheader("Account Notes")
    for index, row in account_data.iterrows():
        st.markdown(f"**MoM Notes for {row['Meeting Date']}**: {row['MoM Notes']}")

    # Add refresh button
    if st.button("Refresh Data"):
        st.experimental_rerun()

except FileNotFoundError:
    st.error(f"The file at {FILE_PATH} was not found. Please ensure the path is correct.")
except KeyError as e:
    st.error(f"A required column is missing: {e}")
except Exception as e:
    st.error(f"An error occurred: {e}")




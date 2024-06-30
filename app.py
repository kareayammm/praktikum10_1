import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

# Initialize session state for journal entries
if 'journal_entries' not in st.session_state:
    st.session_state['journal_entries'] = []

# Function to add a task
def add_task(title, description, deadline):
    task = {
        'Title': title,
        'Description': description,
        'Deadline': deadline,
        'Completed': False
    }
    st.session_state['tasks'].append(task)

# Function to add a journal entry
def add_journal_entry(date, entry):
    journal_entry = {
        'Date': date,
        'Entry': entry
    }
    st.session_state['journal_entries'].append(journal_entry)

# Sidebar inputs for user profile
st.sidebar.header("Profile")
user_name = st.sidebar.text_input("Name", "John Doe")
user_email = st.sidebar.text_input("Email", "john.doe@example.com")
user_profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
if user_profile_pic is not None:
    st.sidebar.image(user_profile_pic, width=100, caption='Profile Picture', use_column_width=False)

# Sidebar inputs for adding new task
st.sidebar.header("Add New Task")
title = st.sidebar.text_input("Title")
description = st.sidebar.text_area("Description")
deadline = st.sidebar.date_input("Deadline")
if st.sidebar.button("Add Task"):
    add_task(title, description, deadline)
    st.sidebar.success("Task added!")

# Main interface
st.title("NOTE YOURS")

# Task filtering
st.subheader("Tasks")
filter_status = st.selectbox("Filter tasks by status", ["All", "Completed", "Pending"])

# Convert tasks to DataFrame
df = pd.DataFrame(st.session_state['tasks'])

# Filter tasks based on the selected filter
if filter_status == "Completed":
    df = df[df['Completed']]
elif filter_status == "Pending":
    df = df[~df['Completed']]

# Display tasks
if not df.empty:
    for index, row in df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{row['Title']}**")
            st.markdown(f"{row['Description']}")
            st.markdown(f"**Deadline:** {row['Deadline']}")
        with col2:
            if not row['Completed']:
                if st.button(f"Mark as Completed##{index}"):
                    st.session_state['tasks'][index]['Completed'] = True
                    st.experimental_rerun()
            else:
                st.markdown("✅ Completed")
else:
    st.write("No tasks to display.")

# Visualization
st.subheader("Task Deadlines")
if not df.empty:
    deadlines = df.groupby('Deadline').size()
    st.bar_chart(deadlines)

# Daily Journal
st.sidebar.header("Daily Journal")
journal_date = st.sidebar.date_input("Date", value=datetime.now())
journal_entry = st.sidebar.text_area("Journal Entry")
if st.sidebar.button("Add Journal Entry"):
    add_journal_entry(journal_date, journal_entry)
    st.sidebar.success("Journal entry added!")

st.subheader("Daily Journal")
journal_df = pd.DataFrame(st.session_state['journal_entries'])
if not journal_df.empty:
    journal_df.set_index('Date', inplace=True)
    st.dataframe(journal_df)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")

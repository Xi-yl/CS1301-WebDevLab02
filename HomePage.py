# This creates the main landing page for the Streamlit application.

import streamlit as st

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
)

st.title("Student Study Habits Dashboard")

st.write("""
This application displays and analyzes student study hours and sleep patterns throughout the week.

### How to use this app:
- **Visuals Page**: View weekly study hours and interact with the study and sleep charts.
- **Survey Page**: Enter your own data (Part 2).

This project is part of CS 1301's Lab 2.
""")
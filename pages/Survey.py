# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv
from pathlib import Path

csv_file = Path(__file__).resolve().parent.parent / "data.csv"

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Enter a subject and how many hours you study it per day.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("What subject do you study?")
    value_input = st.text_input("How many hours do you study this subject per day?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        category_input = category_input.strip()
        try:
            hours = float(value_input)
        except ValueError:
            hours = -1

        if not category_input:
            st.error("Please enter a subject.")
        elif not 0 <= hours <= 24:
            st.error("Please enter a number of hours between 0 and 24.")
        else:
            needs_header = not csv_file.exists() or csv_file.stat().st_size == 0
            with open(csv_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if needs_header:
                    writer.writerow(["Category", "Value"])
                writer.writerow([category_input, hours])

            st.success("Your data has been submitted!")
            st.write(f"Subject: {category_input}, Daily study hours: {hours}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv(csv_file, dtype={"Category": str}, keep_default_na=False)
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")

# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import altair as alt
import json
from pathlib import Path

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json

st.header("Student Study Habits Dashboard")
st.write("Explore study hours and sleep patterns throughout the week.")

# Load data from JSON file
with open(Path(__file__).resolve().parent.parent / "data.json", "r") as file:
    data = json.load(file)

# Convert JSON data into a DataFrame
df = pd.DataFrame(data["data_points"])


# GRAPH 1: STATIC BAR CHART

st.subheader("1. Weekly Study Hours")
st.write("This chart shows the number of hours spent studying each day.")

day_order = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

df["day"] = pd.Categorical(
    df["day"],
    categories=day_order,
    ordered=True
)

st.bar_chart(
    df,
    x="day",
    y="study_hours"
)

# GRAPH 2: DYNAMIC LINE CHART

st.subheader("2. Interactive Study and Sleep Analysis")

# Initialize Session State
if "selected_metric" not in st.session_state:
    st.session_state["selected_metric"] = "study_hours"

if "days_to_show" not in st.session_state:
    st.session_state["days_to_show"] = 7

# User interaction
metric = st.radio(
    "Choose a metric:",
    ["study_hours", "sleep_hours"],
    key="selected_metric"
)

days = st.slider(
    "Number of days to display:",
    min_value=1,
    max_value=7,
    key="days_to_show"
)

# Filter data according to user selection
filtered_df = df.head(days)

# Create advanced Altair line chart
chart = (
    alt.Chart(filtered_df)
    .mark_line(point=True)
    .encode(
        x=alt.X("day:N", title="Day of the Week", sort=None),
        y=alt.Y(f"{metric}:Q", title="Hours"),
        tooltip=["day", metric]
    )
    .properties(
        title="Weekly Study and Sleep Trends",
        height=400
    )
)

st.altair_chart(chart, use_container_width=True)


# EXTRA CREDIT: MEAN AND MEDIAN

st.subheader("Summary Statistics")

mean_value = filtered_df[metric].mean()
median_value = filtered_df[metric].median()

# Initialize previous statistics in Session State
if "previous_mean" not in st.session_state:
    st.session_state["previous_mean"] = mean_value

if "previous_median" not in st.session_state:
    st.session_state["previous_median"] = median_value

# Calculate changes
mean_change = mean_value - st.session_state["previous_mean"]
median_change = median_value - st.session_state["previous_median"]

# Display metrics
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Mean Hours",
        value=f"{mean_value:.2f}",
        delta=f"{mean_change:+.2f}"
    )

with col2:
    st.metric(
        label="Median Hours",
        value=f"{median_value:.2f}",
        delta=f"{median_change:+.2f}"
    )

# Save current statistics for the next interaction
st.session_state["previous_mean"] = mean_value
st.session_state["previous_median"] = median_value


# PART 2: GRAPHS FROM data.csv
st.header("Study Habits Survey Results")
csv_file = Path(__file__).resolve().parent.parent / "data.csv"

if not csv_file.exists() or csv_file.stat().st_size == 0:
    st.info("Submit study data on the Survey page to see the charts.")
else:
    survey_data = pd.read_csv(csv_file, dtype={"Category": str}, keep_default_na=False)

    if survey_data.empty:
        st.info("Submit study data on the Survey page to see the charts.")
    else:
        # This chart always uses every response in the CSV.
        st.subheader("Average Daily Study Hours by Subject")
        averages = survey_data.groupby("Category")["Value"].mean()
        st.bar_chart(averages, x_label="Subject", y_label="Daily study hours")

        st.subheader("Individual Study Responses")
        subjects = sorted(survey_data["Category"].unique().tolist())
        if "csv_subjects" not in st.session_state:
            st.session_state.csv_subjects = subjects

        st.multiselect("Subjects to display", subjects, key="csv_subjects")
        survey_data["Response"] = range(1, len(survey_data) + 1)
        filtered_data = survey_data[
            survey_data["Category"].isin(st.session_state.csv_subjects)
        ]

        if filtered_data.empty:
            st.info("Choose at least one subject to display.")
        else:
            chart = alt.Chart(filtered_data).mark_circle(size=80).encode(
                x=alt.X("Response:Q", title="Response number"),
                y=alt.Y("Value:Q", title="Daily study hours"),
                color=alt.Color("Category:N", title="Subject")
            ).properties(title="Daily Study Hours for Selected Subjects")
            st.altair_chart(chart)

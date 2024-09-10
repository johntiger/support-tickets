import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

# Show app title and description.
st.set_page_config(page_title="Streamlit Table Demo", page_icon="🎫")
st.title("🎫 Table Demo")

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:

    # Set seed for reproducibility.
    np.random.seed(42)

    # Make up some fake issue descriptions.
    issue_descriptions = [
        "Network connectivity issues in the office",
        "Software application crashing on startup",
        # ... (remaining issue descriptions)
    ]

    # Generate the dataframe with 100 rows/tickets.
    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Issue": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2023, 6, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df

# Show section to view and edit existing tickets in a table.
st.header("Table")
date_min, date_max = st.slider(
    "Date filter",
    min_value=st.session_state.df["Date Submitted"].min(),
    max_value=st.session_state.df["Date Submitted"].max(),
    value=(
        st.session_state.df["Date Submitted"].min(),
        st.session_state.df["Date Submitted"].max(),
    ),
)

# 選択された範囲でデータフレームをフィルター
filtered_df = st.session_state.df[
    (st.session_state.df["Date Submitted"] >= date_min)
    & (st.session_state.df["Date Submitted"] <= date_max)
]
st.session_state.filtered_df = filtered_df

# テーブルを左側に表示
left_column, right_column = st.columns(2)
with left_column:
    st.write(f"Number of data: `{len(st.session_state.filtered_df)}`")
    st.write(filtered_df)

# Show some metrics and charts about the ticket.
with right_column:
    st.header("Statistics")

# 棒グラフを右上に表示
status_plot = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
right_column.altair_chart(status_plot, use_container_width=True, theme="streamlit")

# 円グラフを右下に表示
priority_plot = (
    alt.Chart(filtered_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
right_column.altair_chart(priority_plot, use_container_width=True, theme="streamlit")


# データフレームをCSV形式に変換
csv = filtered_df.to_csv(index=False).encode("utf-8")

# ダウンロードボタンを右側に表示
st.download_button(
    label="テーブルをダウンロード", data=csv, file_name="table.csv", mime="text/csv"
)

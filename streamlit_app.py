import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from faker import Faker

# Show app title and description.
st.set_page_config(page_title="Streamlit Table Demo", page_icon="🎫", layout="wide")
st.title("🎫 Table Demo")
import random
from faker import Faker
from faker.providers import BaseProvider

# カスタムプロバイダーを作成
class AirportProvider(BaseProvider):
    def airport_name(self):
        airports = [
             "東京羽田空港", "成田国際空港", "新千歳空港", "旭川空港", "函館空港",
            "青森空港", "秋田空港", "仙台空港", "新潟空港", "富山空港",
            "小松空港", "中部国際空港", "大阪伊丹空港", "関西国際空港", "神戸空港",
            "岡山空港", "広島空港", "山口宇部空港", "高松空港", "松山空港",
            "福岡空港", "北九州空港", "長崎空港", "熊本空港", "大分空港",
            "宮崎空港", "鹿児島空港", "那覇空港"
        ]
        return random.choice(airports)

# Create a random Pandas dataframe with existing tickets.
if "df" not in st.session_state:
    # Fakerライブラリを使って架空のデータを生成
    fake = Faker('ja_JP')

    # データの数
    num_records = 1000

    # データフレームのカラム
    columns = ['Name', 'Ticket Number', 'Date', 'Class', 'Departure', 'Destination', 'Flight Number', 'Seat Number']

    # Fakerインスタンスを作成し、カスタムプロバイダーを追加
    fake.add_provider(AirportProvider)

    # データを生成
    data = {
        'Name': [fake.name() for _ in range(num_records)],
        'Ticket Number': [fake.unique.random_number(digits=10) for _ in range(num_records)],
        'Date': [fake.date_this_year() for _ in range(num_records)],
        'Class': [np.random.choice(['Economy', 'Business', 'First']) for _ in range(num_records)],
        'Departure': [fake.airport_name() for _ in range(num_records)],
        'Destination': [fake.airport_name() for _ in range(num_records)],
        'Flight Number': ['JAL'+str(fake.random_number(digits=3)) for _ in range(num_records)],
        'Seat Number': [f"{np.random.randint(1, 30)}{np.random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}" for _ in range(num_records)]
    }

    # データフレームを作成
    df = pd.DataFrame(data)

    # Save the dataframe in session state (a dictionary-like object that persists across
    # page runs). This ensures our data is persisted when the app updates.
    st.session_state.df = df

# Show section to view and edit existing tickets in a table.
st.header("Table")
date_min, date_max = st.slider(
    "Date filter",
    min_value=st.session_state.df["Date"].min(),
    max_value=st.session_state.df["Date"].max(),
    value=(
        st.session_state.df["Date"].min(),
        st.session_state.df["Date"].max(),
    ),
)

# 選択された範囲でデータフレームをフィルター
filtered_df = st.session_state.df[
    (st.session_state.df["Date"] >= date_min)
    & (st.session_state.df["Date"] <= date_max)
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
        x="month(Date):O",
        y="count():Q",
        xOffset="Class:N",
        color="Class:N",
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
    .encode(theta="count():Q", color="Class:N")
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

import streamlit as st
import altair as alt
import pandas as pd
import math
from datetime import datetime
import json

import components

st.set_page_config(layout="wide")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
st.write("https://www.tbank.ru/mybank/")
file = st.file_uploader('Excel')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

df_raw = pd.read_excel(file)
print('---Raw data table---')
print(df_raw)
print(df_raw.info())
df = df_raw.copy()

# Filter only success expensess
df = df[df['Статус'] == 'OK']
df = df[df['Сумма операции'] < 0]
df = df.reset_index()
# Preparing table
df = df[['Дата операции', 'Статус', 'Сумма операции', 'Категория', 'Описание']]
df = df.rename(columns={
    'Дата операции': 'date', 
    'Статус': 'status', 
    'Сумма операции': 'amount', 
    'Категория': 'category', 
    'Описание': 'description'
})
df['date'] = df['date'].map(lambda d: datetime.strptime(d, '%d.%m.%Y %H:%M:%S'))
df['date'] = df['date'].map(lambda d: d.date())
df['amount'] = df['amount'] * -1


# Mapping categories
with open('configs/mapCategories.json') as file:
    super_categories_map = json.load(file)
df['sup_cat'] = df['category'].map(super_categories_map)
df['sup_cat'].fillna('other', inplace=True)
print('---Mapped categories---')
print(df.tail(10))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
st.dataframe(df, use_container_width=True)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Grouping
df_grouped = df.groupby(['sup_cat'])['amount'].sum()
print('---Groupped data---')
print(df_grouped)



# Month graph
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# components.month_graph(df)
components.current_month_category_graph(df)
time_min = st.date_input("Date range", value=(datetime.now()))
components.choosed_month_category_graph(df, time_min)


tiles = []
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)
tiles.extend(row1 + row2 + row3 + row4)



dates= pd.date_range('2024-01-01','2025-01-01' , freq='1M')-pd.offsets.MonthBegin(1)

# for col in row1 + row2 + row3 + row4:
#     with col.container(height=120):
#         st.write('hi')

for i in range(len(tiles)):
    with tiles[i].container():
        components.choosed_month_category_graph(df, dates[i])


# for date in dates:
#     components.choosed_month_category_graph(df, date)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

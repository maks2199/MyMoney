import streamlit as st
import altair as alt
import pandas as pd
import math
from datetime import datetime

import graphs

st.write("https://www.tbank.ru/mybank/")

file = st.file_uploader('Excel')

df_raw = pd.read_excel(file)

# Write to DataBase new raws

print(df_raw)
print(df_raw.info())

df = df_raw.copy()

# Filter only success expensess
df = df[df['Статус'] == 'OK']
df = df[df['Сумма операции'] < 0]
df = df.reset_index()
df = df[['Дата операции', 'Статус', 'Сумма операции', 'Категория', 'Описание']]
df = df.rename(columns={
    'Дата операции': 'date', 
    'Статус': 'status', 
    'Сумма операции': 'amount', 
    'Категория': 'category', 
    'Описание': 'description'
})
df['date'] = df['date'].map(lambda d: datetime.strptime(d, '%d.%m.%Y %H:%M:%S'))
df['amount'] = df['amount'] * -1


# Mapping categories
super_categories_map = {
    'Такси': 'transport',
    'Местный транспорт': 'transport',
    'Ж/д билеты': 'transport',
    'Транспорт': 'transport',
    'Супермаркеты': 'groceries',
    'Фастфуд': 'caffe',
    'Рестораны': 'caffe',
    'Caffe': 'caffe',
    'Переводы': 'transaction',
    'Наличные': 'transaction'
}
df['sup_cat'] = df['category'].map(super_categories_map)
df['sup_cat'].fillna('other', inplace=True)
print(df.tail(10))

st.dataframe(df)


# Grouping
df_grouped = df.groupby(['sup_cat'])['amount'].sum()
print(df_grouped)



# # Visualization
# df_vizualize = df_grouped.copy()
# df_vizualize = df_vizualize.drop('transaction')
# df_vizualize = df_vizualize 
# st.dataframe(df_vizualize)
# st.bar_chart(df_vizualize)




# Month graph
graphs.month_graph(df)

graphs.category_graph(df)


time_min, time_max = st.date_input("Date range", value=(datetime.now(), datetime.now()))


graphs.category_graph_by_time(df, time_min, time_max)
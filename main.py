import streamlit as st
import altair as alt
import pandas as pd
import math
from datetime import datetime

import graphs

df_raw = pd.read_excel('file.xls')

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
    'Супермаркеты': 'groceries',
    'Фастфуд': 'caffe',
    'Рестораны': 'caffe',
    'Переводы': 'transaction',
}
df['sup_cat'] = df['category'].map(super_categories_map)
df['sup_cat'].fillna('other', inplace=True)
print(df.tail(10))



# Grouping
df_grouped = df.groupby(['sup_cat'])['amount'].sum()
print(df_grouped)



# Visualization
df_vizualize = df_grouped.copy()
df_vizualize = df_vizualize.drop('transaction')
df_vizualize = df_vizualize 
st.dataframe(df_vizualize)
st.bar_chart(df_vizualize)




# Month graph
graphs.month_graph(df)

graphs.category_graph(df)

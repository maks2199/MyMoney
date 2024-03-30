import streamlit as st
import pandas as pd

data1 = st.slider('Data1', 1000, 10000, step=1000)
data2 = st.slider('Data2', 1000, 10000, step=1000)
data3 = st.slider('Data3', 1000, 10000, step=1000)

data_dct = {
    'Data1': [data1],
    'Data2': [data2],
    'Data3': [data3],
}

data_list = [data1, data2, data3]

data_df = pd.DataFrame.from_dict(data_dct)


st.table(data_df)
st.bar_chart(data_list)






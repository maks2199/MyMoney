import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import json

def get_current_month_interval():
    now = datetime.now()
    month_start = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)).date()
    nxt_mnth = now.replace(day=28) + timedelta(days=4)
    month_end = (nxt_mnth - timedelta(days=nxt_mnth.day)).date()

    return month_start, month_end

def get_month_interval(date):
    month_start = (date.replace(day=1))
    nxt_mnth = date.replace(day=28) + timedelta(days=4)
    month_end = (nxt_mnth - timedelta(days=nxt_mnth.day))

    return month_start, month_end

def get_current_month_df(df: pd.DataFrame) -> pd.DataFrame:
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).date()
    df_month = df[df['date'] >= month_start]

    return df_month

def slice_df_by_time(df: pd.DataFrame, time_min, time_max) -> pd.DataFrame:
    
    df_month = df[(df['date'] >= pd.to_datetime(time_min).date()) & (df['date'] <= pd.to_datetime(time_max).date())]

    return df_month

# def month_graph(df: pd.DataFrame) -> None:

#     df = df[df['sup_cat'] != 'transaction']

#     # Get only current month
#     current_month_start_date, current_month_end_date = get_current_month_interval()
#     df_month = slice_df_by_time(df, current_month_start_date, current_month_end_date)

#     # Grouping
#     df_month_grouped = df_month.groupby(['sup_cat'])['amount'].sum()
#     total_sum = df_month_grouped.sum()
#     df_month_grouped = df_month_grouped.to_frame()
#     df_month_grouped = df_month_grouped.rename(columns={'amount': 'b-month'})
#     print(df_month_grouped)




#     now = datetime.now()
#     week_start = now + timedelta(days = -now.weekday())
#     week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    

#     df_week = df[df['date'] >= week_start]
#     print(df_week.tail(20))
#     df_week_grouped = df_week.groupby(['sup_cat'])['amount'].sum()
#     df_week_grouped = df_week_grouped.to_frame()
#     df_week_grouped = df_week_grouped.rename(columns={'amount': 'a-week'})
#     print(df_week_grouped)

#     # Merge
#     df_merged = df_month_grouped.merge(df_week_grouped,  left_index=True, right_index=True)
#     print(df_merged)


#     # Visualize
#     with st.container(border=True):
#         st.write('# This month expenses')
#         st.bar_chart(df_merged)
#         st.markdown(f'## {"{:,}".format(round(total_sum)).replace(',',' ')} ₽')


if __name__ == '__main__':
    now = datetime.now()
    week_start = now + timedelta(days = -now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    print(week_start)

def current_month_category_graph(df: pd.DataFrame):
    current_month_start_date, current_month_end_date = get_current_month_interval()
    month_category_graph(df, current_month_start_date, current_month_end_date)

def choosed_month_category_graph(df, start_date):
    month_start, month_end = get_month_interval(start_date)
    month_category_graph(df, month_start, month_end)

def month_category_graph(df, month_start_date, month_end_date):
    df = df[df['sup_cat'] != 'transaction']

    # # Get only current month
    # current_month_start_date, current_month_end_date = get_current_month_interval()
    df_month = slice_df_by_time(df, month_start_date, month_end_date)

    
    # Pivoting
    df_month_grouped = df_month[['date','amount','sup_cat']].groupby(by=['sup_cat','date']).sum()
    df_month_grouped = df_month_grouped.reset_index()
    total_sum = df_month_grouped['amount'].sum()
    df_month_pivoted = df_month_grouped.pivot(index='date', columns='sup_cat', values='amount')
    df_month_pivoted = df_month_pivoted.fillna(0)
    

    # Cumsum
    df_summed = df_month_pivoted.cumsum()

    # FOOD summary
    if '1_caffe' not in df_summed:
        df_summed['1_caffe'] = 0.0
    if '2_groceries' not in df_summed:
        df_summed['2_groceries'] = 0.0
    df_summed['FOOD'] = df_summed['1_caffe'] + df_summed['2_groceries']
    print('---Month summary table---')
    print(df_summed)



    # Visualize
    fig_fact = px.line(df_summed)

    # Planned lines
    with open('configs/plannedExpenses.json') as file:
        planned_expenses = json.load(file)
    plan_table = {'date': [month_start_date, month_end_date]}
    for key, value in planned_expenses.items():
        plan_table[key] = [0, value]
    plan = pd.DataFrame(plan_table)
    plan = plan.set_index(['date'])
    print('---Planned table---')
    print(plan)


    fig_plan = px.line(plan)
    fig_fact.add_traces(fig_plan.data)
    fig_fact.update_traces(patch={"line": {"dash": "dot"}}, selector=lambda x: True if 'p_' in x.name else False)
    fig_fact.update_traces(line=dict(width=5.0))


    with st.container(border=True):
        st.write(f'# :blue[{month_start_date.strftime("%B")}] expenses: {"{:,}".format(round(total_sum)).replace(',',' ')} ₽')
        st.plotly_chart(fig_fact, use_container_width=True)





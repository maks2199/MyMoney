import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px

def get_current_month_df(df: pd.DataFrame) -> pd.DataFrame:
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    df_month = df[df['date'] >= month_start]

    return df_month

def get_df_by_time(df: pd.DataFrame, time_min, time_max) -> pd.DataFrame:
    
    df_month = df[(df['date'] >= pd.to_datetime(time_min)) & (df['date'] <= pd.to_datetime(time_max))]

    return df_month

def month_graph(df: pd.DataFrame):
    print('month graph')

    df = df[df['sup_cat'] != 'transaction']

    # Get only current month
    df_month = get_current_month_df(df)
    

    # Grouping
    print(df_month.tail(10))
    df_month_grouped = df_month.groupby(['sup_cat'])['amount'].sum()
    total_sum = df_month_grouped.sum()
    df_month_grouped = df_month_grouped.to_frame()
    df_month_grouped = df_month_grouped.rename(columns={'amount': 'b-month'})
    print(df_month_grouped)




    now = datetime.now()
    week_start = now + timedelta(days = -now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    

    df_week = df[df['date'] >= week_start]
    print(df_week.tail(20))
    df_week_grouped = df_week.groupby(['sup_cat'])['amount'].sum()
    df_week_grouped = df_week_grouped.to_frame()
    df_week_grouped = df_week_grouped.rename(columns={'amount': 'a-week'})
    print(df_week_grouped)

    # Merge
    df_merged = df_month_grouped.merge(df_week_grouped,  left_index=True, right_index=True)
    print(df_merged)


    # Visualize
    st.bar_chart(df_merged)
    st.markdown(f'## {"{:,}".format(round(total_sum)).replace(',',' ')} ₽')

    return df_merged

if __name__ == '__main__':
    now = datetime.now()
    week_start = now + timedelta(days = -now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    print(week_start)

def category_graph(df):
    print('catgory graph')

    df = df[df['sup_cat'] != 'transaction']

    # Get only current month
    df_month = get_current_month_df(df)

    # Format date by day
    df_month['date'] = df_month['date'].map(lambda d: d.date())
    print(df_month.tail(10))

    # Pivoting
    df_month_grouped = df_month[['date','amount','sup_cat']].groupby(by=['sup_cat','date']).sum()
    df_month_grouped = df_month_grouped.reset_index()
    print(df_month_grouped)
    df_month_pivoted = df_month_grouped.pivot(index='date', columns='sup_cat', values='amount')
    df_month_pivoted = df_month_pivoted.fillna(0)
    print(df_month_pivoted)

    # Cumsum
    df_summed = df_month_pivoted.cumsum()
    print(df_summed)



    # Visualize
    fig = px.line(df_summed)

    ## Month's first and last days
    now = datetime.now()
    month_start = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)).date()
    nxt_mnth = now.replace(day=28) + timedelta(days=4)
    month_end = (nxt_mnth - timedelta(days=nxt_mnth.day)).date()
    print('month dates:', month_start, month_end)


    plan = pd.DataFrame({
    'date': [month_start, month_end],
    'caffe_p': [0, 20000],
    'groceries_p': [0, 30000],
    'other_p': [0, 4000],
    'transport_p': [0, 6000],
    })

    plan = plan.set_index(['date'])
    print('plan')
    print(plan)


    fig2 = px.line(plan)

    # for d in fig2.data:
        # fig.add_trace(d)
    fig.add_traces(fig2.data)
    # fig.add_scatter(x=plan['date'], y=plan['caffe'], mode='lines')
    # fig.update_layout(title='Stock vs Prediction', xaxis_title='Date', yaxis_title='Value')
    fig.update_traces(patch={"line": {"dash": "dot"}}, selector=lambda x: True if '_p' in x.name else False)
    fig.update_traces(line=dict(width=5.0))



    st.plotly_chart(fig, use_container_width=True)


def category_graph_by_time(df, time_min, time_max):
    print('catgory graph')

    df = df[df['sup_cat'] != 'transaction']

    # Get only current month
    df_month = get_df_by_time(df, time_min, time_max)

    # Format date by day
    df_month['date'] = df_month['date'].map(lambda d: d.date())
    print(df_month.tail(10))

    # Pivoting
    df_month_grouped = df_month[['date','amount','sup_cat']].groupby(by=['sup_cat','date']).sum()
    df_month_grouped = df_month_grouped.reset_index()
    print(df_month_grouped)
    df_month_pivoted = df_month_grouped.pivot(index='date', columns='sup_cat', values='amount')
    df_month_pivoted = df_month_pivoted.fillna(0)
    print(df_month_pivoted)

    # Cumsum
    df_summed = df_month_pivoted.cumsum()
    print(df_summed)



    # Visualize
    fig = px.line(df_summed)

    ## Month's first and last days


    plan = pd.DataFrame({
    'date': [time_min, time_max],
    'caffe_p': [0, 20000],
    'groceries_p': [0, 30000],
    'other_p': [0, 4000],
    'transport_p': [0, 6000],
    })

    plan = plan.set_index(['date'])
    print('plan')
    print(plan)


    fig2 = px.line(plan)

    # for d in fig2.data:
        # fig.add_trace(d)
    fig.add_traces(fig2.data)
    # fig.add_scatter(x=plan['date'], y=plan['caffe'], mode='lines')
    # fig.update_layout(title='Stock vs Prediction', xaxis_title='Date', yaxis_title='Value')
    fig.update_traces(patch={"line": {"dash": "dot"}}, selector=lambda x: True if '_p' in x.name else False)
    fig.update_traces(line=dict(width=5.0))



    st.plotly_chart(fig, use_container_width=True)


import pandas as pd
from datetime import datetime, timedelta


def month_graph(df: pd.DataFrame):
    print('month graph')

    df = df[df['sup_cat'] != 'transaction']

    # Get only current month
    now = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    print('month start:', month_start)
    df_month = df[df['date'] >= month_start]
    

    # Grouping
    print(df_month.tail(10))
    df_month_grouped = df_month.groupby(['sup_cat'])['amount'].sum()
    df_month_grouped = df_month_grouped.to_frame()
    df_month_grouped = df_month_grouped.rename(columns={'amount': 'b-month'})
    print(df_month_grouped)




    now = datetime.now()
    week_start = now + timedelta(days = -now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    

    df_week = df[df['date'] >= week_start]
    print(df_week.tail(10))
    df_week_grouped = df_week.groupby(['sup_cat'])['amount'].sum()
    df_week_grouped = df_week_grouped.to_frame()
    df_week_grouped = df_week_grouped.rename(columns={'amount': 'a-week'})
    print(df_week_grouped)

    # Merge
    df_merged = df_month_grouped.merge(df_week_grouped,  left_index=True, right_index=True)
    print(df_merged)

    return df_merged

if __name__ == '__main__':
    now = datetime.now()
    week_start = now + timedelta(days = -now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    print(week_start)
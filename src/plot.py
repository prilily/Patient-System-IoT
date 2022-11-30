import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

def plot():
    my_health_data=pd.read_csv('/home/milano/Desktop/CSE4.1/iot/multipage-streamlit/apple.csv',parse_dates=['Date'])
    #df.info()

    st.title('HEART RATE over the year')

    #visualizing heartrate over time
    fig, ax = plt.subplots(figsize = (20, 8))
    chart = sns.lineplot(x='Date', y='Heart rate(count/min)', data=my_health_data)
    ax.set_title("Distance walked or ran in the past year (source: Apple Health Data)", loc='left', fontdict={'fontsize':20})
    st.pyplot(fig)

    st.error("ALERT!! **Days when heartbeat rose above 120 BPS**")
    my_health_data['Heart rate(count/min)']=pd.to_numeric(my_health_data['Heart rate(count/min)'],errors = 'coerce')
    temp=my_health_data.query("`Heart rate(count/min)`>120")
    st.write(temp[['Date','Heart rate(count/min)','Walking heart rate average(count/min)']])

    st.title('Distance WALKED/RUN the year')
    #visualizing distance over time
    fig, ax = plt.subplots(figsize = (20, 8))
    chart = sns.lineplot(x='Date', y='Distance walking / running(km)', data=my_health_data)
    ax.set_title("Distance walked or ran in the past year (source: Apple Health Data)", loc='left', fontdict={'fontsize':20})
    st.pyplot(fig)

    st.title('ROLLING MEAN Distance WALKED/RUN the year')
    rolling_mean = my_health_data['Distance walking / running(km)'].rolling(window=7).mean()
    rolling_mean2 = my_health_data['Distance walking / running(km)'].rolling(window=30).mean()

    fig, ax = plt.subplots(figsize = (20, 6))
    chart = sns.lineplot(x='Date', y='Distance walking / running(km)', data=my_health_data)
    chart2 = sns.lineplot(x='Date', y=rolling_mean, label='Rolling weekly average',data=my_health_data, color='red')
    chart2 = sns.lineplot(x='Date', y=rolling_mean2, label='Rolling monthly average',data=my_health_data, color='orange')
    ax.set_title("Distance walked or ran in the past year (source: Apple Health Data)", loc='left', fontdict={'fontsize':20})
    ax.xaxis.grid()

    st.pyplot(fig)

    # creating a 'day of the week' column
    my_health_data['dow'] = my_health_data['Date'].dt.strftime('%A')

    # grouping by 'dow'
    days_grouped = my_health_data.groupby('dow')
    

    # exploring distance by dow
    distance_by_dow = days_grouped['Distance walking / running(km)']
    distance_by_dow = pd.DataFrame(distance_by_dow.agg([np.min, np.max, np.mean]))
    distance_by_dow = distance_by_dow.reset_index()
    st.title('Distance WALKED/RUN the year WEEK DAY WISE')
    st.success("Most active on : Saturday")
    # changing days to numbers to preserve order when plotted
    days_num = {"Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4, "Friday":5, "Saturday":6, "Sunday":7}
    distance_by_dow["dow_num"] = distance_by_dow["dow"].map(days_num)

    # list to correct numbers back to day
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sun"]

    fig, ax = plt.subplots(figsize = (15, 6))
    chart=sns.barplot(x='dow_num', y='mean', data=distance_by_dow)
    chart.set_xticklabels(days)
    ax.set_xlabel('')
    ax.set_title("Mean distance by day of week (source: Apple Health Data)", loc='left', fontdict={'fontsize':20})
    st.pyplot(fig)


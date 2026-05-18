import streamlit as st
import pandas as pd
import plotly.express as px


def load_data():
    return pd.read_csv('jobs.csv')
df = load_data()
st.title('Machine Learning Graduate Jobs Dashboard')
df['Location'] = df['Location'].replace(['Mount Waverley', 'South Yarra'], 'Melbourne VIC')

city_counts = df['Location'].value_counts()
city_counts = city_counts[city_counts > 1].reset_index()
city_counts.columns = ['city', 'jobs']

fig = px.bar(city_counts, x='city', y='jobs', title='Jobs per City (>1)')
st.plotly_chart(fig)

salary_df = df.copy()

salary_df = salary_df[salary_df['Salary'].notna()]
salary_df = salary_df[salary_df['Salary'] != 'Not listed']

# extract number and optional 'k'
salary_df[['num', 'k']] = salary_df['Salary'].str.extract(r'(\d+[\d,]*)([kK]?)')

# clean and convert number
salary_df['num'] = salary_df['num'].str.replace(',', '', regex=False)
salary_df['num'] = pd.to_numeric(salary_df['num'], errors='coerce')

# apply multiplier if 'k' exists
salary_df['Salary_num'] = salary_df['num']
salary_df.loc[salary_df['k'].str.lower() == 'k', 'Salary_num'] *= 1000

# drop invalid rows
salary_df = salary_df[salary_df['Salary_num'].notna()]

# histogram
fig = px.histogram(salary_df, x='Salary_num', nbins=20, title='Salary Distribution')
st.plotly_chart(fig)
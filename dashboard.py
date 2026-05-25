import streamlit as st
import pandas as pd
import plotly.express as px


def load_data():
    return pd.read_csv('jobs_with_desc.csv')
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

# ---------------- SKILLS ANALYSIS ----------------

# define skills to track
skills = [
    'python', 'sql', 'machine learning', 'deep learning',
    'tensorflow', 'pytorch', 'pandas', 'numpy',
    'aws', 'azure', 'gcp', 'docker', 'git'
]

# make sure Description exists and is usable
df['Description'] = df['Description'].fillna('').str.lower()

# count skills
skill_counts = {}

for skill in skills:
    skill_counts[skill] = df['Description'].str.contains(skill, case=False, na=False).sum()

# convert to dataframe
skills_df = pd.DataFrame(list(skill_counts.items()), columns=['skill', 'count'])

# sort descending
skills_df = skills_df.sort_values(by='count', ascending=False)

# plot
fig = px.bar(skills_df, x='skill', y='count', title='Most In-Demand Skills')
st.plotly_chart(fig)
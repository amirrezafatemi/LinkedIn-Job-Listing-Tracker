import streamlit as st
import pandas as pd
import os

os.system("python tracker.py")

def adding_data():
    pass

st.title("Filtering Page")

data = {
    "ops" : ["Job titles", "Company", "Location", "Link"], # bayad etelaat ro be inja ezafe konam
    }


df = pd.DataFrame(data)

# df = pd.read_csv("layout\\pages\\csvfile.csv")

selected_categories = st.multiselect('Select Filters', options=df['ops'].unique())

if selected_categories:
    filtered_df = df[df['ops'].isin(selected_categories)]
    st.write('Filtered Data:')
    st.dataframe(filtered_df)
else:
    st.write('Please select at least one filter.')



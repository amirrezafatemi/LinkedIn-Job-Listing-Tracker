import streamlit as st


st.set_page_config(
    page_title="Job Tracker",
    page_icon=":material/mystery:",
)


st.markdown(
"""
With this program, you can search the job opportunities
through Linkedin network.
Enter the job title you are looking for with the number of results you want.
For instance, you currently looking for "Data Scientist"
and you only need 10 out of all searched results.
"""
)

with st.form(label="Search page", enter_to_submit=False):
    jobtitle = st.text_input(label="Job Title")
    resultcount = st.text_input(label="How many results should be shown?")












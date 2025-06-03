import streamlit as st

LOGIN_DIR = r"layout\\user_data\\search.txt"

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

def saving_data(jt, rc):
    with open(LOGIN_DIR, "r+") as f:
        f.write(jt)
        f.write("\n")
        f.write(rc)


with st.form("Search page", enter_to_submit=False):
    jobtitle = st.text_input(label="Job Title")
    jobtitle = jobtitle.replace(" ", "%20")
    resultcount = st.text_input(label="How many results should be shown?")
    saving_data(jobtitle, resultcount)
    submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        st.switch_page("pages/filter.py")












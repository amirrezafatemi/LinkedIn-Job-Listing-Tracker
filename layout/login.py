import streamlit as st


st.title("LinkedIn Job Listing Tracker")
with st.form("Login page"):

    email = st.text_input("Email", icon=":material/mail:")
    password = st.text_input("Password", type="password", icon=":material/key:")

    st.form_submit_button(label="Submit")

st.write("outside")
# st.page_link("app.py", label="The App", icon=":material/Login:")









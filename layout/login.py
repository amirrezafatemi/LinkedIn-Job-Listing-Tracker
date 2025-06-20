import streamlit as st

LOGIN_DIR = r"layout\\user_data\\login.txt"

def saving_data(email, psswd):
    with open(LOGIN_DIR, "r+") as f:
        f.write(email)
        f.write("\n")
        f.write(psswd)




st.set_page_config(
    page_title="Login",
    page_icon=":material/login:",
)

st.title("LinkedIn Job Listing Tracker")

with st.form("Login page", clear_on_submit=True, enter_to_submit=False):

    email = st.text_input("Email", value="test@mail.com", icon=":material/mail:")
    password = st.text_input("Password", value="1234567", type="password", icon=":material/key:")
    saving_data(email, password)
    submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        st.switch_page("pages/app.py")











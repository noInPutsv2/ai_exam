import streamlit as st # type: ignore
from streamlit_option_menu import option_menu # type: ignore
import pandas as pd
import user_db_operations as udb
import MongoDB as mdb


if 'admin' not in st.session_state:
            st.session_state['admin'] = None
def Logs():
    st.title("Login logs")
    data_df = udb.get_logs()
    st.write("seach for user:")
    id = st.text_input("search")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("search"):
            data_df = udb.get_user_logs(id)
    with col2:
        if st.button("Clear search"):
            data_df = udb.get_logs()
    
    st.dataframe(data_df, width=1000, hide_index = True) 
    

def users():
    st.title("Users")
    data_df = udb.get_users()
    row = st.dataframe(data_df, width=1000, hide_index = True)
    id = st.number_input(label = "see number of chats for each user", step = None, format = "%d")
    if st.button("search"):
        for i in mdb.get_number_of_chats(id):
            st.write(i)

def test():
    st.write(st.session_state["admin"])

if st.session_state["admin"]:
    with st.sidebar:
        selected = option_menu("See:", ["Users", 'Logs'], default_index=1)
        if st.button("Logout"):
            st.session_state["admin"] = None
            st.rerun()

    if selected == "Users":
        users()
        
    elif selected == "Logs":
        Logs()
    
else:
    admin_login_form = st.form('Admin Login')
    admin_login_form .subheader('Admin Login')
    username = admin_login_form .text_input('Username').lower()
    password = admin_login_form .text_input('Password',type='password')
    if admin_login_form.form_submit_button('Login'):
        if username and password:
            if udb.admin_login(username, password):
                st.session_state["admin"] = True
                st.rerun()
            else:
                st.error("Username or password is incorrect")
    if st.button("Back to main page"):
        st.switch_page("main.py")
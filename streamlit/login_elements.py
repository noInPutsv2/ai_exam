import streamlit as st # type: ignore
import user_db_operations as db

def check_credentials(username, password):
      return db.check_login(username, password)


def Set_session_state(username, userid, state):
    st.session_state['username'] = username
    st.session_state['userid'] = userid
    st.session_state['authentication_status'] = state


def login_form():
    login_form = st.sidebar.form('Login')
    login_form.subheader('Login')
    username = login_form.text_input('Username').lower()
    password = login_form.text_input('Password',type='password')
    if login_form.form_submit_button('Login'):
        login(username, password)
    if login_form.form_submit_button('Create Account'):
            st.switch_page("pages/create_user_page.py")


def login(username, password):
    userid = check_credentials(username, password)
    if userid:
        db.add_to_logs(userid, 1)
        Set_session_state(username, userid, True)
        #self.cookie_handler.set_cookie()
    else:
        Set_session_state(None, None, False)

def logout():
     if st.button('logout'):
        db.add_to_logs(st.session_state['userid'], 0)
        Set_session_state(None, None, None)
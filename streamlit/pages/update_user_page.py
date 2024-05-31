import streamlit as st # type: ignore
from streamlit_option_menu import option_menu # type: ignore
import user_db_operations as db
import login_elements as le


def update_password():
    register_user_form = st.form('update password')

    register_user_form.subheader('update password')
    new_password = register_user_form.text_input('Password',type='password')
    new_password_repeat = register_user_form.text_input('Repeat password',type='password')
    if register_user_form.form_submit_button('update'):
        if new_password and new_password_repeat:
            if new_password == new_password_repeat:
                db.change_password(st.session_state['userid'], new_password_repeat)
                st.success('Password updated successfully')

def update_email():
    register_user_form = st.form('update email')

    register_user_form.subheader('update email')
    new_email = register_user_form.text_input('Email').lower()
    if register_user_form.form_submit_button('update'):
        if new_email:
            db.change_email(st.session_state['userid'], new_email)
            st.success('Email updated successfully')


@st.experimental_dialog("Delete account")
def Delete_user():
    st.write(f"Are you sure you want to delete your account?")
    
    if st.button("Yes I'm sure"):
        db.delete_user(st.session_state['userid'])
        le.logout()
        st.switch_page("main.py")

with st.sidebar:
    selected = option_menu("Change:", ["Email", 'Password'], default_index=1)
    
    if st.button(label = "Delete account"):
        Delete_user()   
    if st.button(label = "Go Back"):
        st.switch_page("main.py")


if st.session_state["authentication_status"]:
    if selected == "Email":
        update_email()
    elif selected == "Password":
        update_password()


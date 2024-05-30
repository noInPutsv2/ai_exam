import streamlit as st # type: ignore
import user_db_operations as db
import login_elements as le


register_user_form = st.form('Register user')

register_user_form.subheader('Register User')
new_email = register_user_form.text_input('Email').lower()
new_username = register_user_form.text_input('Username').lower()
new_password = register_user_form.text_input('Password',type='password')
new_password_repeat = register_user_form.text_input('Repeat password',type='password')
if register_user_form.form_submit_button('Register'):
    if new_email and new_username and new_password and new_password_repeat:
        if new_password == new_password_repeat:
            if db.check_username(new_username):
                if db.register_user(new_email, new_username, new_password):
                    st.success('User registered successfully')
                    le.login(new_username, new_password)
                    st.switch_page("main.py")
            else:
                st.error('Username already exists')
        else:
            st.error('Passwords do not match')
        

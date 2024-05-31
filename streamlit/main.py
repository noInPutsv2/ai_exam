import streamlit as st # type: ignore
from streamlit_option_menu import option_menu # type: ignore
import login_elements as le
from yaml.loader import SafeLoader # type: ignore
import chatbot


if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None


ravenclaw = 'Ravenclaw-logo.png'
gryffindor = 'Gryffindor-logo.png'
slytherin = 'Slytherin-logo.png'
hufflepuff = 'Hufflepuff-logo.png'

assistent = "WW_Hero_Image.jpg"

#reset chat history
def reset():
    st.session_state.messages = []

#choose avatar icon
with st.sidebar:
    if st.session_state["authentication_status"] is False or st.session_state["authentication_status"] is None:
        le.login_form()
    if st.session_state["authentication_status"] is True:
        selected = option_menu("Choose your house", ["Gryffindor", 'Slytherin', 'Hufflepuff', 'Ravenclaw'],  
                        menu_icon = 'house-heart', icons=['house', 'house', 'house', 'house'], default_index=3)
        if selected == "Gryffindor":
            user = gryffindor
        elif selected == "Slytherin":
            user = slytherin
        elif selected == "Hufflepuff":
            user = hufflepuff
        else:
            user = ravenclaw
        le.logout()
        if st.button("Change password"):
            st.switch_page("pages/Change_password_page.py")
        st.button(label = "Clear conversation", on_click = reset)
    
    

## Main page
if st.session_state["authentication_status"]:
    st.write(f'Welcome *{st.session_state["username"]}*')
    chatbot.Show(user, assistent)
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


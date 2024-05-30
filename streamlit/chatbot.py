import streamlit as st # type: ignore
import random
import time
import getDb

def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def Show(user, assistent):
    # Set page title
    st.title("Harry Potter Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message(name = message["role"], avatar = user):
                st.markdown(message["content"])
        else:
            with st.chat_message(name = message["role"], avatar = assistent):
                st.markdown(message["content"])
    

    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user",  avatar = user):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "avatar": user , "content": prompt})

        with st.chat_message("assistant"):
            response = st.write(getDb.ask_question(prompt))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "avatar": assistent,  "content": response})

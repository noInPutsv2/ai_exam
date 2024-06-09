import streamlit as st # type: ignore
import random
import time
import getDb
import MongoDB as mdb

def makeChatHistory(items, user, assistent):
    for i in items:
        st.session_state.messages.append({"role": "user", "avatar": user, "content": i["user_input"]})
        st.session_state.messages.append({"role": "assistant", "avatar": assistent, "content": i["chatbot_response"]})

def stream_text(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.2)

def Show(user, assistent):
    # Set page title
    st.title("Harry Potter Chatbot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        makeChatHistory(mdb.GetChatHistory(st.session_state['userid']), user, assistent)
    

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
            with st.spinner("I'm thinking..."):
                start = time.time()
                response = getDb.ask_question(prompt)
                end = time.time()
            st.write_stream(stream_text(str(response)))
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "avatar": assistent,  "content": response})
        times = (end - start)/60
        mdb.InsertChatHistory(st.session_state['userid'], prompt, response, times)

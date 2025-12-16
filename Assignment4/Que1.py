import streamlit as st
import time

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def stream_reply(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.3)

user_msg = st.chat_input("Type your message")

if user_msg:
    st.session_state.messages.append(
        {"role": "user", "content": user_msg}
    )
    with st.chat_message("user"):
        st.write(user_msg)

    reply = f"You said: {user_msg}"

    with st.chat_message("assistant"):
        st.write_stream(stream_reply(reply))

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

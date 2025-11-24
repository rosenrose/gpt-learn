import streamlit as st
import time

st.title("Document GPT")
st.session_state["messages"] = st.session_state.get("messages", [])


def send_message(message, role, is_save=True):
    with st.chat_message(role):
        st.write(message)

    if is_save:
        st.session_state["messages"].append({"message": message, "role": role})


for message in st.session_state["messages"]:
    send_message(message["message"], message["role"], is_save=False)

message = st.chat_input("Send msg")

if message:
    send_message(message, "human")
    time.sleep(2)
    send_message(f"You said: {message}", "ai")

    with st.sidebar:
        st.write(st.session_state)

import streamlit as st
import requests

st.title("🧵 TailorTalk - AI Calendar Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        res = requests.post("http://localhost:8000/chat/", json={"message": user_input})
        bot_reply = res.json()["response"]
        st.session_state.chat_history.append(("TailorTalk", bot_reply))
        user_input = ""

for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**TailorTalk:** {msg}")
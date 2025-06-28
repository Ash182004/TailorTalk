import streamlit as st
import requests

st.title("🧵 TailorTalk - AI Calendar Assistant")

# ✅ Update with your actual backend FastAPI Render URL
API_URL = "https://tailortalk-2-ixq1.onrender.com/chat/"

# ✅ Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Text input for user
user_input = st.text_input("You:", "")

# ✅ When Send button is clicked
if st.button("Send"):
    if user_input:
        # Save user input to chat history
        st.session_state.chat_history.append(("You", user_input))

        try:
            # Call backend FastAPI
            res = requests.post(API_URL, json={"message": user_input})

            if res.status_code == 200:
                bot_reply = res.json().get("response", "No response from TailorTalk.")
            else:
                bot_reply = f"Backend Error ({res.status_code})"

        except Exception as e:
            bot_reply = f"Error connecting to backend: {str(e)}"

        # Save bot reply to chat history
        st.session_state.chat_history.append(("TailorTalk", bot_reply))

# ✅ Display full chat history
for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**TailorTalk:** {msg}")

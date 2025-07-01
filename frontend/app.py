import streamlit as st
import requests

st.set_page_config(page_title="Calendar Booking Bot", page_icon="📅")
st.title("📅 Calendar Booking Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Type your request...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post("http://localhost:8000/chat", json={"message": user_input})
                reply = res.json().get("response", "❌ No response.")
            except Exception as e:
                reply = f"❌ Error: {e}"

            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

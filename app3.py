import os
import streamlit as st
from google import genai

# Load API Key (from environment variable)
api_key = os.getenv("API_KEY")

client = genai.Client(api_key="AIzaSyAcXuFqLM3_KDgrGHMZe9McOKimRJCprVA")

# Initialize Gemini client
#client = genai.Client(api_key=api_key)

st.title("🤖 Turing-Style Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

# Get user input
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append(("user", prompt))
    st.chat_message("user").write(prompt)

    # AI Response
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    bot_reply = response.text

    st.session_state.messages.append(("assistant", bot_reply))
    st.chat_message("assistant").write(bot_reply)

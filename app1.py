import streamlit as st
import google.generativeai as genai
import os

# ------------------------------
# Gemini API Setup
# ------------------------------
# Option A: Use environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

# Option B: (testing only) paste your key directly
API_KEY = "AIzaSyAcXuFqLM3_KDgrGHMZe9McOKimRJCprVA"

if not API_KEY:
    st.error("❌ No API key found! Set GOOGLE_API_KEY as env variable or paste directly in code.")
else:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # ------------------------------
    # Streamlit UI
    # ------------------------------
    st.set_page_config(page_title="Elder Companion Chatbot", page_icon="🤖")

    st.title("🤖 Elder Companion Chatbot")
    st.write("Hello 👋 I’m here to chat with you and keep you company!")

    # Keep chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Say something..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get Gemini response
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                bot_reply = response.text
                st.markdown(bot_reply)
            except Exception as e:
                bot_reply = f"⚠️ Error: {e}"
                st.error(bot_reply)

        # Save bot reply
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

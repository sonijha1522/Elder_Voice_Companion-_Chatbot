import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
from gtts import gTTS
import tempfile

# ------------------------------
# Gemini API Setup
# ------------------------------
API_KEY = "AIzaSyD0gUrWD42YEuu5m2TmRldsuQiD7-l0R3c"   # or use os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Elder Voice Companion", page_icon="🎤")
st.title("🎤 Elder Voice Companion Chatbot")

# ------------------------------
# Voice Input Function
# ------------------------------
def listen_microphone():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("🎙️ Listening... Speak now")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "❌ Sorry, I couldn't understand."
    except sr.RequestError:
        return "⚠️ Speech Recognition API unavailable."

# ------------------------------
# Text-to-Speech Function
# ------------------------------
def speak_text(text):
    tts = gTTS(text=text, lang="en")
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp_file.name)
    return tmp_file.name

# ------------------------------
# Chat Memory
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🎤 Button for voice input
if st.button("🎙️ Speak"):
    user_input = listen_microphone()
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Gemini response
    response = model.generate_content(user_input)
    bot_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # 🔊 Play voice output
    audio_file = speak_text(bot_reply)
    st.audio(audio_file, format="audio/mp3")

# ✍️ Also allow normal typing
if prompt := st.chat_input("Or type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = model.generate_content(prompt)
    bot_reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    audio_file = speak_text(bot_reply)
    st.audio(audio_file, format="audio/mp3")

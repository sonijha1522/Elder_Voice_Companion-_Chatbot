import streamlit as st
import sounddevice as sd
import numpy as np
import soundfile as sf
import speech_recognition as sr
from gtts import gTTS
from google import genai

# ---------------------------
# 1. Load Gemini API Key
# ---------------------------

api_key = "AIzaSyAcXuFqLM3_KDgrGHMZe9McOKimRJCprVA"
# Initialize Gemini client
client = genai.Client(api_key=api_key)

# ---------------------------
# 2. Streamlit UI
# ---------------------------
st.title("🎤 Voice-enabled Gemini Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

# ---------------------------
# 3. Audio Handling
# ---------------------------
def record_audio(filename="input.wav", duration=5, fs=44100):
    """Record voice from mic and save to wav"""
    st.info("🎙️ Recording... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    sf.write(filename, recording, fs)   # using soundfile (not wavio)
    return filename

def speech_to_text(audio_file):
    """Convert recorded audio to text"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None

def speak(text, filename="response.mp3"):
    """Convert text to speech and play"""
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    st.audio(filename, format="audio/mp3")

# ---------------------------
# 4. User Input Options
# ---------------------------
col1, col2 = st.columns(2)
with col1:
    mic_input = st.button("🎙️ Speak")
with col2:
    text_input = st.text_input("💬 Or type your message:")

user_text = None

if mic_input:
    audio_file = record_audio()
    user_text = speech_to_text(audio_file)
    if user_text:
        st.success(f"🧑 You said: {user_text}")
    else:
        st.warning("❌ Couldn't understand. Try again.")

if text_input:
    user_text = text_input

# ---------------------------
# 5. Chatbot Response
# ---------------------------
if user_text:
    # Save user msg
    st.session_state.messages.append(("user", user_text))
    st.chat_message("user").write(user_text)

    # Gemini AI response
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=user_text
    )
    bot_reply = response.text

    # Save assistant msg
    st.session_state.messages.append(("assistant", bot_reply))
    st.chat_message("assistant").write(bot_reply)

    # Speak reply
    speak(bot_reply)

import streamlit as st
import json
import os
from datetime import datetime
from google import genai

# Initialize Gemini client (requires GOOGLE_API_KEY env var)
client = genai.Client(api_key=os.getenv("AIzaSyCqFuILLv1cp82ZD1pxupRhp9xWcuJGpvQ"))

# Memory file
MEMORY_FILE = "elder_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

# Initialize memory
memory = load_memory()

st.set_page_config(page_title="Elder Companion Chatbot", page_icon="💬", layout="centered")
st.title("💬 Elder Companion Chatbot")
st.write("I’m here to chat with you, share stories, and keep you company.")

# User input for name
if "name" not in memory:
    name = st.text_input("What’s your name?")
    if name:
        memory["name"] = name
        save_memory(memory)
        st.success(f"Hello {name}, nice to meet you! 👋")
else:
    st.write(f"👋 Hello again, {memory['name']}!")

# Sidebar for mood check-in
with st.sidebar:
    st.header("🌼 Daily Check-in")
    mood = st.slider("How are you feeling today?", 0, 10, 5)
    loneliness = st.slider("How lonely are you feeling right now?", 0, 10, 5)
    if st.button("Save Check-in"):
        memory.setdefault("checkins", []).append({
            "time": str(datetime.now()),
            "mood": mood,
            "loneliness": loneliness
        })
        save_memory(memory)
        st.success("Check-in saved. Thank you!")

# Chat interface
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Type your message here:")
if st.button("Send") and user_input:
    st.session_state.chat_history.append(("You", user_input))

    # Detect emergency keywords
    emergency_words = ["suicide", "kill myself", "want to die", "hurt myself"]
    if any(word in user_input.lower() for word in emergency_words):
        bot_reply = "⚠️ I’m really concerned. Please reach out to a caregiver or call your local emergency number immediately. You are not alone."
    else:
        # Use Gemini for reply
        prompt = """
        You are a compassionate elder companion chatbot. Respond warmly, in simple short sentences.
        The user may be lonely. Offer gentle support, light stories, or calming exercises.
        Avoid medical advice. If serious distress, advise contacting family or emergency.
        User message: {user_msg}
        """.format(user_msg=user_input)

        response = client.models.generate(
            model="gemini-1.5-flash",
            contents=[prompt]
        )
        bot_reply = response.text

    st.session_state.chat_history.append(("Bot", bot_reply))

# Display chat history
for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑‍🦳 {speaker}:** {msg}")
    else:
        st.markdown(f"**🤖 {speaker}:** {msg}")

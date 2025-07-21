import streamlit as st
from groq import Groq
import os

# --- 1. Configuration ---
# Load API key from Streamlit secrets or environment
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

# Validate the API key
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found. Please add it to .streamlit/secrets.toml")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Set system instructions for chat
SYSTEM_PROMPT = "You are a helpful assistant. Answer all user questions conversationally."

# --- 2. Page Layout ---
st.set_page_config(page_title="Piyush Chatbot", layout="wide")
st.title("🤖 PIYUSH CHATBOT")

# --- 3. Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Display chat
for msg in st.session_state.chat_history[1:]:  # Skip system prompt
    role = msg["role"]
    with st.chat_message(role):
        st.markdown(msg["content"])

# --- 4. User Input Box ---
if prompt := st.chat_input("Type your message and press Enter"):
    # Save user input
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get model response from Groq
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",  # Or llama3-70b-8192
                    messages=st.session_state.chat_history,
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"❌ Error: {e}"
        
        st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})






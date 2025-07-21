import streamlit as st
import requests
import os

# --- 1. Configuration ---
# Load API key from .env if running locally
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"  # You can try e.g. 'llama3-70b-8192' or other available models

SYSTEM_PROMPT = "You are a helpful assistant. Answer all user questions conversationally."

st.set_page_config(page_title="Chatbot", layout="wide")
st.title("🤖 PIYUSH CHATBOT ")

# --- 2. Initialize Chat History ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# --- 3. Chat Display ---
for msg in st.session_state.chat_history[1:]:  # Skip the system prompt
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# --- 4. User Input ---
if prompt := st.chat_input("Type your message and press Enter"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # --- 5. Call Groq API ---
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": MODEL,
                "messages": st.session_state.chat_history,
                "temperature": 0.7,
            }
            try:
                response = requests.post(GROQ_API_URL, headers=headers, json=payload)
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                reply = f"❌ Error: {e}"

            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})





import streamlit as st
import os
from groq import Groq

# 1. Try to read from Streamlit secrets (Cloud)
key = st.secrets.get("GROQ_API_KEY", None)

# 2. Fallback: Try to get from env var (for local/dev or advanced users)
if key is None:
    key = os.environ.get("GROQ_API_KEY", None)

# 3. If still not found, show error
if not key:
    st.error("❌ GROQ_API_KEY not found. Please set it in .streamlit/secrets.toml or as an environment variable.")
    st.stop()

# 4. Always set as env var as well (for 3rd-party/Python compatibility)
os.environ["GROQ_API_KEY"] = key

# 5. Pass to client explicitly (always works on all platforms)
client = Groq(api_key=key)


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

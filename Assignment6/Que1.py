import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
LMSTUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.sidebar.title("LLM Selector")
model_choice = st.sidebar.radio(
    "Choose Model",
    ("Groq (Cloud)", "LM Studio (Local)")
)

st.title("💬 Groq vs LM Studio Chat App")

user_question = st.text_input("Ask your question:")

if st.button("Send") and user_question.strip():

    if model_choice == "Groq (Cloud)":
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": user_question}
            ]
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload)
        result = response.json()

        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
        else:
            answer = f"Error: {result}"

    else:  # LM Studio
        headers = {
            "Authorization": "Bearer dummy-key",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "local-model",
            "messages": [
                {"role": "user", "content": user_question}
            ]
        }

        response = requests.post(LMSTUDIO_URL, headers=headers, json=payload)
        result = response.json()

        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
        else:
            answer = "LM Studio server not running"

    # Save chat history
    st.session_state.chat_history.append(
        {"question": user_question, "answer": answer}
    )

#chat history
st.subheader("📜 Chat History")

for chat in st.session_state.chat_history:
    st.markdown(f"**User:** {chat['question']}")
    st.markdown(f"**Model:** {chat['answer']}")
    st.markdown("---")

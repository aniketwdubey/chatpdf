import streamlit as st
import requests
from dataclasses import dataclass

@dataclass
class Message:
    actor: str
    payload: str

API_URL = "http://localhost:8000"  # Adjust this to your FastAPI server address

USER = "user"
ASSISTANT = "ai"
MESSAGES = "messages"

def initialize_session_state():
    if MESSAGES not in st.session_state:
        st.session_state[MESSAGES] = []

initialize_session_state()

st.title("AI Chat Application")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Upload PDF
    files = {"file": ("uploaded.pdf", uploaded_file.getvalue(), "application/pdf")}
    try:
        response = requests.post(f"{API_URL}/upload_pdf/", files=files)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        st.success("PDF uploaded and processed successfully", icon="✅")

        # Ask questions
        st.subheader("Ask a question about the uploaded PDF:")
        
        # Display chat messages
        for msg in st.session_state[MESSAGES]:
            st.chat_message(msg.actor).write(msg.payload)

        # Correct usage of chat_input
        user_question = st.chat_input("Your question")  # Removed placeholder for compatibility

        if user_question:
            st.session_state[MESSAGES].append(Message(actor=USER, payload=user_question))
            st.chat_message(USER).write(user_question)

            with st.spinner("Processing your question..."):
                response = requests.post(f"{API_URL}/ask/", json={"question": user_question})
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=answer))
                    st.chat_message(ASSISTANT).write(answer)
                else:
                    st.error("Error getting answer from the server", icon="❌")
    except requests.RequestException as e:
        st.error(f"Error uploading PDF: {str(e)}", icon="❌")
else:
    st.write("Please upload a PDF file to start chatting.")
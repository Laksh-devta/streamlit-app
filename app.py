import streamlit as st
import requests
import whisper
from audio_recorder_streamlit import audio_recorder

# Load the Whisper model
model = whisper.load_model("small.en")

# Flask API endpoint
API_URL = "http://localhost:5000/query"  # Change this if your Flask server is hosted elsewhere

# Function to transcribe audio
def transcribe_with_whisper(audio_bytes):
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    result = model.transcribe("temp_audio.wav")
    return result["text"]

# Function to query the Flask API
def query_flask_api(query):
    try:
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            return response.json()
        else:
            return [{"text": f"Error: {response.status_code} - {response.text}"}]
    except Exception as e:
        return [{"text": f"Exception: {str(e)}"}]

def main():
    st.title("SHL Assessment Assistant")
    st.markdown("*Ask questions about the SHL assessment documents.*")

    if "history" not in st.session_state:
        st.session_state.history = []

    # Chat layout
    col1, col2 = st.columns([1, 7])

    # Audio recorder
    with col1:
        audio_bytes = audio_recorder(key="audio_recorder_no_text")

    # Text input
    with col2:
        text_input = st.chat_input("Type your question here...")

    user_input = None

    if audio_bytes:
        user_input = transcribe_with_whisper(audio_bytes)
        audio_bytes = None

    if text_input:
        user_input = text_input

    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        results = query_flask_api(user_input)
        answer = "\n\n".join([r["text"] for r in results])
        st.session_state.history.append({"role": "bot", "content": answer})

    # Display chat history
    for msg in reversed(st.session_state.history):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if __name__ == "__main__":
    main()

import streamlit as st
import os
from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

# Float feature initialization
float_init()

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! How may I assist you today?"}
        ]

initialize_session_state()

# Add a logo to the top left
st.image("./logo.png", width=250)  # Adjust the path and width as needed

st.title("Welcome to Kathabarta 🖋")


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Create footer container for the microphone and text input
footer_container = st.container()
with footer_container:
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the width ratio as needed
    with col2:
        st.markdown("""""",unsafe_allow_html=True)
        audio_bytes = audio_recorder(key="mic-container")

    st.markdown("""""",unsafe_allow_html=True)
    manual_input = st.text_input("Type your question here:", key="manual_input", help="You can type your question here")

# Handle audio input
if audio_bytes:
    with st.spinner("Transcribing..."):
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        transcript = speech_to_text(webm_file_path)
        if transcript:
            st.session_state.messages.append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

# Handle manual text input
if manual_input:
    st.session_state.messages.append({"role": "user", "content": manual_input})
    with st.chat_message("user"):
        st.write(manual_input)

# Generate assistant response if last message is from the user
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking🤔..."):
            final_response = get_answer(st.session_state.messages)
        with st.spinner("Generating audio response..."):    
            audio_file = text_to_speech(final_response)
            autoplay_audio(audio_file)
        st.write(final_response)
        st.session_state.messages.append({"role": "assistant", "content": final_response})
        os.remove(audio_file)

# Float the footer container and provide CSS to target it with
footer_container.float("bottom: 2rem;")

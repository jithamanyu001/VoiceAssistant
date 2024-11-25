import streamlit as st
from st_audiorec import st_audiorec
import os
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS

# Title and Description
st.title("AI Language Learning Assistant")
st.markdown("Record your voice, and get a translation with explanations!")

# Sidebar for language selection
target_language = st.sidebar.selectbox(
    "Select the target language", options=list(LANGUAGES.values()), index=21  # Default to French
)

# Map language name to language code
language_code = {value: key for key, value in LANGUAGES.items()}.get(target_language)

# Audio Recording
st.write("Record your audio below:")
audio_data = st_audiorec()

# Process Recorded Audio
if audio_data is not None:
    st.audio(audio_data, format="audio/wav")
    
    # Save the audio temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_data)
    
    # Convert audio to text
    recognizer = sr.Recognizer()
    with sr.AudioFile("temp_audio.wav") as source:
        try:
            st.info("Processing the audio for transcription...")
            audio_content = recognizer.record(source)
            input_text = recognizer.recognize_google(audio_content)
            st.success(f"Transcription: {input_text}")
            
            # Translate the text
            translator = Translator()
            translated_text, pronunciation = translator.translate(input_text, dest=language_code).text, translator.translate(input_text, dest=language_code).pronunciation
            st.write(f"**Translation in {target_language}:** {translated_text}")
            if pronunciation:
                st.write(f"**Pronunciation:** {pronunciation}")
            
            # Provide explanation
            explanation = f"The original text '{input_text}' was translated to '{translated_text}'. It follows the grammatical rules of {target_language}."
            st.write("**Explanation:**")
            st.write(explanation)
            
            # Convert translation to speech
            tts = gTTS(translated_text, lang=language_code)
            tts.save("output.mp3")
            audio_file = open("output.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            audio_file.close()
            os.remove("output.mp3")
        
        except sr.UnknownValueError:
            st.error("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Error with the speech recognition service: {e}")

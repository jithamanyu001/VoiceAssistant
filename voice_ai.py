import streamlit as st
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

# Set up Streamlit
st.title("AI Language Learning Assistant")
st.markdown("Speak in English, and get a translation with explanations!")

# Sidebar for language selection
target_language = st.sidebar.selectbox(
    "Select the target language", options=list(LANGUAGES.values()), index=21  # Default to French
)

# Map language name to language code
language_code = {value: key for key, value in LANGUAGES.items()}.get(target_language)

# Function to capture voice input
def capture_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak into the microphone.")
        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("Audio captured successfully!")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Error with the speech recognition service.")
            return None

# Function to translate text
def translate_text(input_text, dest_lang):
    translator = Translator()
    translation = translator.translate(input_text, dest=dest_lang)
    return translation.text, translation.pronunciation

# Function to provide translation explanation
def translation_explanation(original_text, translated_text):
    return f"The original text '{original_text}' was translated to '{translated_text}'. It follows basic grammatical rules of the target language."

# Capture voice input
if st.button("Start Recording"):
    input_text = capture_voice()
    if input_text:
        st.write(f"**You said:** {input_text}")
        
        # Translate the text
        translated_text, pronunciation = translate_text(input_text, language_code)
        st.write(f"**Translation in {target_language}:** {translated_text}")
        if pronunciation:
            st.write(f"**Pronunciation:** {pronunciation}")
        
        # Provide explanation
        explanation = translation_explanation(input_text, translated_text)
        st.write("**Explanation:**")
        st.write(explanation)
        
        # Play the translated text
        tts = gTTS(translated_text, lang=language_code)
        tts.save("output.mp3")
        audio_file = open("output.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")
        audio_file.close()
        os.remove("output.mp3")

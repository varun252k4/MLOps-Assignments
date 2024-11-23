import streamlit as st
from transformers import pipeline
from textblob import TextBlob
import speech_recognition as sr
from pydub import AudioSegment
import os
import tempfile

# Load Emotion Detection Model
@st.cache_resource
def load_emotion_model():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

emotion_model = load_emotion_model()
recognizer = sr.Recognizer()

# Sentiment Analysis Function
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Emotion Detection Function
def detect_emotions(text):
    if text:
        results = emotion_model(text)
        emotions = sorted(results, key=lambda x: x['score'], reverse=True)  # Sort by score
        return emotions[0]['label']  # Return the most likely emotion
    return "No emotion detected"

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

# Transcribe Audio Function
def transcribe_audio(file_path):
    try:
        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Error with the speech recognition service: {e}"

# Streamlit App
def main():
    st.title("Sentiment and Emotion Analysis")
    st.write("Choose between uploading an MP3 file or entering text for analysis.")

    # MP3 File Upload Section
    st.subheader("Upload Audio File")
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    if audio_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_file.name.split('.')[-1]}") as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name

        if audio_file.name.endswith(".mp3"):
            wav_path = temp_audio_path.replace(".mp3", ".wav")
            convert_mp3_to_wav(temp_audio_path, wav_path)
            temp_audio_path = wav_path

        st.audio(temp_audio_path, format="audio/wav")
        if st.button("Analyze Uploaded MP3"):
            st.write("Transcribing the uploaded audio...")
            transcription = transcribe_audio(temp_audio_path)
            st.write(f"Transcription: {transcription}")

            
            if transcription:
                # Sentiment Analysis
                sentiment = analyze_sentiment(transcription)
                st.success(f"Sentiment: {sentiment}")
                
                # Emotion Detection
                emotion = detect_emotions(transcription)
                st.success(f"Detected Emotion: {emotion}")
            
            os.remove(temp_audio_path)

    # Text Input Section
    st.subheader("Enter Text for Analysis")
    text_input = st.text_area("Enter text here", "")
    if st.button("Analyze Entered Text"):
        if text_input.strip():
            # Sentiment Analysis
            sentiment = analyze_sentiment(text_input)
            st.success(f"Sentiment: {sentiment}")
            
            # Emotion Detection
            emotion = detect_emotions(text_input)
            st.success(f"Detected Emotion: {emotion}")
        else:
            st.warning("Please enter some text for analysis.")

if __name__ == "__main__":
    main()

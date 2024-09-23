import librosa
import numpy as np
import soundfile as sf
import speech_recognition as sr
from transformers import pipeline
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
import azure.cognitiveservices.speech as speechsdk
import ffmpeg

def segment_audio(input_audio_path, segment_length_ms=10000):
    audio = AudioSegment.from_file(input_audio_path)
    segments = []
    
    for i in range(0, len(audio), segment_length_ms):
        segment = audio[i:i+segment_length_ms]
        segment_path = f"segment_{i // segment_length_ms}.wav"
        segment.export(segment_path, format="wav")
        segments.append(segment_path)
    
    return segments


def fetch_emotions(audio_path):
    """
    Fetch emotions from the speaker's voice using a pre-trained deep learning model.
    
    Args:
        audio_path (str): Path to the input audio file.
    
    Returns:
        str: Detected emotion (e.g., 'happy', 'sad', 'angry').
    """
    # Load the audio file
    audio_data, sample_rate = librosa.load(audio_path, sr=None)

    # Use Hugging Face pipeline for emotion detection
    # Using 'wav2vec2' model for extracting features
    emotion_classifier = pipeline("sentiment-analysis", model="j-hartmann/emotion-english-distilroberta-base")

    # Convert audio to features (dummy features for demo)
    # You might need to adapt this with actual features for a real model
    features = np.mean(librosa.feature.mfcc(y=audio_data, sr=sample_rate).T, axis=0)

    # Predict emotion from the features
    emotion = emotion_classifier(str(features))[0]['label']
    print(f"Detected emotion: {emotion}")
    return emotion



def analyze_emotions_for_segments(segments):
    emotions = {}
    
    for segment in segments:
        emotion = fetch_emotions(segment)
        emotions[segment] = emotion
    
    return emotions



def translate_voice(audio_path, target_language):
    """
    Translate the voice in the input audio file to the target language.
    
    Args:
        audio_path (str): Path to the input audio file.
        target_language (str): Target language code (e.g., 'es' for Spanish, 'fr' for French).
    
    Returns:
        str: Translated text.
    """
    # Recognize speech using SpeechRecognition
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    original_text = recognizer.recognize_google(audio)
    print(f"Original text: {original_text}")

    # Translate text to target language using Googletrans
    translator = Translator()
    translated_text = translator.translate(original_text, dest=target_language).text
    print(f"Translated text: {translated_text}")
    return translated_text


def apply_emotions_to_translated_voice_azure(translated_text, emotion, output_audio_path, azure_key, azure_region, speech_synthesis_voice_name):
    """
    Generate a translated voice with detected emotions using Azure Cognitive Services TTS.
    
    Args:
        translated_text (str): The translated text to synthesize.
        emotion (str): The detected emotion to apply (e.g., 'happy', 'sad', 'angry').
        output_audio_path (str): Path to save the emotion-applied translated voice.
        azure_key (str): Azure Speech service subscription key.
        azure_region (str): Azure region of the Speech service.
    """
    # Initialize Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=azure_key, region=azure_region)
    
    # Choose voice with support for emotions
    speech_config.speech_synthesis_voice_name = speech_synthesis_voice_name

    # Construct SSML with emotion
    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
        <voice name='en-US-JennyNeural'>
            <mstts:express-as style='{emotion}'>
                {translated_text}
            </mstts:express-as>
        </voice>
    </speak>
    """

    # Initialize audio configuration
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_audio_path)

    # Initialize speech synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Synthesize speech
    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Emotion-applied speech saved at {output_audio_path}")
    else:
        print(f"Speech synthesis failed: {result.reason}")

    
def combine_audio_segments(segments, output_path):
    combined = AudioSegment.empty()
    
    for segment in segments:
        audio = AudioSegment.from_file(segment)
        combined += audio
    
    combined.export(output_path, format='wav')
    print(f"Combined audio saved to: {output_path}")



if __name__ == "__main__":
    # Usage
    input_audio_path = "input_audio.wav"
    target_language = "en"
    output_audio_path = "translated_emotion_applied.wav"
    azure_key = "YOUR_AZURE_KEY"
    azure_region = "centralus"
    speech_synthesis_voice_name = "en-US-JennyNeural"  # Voice with emotion support

    # Step 1: Fetch emotions from speaker's voice
    segments = segment_audio(input_audio_path, segment_length_ms=10000)
    emotions = analyze_emotions_for_segments(segments)

    # Apply emotions to TTS and save results
    for segment, emotion in emotions.items():
        # Step 2: Translate voice
        translated_text = translate_voice(segment, target_language)
        # Step 3: Apply emotions to translated voice
        apply_emotions_to_translated_voice_azure(translated_text, emotion, f"emotion_applied_{segment}", azure_key, azure_region, speech_synthesis_voice_name)

    # Combine emotion-applied segments into a single file
    emotion_applied_segments = [f"emotion_applied_{seg}" for seg in segments]
    output_combined_audio_path = 'final_combined_audio.wav'
    combine_audio_segments(emotion_applied_segments, output_combined_audio_path)

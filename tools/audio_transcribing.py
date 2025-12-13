from langchain.tools import tool
import speech_recognition as sr
from pydub import AudioSegment
import os

@tool
def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an MP3 or WAV audio file into text using Google's Web Speech API.

    Args:
        file_path (str): Path to the input audio file (.mp3 or .wav).

    Returns:
        str: The transcribed text from the audio.

    Notes:
        - MP3 files are automatically converted to WAV.
        - Requires `pydub` and `speech_recognition` packages.
        - Uses Google's free recognize_google() API (requires internet).
    """
    try:
        # Define full path
        file_path = os.path.join("AgentFiles", file_path)
        final_path = file_path

        # Check if file needs conversion (anything that is NOT a .wav file)
        # This covers .mp3, .opus, .ogg, .flac, etc.
        if not file_path.lower().endswith(".wav"):
            # Load the file using pydub's generic from_file (handles opus automatically)
            # Note: This requires ffmpeg to be installed on your system.
            sound = AudioSegment.from_file(file_path)
            
            # Create a temporary .wav filename
            base_name = os.path.splitext(file_path)[0]
            final_path = f"{base_name}.wav"
            
            # Export to wav
            sound.export(final_path, format="wav")

        # Speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(final_path) as source:
            # Record the audio data
            audio_data = recognizer.record(source)
            # Send to Google API
            text = recognizer.recognize_google(audio_data)

        # Cleanup: remove temp file only if we created a new one
        if final_path != file_path and os.path.exists(final_path):
            os.remove(final_path)

        return text
    
    except Exception as e:
        return f"Error occurred: {e}"
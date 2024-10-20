from dotenv import load_dotenv
import json
from groq import Groq, GroqError
import os
import yt_dlp

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('GROQ_API_KEY_2')

def download_youtube_video(url, output_path="test1.mp4"):
    ydl_opts = {
        'outtmpl': output_path,  # Save with video title as the filename
        'format': 'best',  # Download the best quality video available
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            print(f"Video downloaded successfully!")
    except Exception as e:
        print(f"Error downloading video: {e}")

# Function to transcribe YouTube audio
def transcribe_youtube_audio(youtube_link, language):
    languagedict = {
        "chinese": "zh",
        "english": "en",
    }

    if api_key is None:
        assert("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)

    # Download the YouTube video audio
    download_youtube_video(youtube_link, output_path="test1.mp4")

    # Define the file path to the downloaded audio
    filename = os.path.dirname(__file__) + "/test1.mp4"

    # Open the audio file and send it to the transcription API
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            prompt="You're a video to text expert, for a language learning app. Transcribe the audio/video content, accurately capturing the spoken words and phrases.\n\n",
            response_format="verbose_json",
            language= languagedict[language]
        )
        
    # Extract start, end, and text in a JSON format
    segments_json = []
    for segment in transcription.segments:
        segments_json.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text']
        })
    # should probably delete the video here
    video_file = "test1.mp4"
    if os.path.exists(video_file):
        os.remove(video_file)
        print(f"{video_file} has been deleted.")
    else:
        print(f"{video_file} does not exist.")
    # Print or return the JSON format
    return segments_json

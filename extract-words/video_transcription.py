from dotenv import load_dotenv
import json
from groq import Groq
import os
import yt_dlp

# Load environment variables from .env file
load_dotenv()

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
def transcribe_youtube_audio(youtube_link):
    # Set the GROQ_API_KEY environment variable
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    os.environ['GROQ_API_KEY'] = GROQ_API_KEY

    # Create a Groq client with the API key
    client = Groq()

    # Download the YouTube video audio
    download_youtube_video(youtube_link, output_path="test1.mp4")

    # Define the file path to the downloaded audio
    filename = os.path.dirname(__file__) + "/test1.mp4"

    # Open the audio file and send it to the transcription API
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3-turbo",
            prompt="You're a video to text expert, for a language learning app. Transcribe the audio/video content, accurately capturing the spoken words and phrases.\n\n",
            response_format="verbose_json",
        )
        
    # Extract start, end, and text in a JSON format
    segments_json = []
    for segment in transcription.segments:
        segments_json.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text']
        })

    # Convert to JSON string if needed
    segments_json_str = json.dumps(segments_json, indent=4)

    # Print or return the JSON format
    print(segments_json_str)
    
    # should probably delete the video here
    video_file = "test1.mp4"
    if os.path.exists(video_file):
        os.remove(video_file)
        print(f"{video_file} has been deleted.")
    else:
        print(f"{video_file} does not exist.")

    
url = 'https://www.youtube.com/watch?v=bSEXPzkO3J4'  # Replace with the desired video URL
transcribe_youtube_audio(url)
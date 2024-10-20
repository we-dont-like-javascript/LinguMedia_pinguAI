from cartesia import Cartesia
import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

api_key = os.getenv('CARTESIA_API_KEY')

# transcript = "           火锅"
# language = "zh"
voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"  # Barbershop Man
model_id = "sonic-multilingual"
voice = {
    "mode": "id",
    "id": voice_id,
    "__experimental_controls": {
      "speed": -1,
      "emotion": ["curiosity:high"]
    }
}
output_format = {
    "container": "wav",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}
url = "https://api.cartesia.ai/tts/bytes"
headers = {
    "Cartesia-Version": "2024-06-10",
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}


def cartesiaTextToSpeech(transcript, language):
  # Data to be sent in the request
  data = {
      "model_id": model_id,
      "transcript": transcript,
      "voice": voice,
      "output_format": output_format,
      "language": language
  }
  # Make the POST request
  response = requests.post(url, headers=headers, data=json.dumps(data))

  # Check the response
  if response.status_code == 200:
      print("Request successful!", transcript)
      try:
        # Handle the response bytes (e.g., saving audio data)
        # with open("./audios/"+str(transcript)+".wav", "wb") as f:
        with open("../audios/test.wav", "wb") as f:
            f.write(response.content)
      except:
          print(f"Failed to save wav file for \"{str(transcript)}\"")
  else:
      print(f"Request failed with status code {response.status_code}")
      print(response.text)


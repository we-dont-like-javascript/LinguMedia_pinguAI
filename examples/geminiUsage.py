import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if api_key == None:
  assert("Can't find API key, Check .env file")

genai.configure(api_key=api_key)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}


def getDescription(word):

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="get the translation and description of given mandarin word into english, provide pronunciation and combine both language for demonstration purpose as you are an language teacher",
    # provide an example output JSON format, and output format to regulate the output
  )

  chat_session = model.start_chat(
    history=[
      {
        "role": "user",
        "parts": [
          word,
        ],
      },
    ]
  )

  response = chat_session.send_message("INSERT_INPUT_HERE")
  
  response_json = json.loads(response.text)
  print(response_json)
  print("------------------------")
  print(response_json["translation"])
  print("------------------------")

  return response.text

print(getDescription("火锅"))
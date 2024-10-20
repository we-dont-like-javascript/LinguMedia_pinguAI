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

def languageSelector(language):
  if language == "zh":
    return "mandarin"
  # more languages
  
  return language
  

def getDescriptionUseGemini(word, language):
  language = languageSelector(language)
  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=f"you are a language instructor. Provide the translation and description of given {language} word into english in json format with fields [word], [pronunciation], [translation], [description], combine both language in description for demonstration purpose",
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
  
  try:
    response_json = json.loads(response.text)
    # validate json format
    errorFlag = False
    if "word" not in response_json:
      return None
    elif "pronunciation" not in response_json:
      return None
    elif "translation" not in response_json:
      return None
    elif "description" not in response_json:
      return None
      
    return response_json
  except:
    return None

def generateQuizUseGemini(word, language):
  language = languageSelector(language)
  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=f"you are a language instructor. Provide 1 Synonyms and 1 Antonyms of given english term and 1 random word with description of them in json format with fields [synonyms], [synonymsDescription], [antonyms], [antonymsDescription], [random], [randomDescription]",
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
  
  try:
    response_json = json.loads(response.text)
    # validate json format
    errorFlag = False
    #[synonyms], [synonymsDescription], [antonyms], [antonymsDescription], [random], [randomDescription]
    if "synonyms" not in response_json or "synonymsDescription" not in response_json:
      return None
    elif "antonyms" not in response_json or "antonymsDescription" not in response_json:
      return None
    elif "random" not in response_json or "randomDescription" not in response_json:
      return None
      
    return response_json
  except:
    return None
# print(getDescriptionUseGemini("火锅", "zh"))
# print(generateQuizUseGemini("hot pot", "zh"))
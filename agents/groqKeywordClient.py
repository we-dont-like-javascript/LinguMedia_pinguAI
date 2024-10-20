import os
from groq import Groq, GroqError
from dotenv import load_dotenv
import json
from .groqVideoListenerClient import transcribe_youtube_audio

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('GROQ_API_KEY_2')

def get_Keywords(query, languageFrom, languageTo):
    if api_key is None:
        assert("GROQ_API_KEY is not set")

    client = Groq(api_key=api_key)
    keywords = []
    try:
        chatCompletion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system", 
                    "content": "you are a linguistic professor, you'll be given a stream of " + languageFrom + " text to explain to in " + languageTo + ". Help me extract the 1-4 keywords/keyphrases (only verbs, idioms, slangs, and nouns, no names) including the original text, meaning, and type. Output as JSON following the format of the example below.\n\n{\n   \"keywords\" : [\n      {\n         \"text\" : \"哥们儿\",\n         \"meaning\" : \"mates, pals, buddies\",\n         \"type\" : \"noun\"\n      }\n  ]\n}"
                },
                {
                    "role": "user", 
                    "content": str(query)
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
        )
        json_data = json.loads(chatCompletion.choices[0].message.content)
        types = ["verb", "slang", "idiom", "noun"]
        # ensure keywords have fields text, translation, and type
        for keyword in json_data["keywords"]:
            if  ("text" not in keyword or "meaning" not in keyword or "type" not in keyword) or len(json_data["keywords"]) >= 4 or keyword["type"] not in types or (not keyword["text"] or not keyword["text"].strip) or keyword["meaning"] == "" or keyword is None:
                continue
            keywords.append(keyword)
        return keywords
    except GroqError as e:
        return None

url = 'https://www.youtube.com/watch?v=C_y7zQUZ7pM'  # Replace with the desired video URL
languageFrom = "chinese"
languageTo = "english"
transcription = transcribe_youtube_audio(url, languageFrom)
for segment in transcription:
    query = segment['text']
    time_start = segment['start']
    time_end = segment['end']
    keywords = get_Keywords(query, languageFrom, languageTo)
    json_struct = {
        "time_start": time_start,
        "time_end": time_end,
        "keywords": keywords
    }
    if json_struct["keywords"]:
        print(json.dumps(json_struct, indent=4))
    else:
        continue

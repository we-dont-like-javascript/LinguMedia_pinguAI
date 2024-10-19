import os
from groq import Groq, GroqError
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv('GROQ_API_KEY_2')
if api_key is None:
    assert("GROQ_API_KEY is not set")

client = Groq(api_key=api_key)

class KeywordScraper:
    def __init__(self, timestamps, query, languageFrom, languageTo):
        self.query = query
        self.keywords = []
        self.languageFrom = languageFrom
        self.languageTo = languageTo
        self.timestamps = timestamps

    def get_Keywords(self):
        try:
            chatCompletion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system", 
                        "content": "you'll be given a stream of " + self.languageFrom + " text to translate and explain to in " + self.languageTo + ". Help me extract the keywords (only verbs, idioms, slangs, and non proper nouns) including the original text, meaning and type. Output as JSON following the format of the example below.\n\n{\n   \"keywords\" : [\n      {\n         \"text\" : \"哥们儿\",\n         \"translation\" : \"mates, pals, buddies\",\n         \"type\" : \"noun\"\n      }\n  ]\n}"
                    },
                    {
                        "role": "user", 
                        "content": str(self.query)
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
            self.keywords = json_data["keywords"]
        except GroqError as e:
            print(e)
            return None
        
        return self.keywords
    

# Create a new instance of the KeywordScraper class
exampletext = "昨天，我和几个哥们儿去了一家新开的火锅店，那儿的生意可真是红红火火。我们一边吃着火锅，一边聊着最近的生活和工作。小李最近特别忙得不可开交，他说他加班到很晚，简直是废寝忘食，不过好事多磨，项目总算有了眉目。小王则一直说自己最近有点杯弓蛇影，老觉得哪里不对劲儿。我们都哈哈大笑，劝他别想太多。那天的聚会真是宾主尽欢，大家都觉得放松了不少。虽然生活总有起起伏伏，但偶尔放松一下，也算是劳逸结合吧!"
#split the text into blocks of 10 characters
blocks = [exampletext[i:i+10] for i in range(0, len(exampletext), 10)]
for block in blocks:
    scraper = KeywordScraper(block, "Chinese", "English")
    print(scraper.get_Keywords())
from uagents import Agent, Context, Model
from groqKeywordClient import get_Keywords
from jsonParser import jsonParser
import json

keywordGenPort = 8085

keywordGeneratorAgent = Agent(
    name="keywordGeneratorAgent",
    port=keywordGenPort,
    seed="callhack-11.0-wdljs-keywordgenerator",
    endpoint=[f"http://127.0.0.1:{str(keywordGenPort)}/submit"]
)

class Message(Model):
    jsonStr: str

class Response(Model):
    jsonStr: str
    errorStr: str

recepientAddress = (
    f"keywordGeneratorAgent://endpoint"
)

@keywordGeneratorAgent.on_event("startup")
async def  starUp_printing(ctx: Context):
    ctx.logger.info(f"KeywordAgent running, address:{keywordGeneratorAgent.address}")
@keywordGeneratorAgent.on_message(model=Message)
async def keywordGenerator(ctx: Context, sender: str, request: Message):
    
    data = jsonParser(request.jsonStr)

    # input validation
    errorInput = False
    if data == None:
        print("data is None")
        errorInput = True
    elif "start" not in data or "end" not in data or "text" not in data or "languageFrom" not in data or "languageTo" not in data:
        print ("missing fields in data: start, end, text, languageFrom, or languageTo")
        errorInput = True

    if errorInput:
        print("Error Input in keywordGenerator")
        return
    
    start = data["start"]
    end = data["end"]
    query = data["text"]
    languageFrom = data["languageFrom"]
    languageTo = data["languageTo"]
    
    print("Getting keywords")
    keywords = get_Keywords(query, languageFrom, languageTo)
    print("Keywords complete")
    language_dict = {
        "chinese": "zh",
        "english": "en",
    }
    #add language to keywords
    jsonStruct = {
        "start": start,
        "end": end,
        "keywords": keywords,
        "language": language_dict[languageFrom],
    }
    if jsonStruct["keywords"]:
        print(jsonStruct)
    #await ctx.send(recepientAddress, Message(jsonStr=keywords))

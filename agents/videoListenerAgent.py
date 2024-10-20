import json
from uagents import Agent, Context, Model
from groqVideoListenerClient import transcribe_youtube_audio
from keywordGeneratorAgent import keywordGeneratorAgent
from jsonParser import jsonParser

videoListenerPort = 8084

videoListenerAgent = Agent(
    name="videoListenerAgent",
    port=videoListenerPort,
    seed="callhack-11.0-wdljs-videolistener",
    endpoint=[f"http://127.0.0.1:{str(videoListenerPort)}/submit"]
)

recipientAddress = (
    f"videoListenerAgent://{keywordGeneratorAgent.address}"
)

class Message(Model):
    jsonStr: str

class Response(Model):
    jsonStr: str
    errorStr: str

@videoListenerAgent.on_event("startup")
async def  starUp_printing(ctx: Context):
    ctx.logger.info(f"VideoListenerAgent running, address:{videoListenerAgent.address}")
@videoListenerAgent.on_message(model=Message)
async def videoListener(ctx: Context, sender: str, request: Message):
    
    data = jsonParser(request.jsonStr)
    #input validation
    errorInput = False

    if data == None:
        print("data is None")
        errorInput = True
    elif "url" not in data or "languageTo" not in data or "languageFrom" not in data:
        print("missing fields in data: languageTo, languageFrom, or url")
        errorInput = True
    elif not isinstance(data["url"], str) or not isinstance(data["languageTo"], str) or not isinstance(data["languageFrom"], str):
        print("data fields are not strings")
        errorInput = True

    if errorInput:
        print("Error Input in videoListener")
        return
    
    url = data["url"]
    languageFrom = data["languageFrom"]
    print("Transcribing YouTube audio")
    transcriptionList = transcribe_youtube_audio(url, languageFrom)
    print("Transcription complete")
    for transcription in transcriptionList:
      transcription["languageTo"] = str(data["languageTo"])
      transcription["languageFrom"] = str(data["languageFrom"])
      transcriptionJsonStr = json.dumps(transcription)
      print("Sending transcription to keywordGeneratorAgent")
      print(transcriptionJsonStr)
      await ctx.send(recipientAddress , Message(jsonStr=transcriptionJsonStr))

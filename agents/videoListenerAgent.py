from uagents import Agent, Context, Model
import groqVideoListenerClient
import keywordGeneratorAgent
import jsonParser
import json

videoListenerPort = 8084

agent = Agent(
    name="videoListenerAgent",
    port=videoListenerPort,
    seed="callhack-11.0-wdljs-videolistener",
    endpoint=[f"http://127.0.0.1:{str(videoListenerPort)}/submit"]
)

recipientAddress = (
    f"videoListenerAgent://{keywordGeneratorAgent.address}"
)

class videoListenerRequest(Model):
    url: str
    language: str

class videoListenerResponse(Model):
    json_file: str
    errorStr: str

@agent.on_event("startup")
async def  starUp_printing(ctx: Context):
    ctx.logger.info(f"VideoListenerAgent running, address:{agent.address}")
@agent.on_message(model=videoListenerRequest)
async def videoListener(ctx: Context, sender: str, request: videoListenerRequest):
    
    #input validation
    errorInput = False
    if request.url == None or request.language == None:
        errorInput = True
    elif not isinstance(request.url, str) or not isinstance(request.language, str):
        errorInput = True

    if errorInput:
        await ctx.send(sender, videoListenerResponse(json_file="", errorStr="Error Input"))
        return
    
    transcription = groqVideoListenerClient.transcribe_youtube_audio(request.url, request.language)
    await ctx.send(recipientAddress , videoListenerResponse(json_file=transcription))

agent.run()

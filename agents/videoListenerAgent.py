from uagents import Agent, Context, Model
import groqVideoListenerClient
import keywordGeneratorAgent

videoListenerPort = 8084

agent = Agent(
    name="videoListenerAgent",
    port=videoListenerPort,
    seed="callhack-11.0-wdljs-videolistener",
    endpoint=[f"http://127.0.0.1:{videoListenerPort}/submit"]
)

recipientAddress = (
    f"videoListenerAgent://{keywordGeneratorAgent.address}"
)

class videoListenerRequest(Model):
    url: str
    language: str

class videoListenerResponse(Model):
    json_file: str

@agent.on_message(model=videoListenerRequest)
async def videoListener(ctx: Context, request: videoListenerRequest):
    transcription = groqVideoListenerClient.transcribe_youtube_audio(request.url, request.language)
    await ctx.send(recipientAddress , videoListenerResponse(json_file=transcription))

agent.run()

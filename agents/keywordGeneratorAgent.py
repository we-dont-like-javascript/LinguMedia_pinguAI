from uagents import Agent, Context, Model
import groqKeywordClient
keywordGenPort = 8085

agent = Agent(
    name="VideoListenerAgent",
    port=keywordGenPort,
    seed="callhack-11.0-wdljs-videolistener",
    endpoint=[f"http://127.0.0.1:{keywordGenPort}/submit"]
)

class keywordGeneratorRequest(Model):
    query: str
    languageFrom: str
    languageTo: str

class keywordGeneratorResponse(Model):
    json_file: str

@agent.on_message(model=keywordGeneratorRequest)
async def videoListener(ctx: Context, request: keywordGeneratorRequest):
    keywords = groqKeywordClient.get_Keywords(request.query, request.languageFrom, request.languageTo)
    await ctx.send(request.client_address, keywordGeneratorResponse(json_file=keywords))

agent.run()

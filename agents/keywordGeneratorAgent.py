from uagents import Agent, Context, Model
import groqKeywordClient
import jsonParser
import json

keywordGenPort = 8085

agent = Agent(
    name="VideoListenerAgent",
    port=keywordGenPort,
    seed="callhack-11.0-wdljs-videolistener",
    endpoint=[f"http://127.0.0.1:{str(keywordGenPort)}/submit"]
)

class keywordGeneratorRequest(Model):
    query: str
    languageFrom: str
    languageTo: str

class keywordGeneratorResponse(Model):
    json_file: str
    errorStr: str

@agent.on_event("startup")
async def  starUp_printing(ctx: Context):
    ctx.logger.info(f"VideoListenerAgent running, address:{agent.address}")
@agent.on_message(model=keywordGeneratorRequest)
async def videoListener(ctx: Context, sender: str, request: keywordGeneratorRequest):
    
    data = jsonParser.parseJson(request.jsonStr)

    # input validation
    errorInput = False
    if data == None:
        errorInput = True
    elif "query" not in data or "languageFrom" not in data or "languageTo" not in data:
        errorInput = True
    elif not isinstance(data["query"], str) or not isinstance(data["languageFrom"], str) or not isinstance(data["languageTo"], str):
        errorInput = True

    if errorInput:
        await ctx.send(sender, keywordGeneratorResponse(json_file="", errorStr="Error Input"))
        return
    
    keywords = groqKeywordClient.get_Keywords(request.query, request.languageFrom, request.languageTo)
    await ctx.send(request.client_address, keywordGeneratorResponse(json_file=keywords))

agent.run()

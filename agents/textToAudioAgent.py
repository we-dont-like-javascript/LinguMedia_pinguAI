import json
from cartesiaTextToSpeech import cartesiaTextToSpeech
from uagents import Agent, Context, Model

class Message(Model):
    jsonStr: str

class Response(Model):
    jsonStr: str
    errorStr: str

textToAudioPort = 8083
textToAudioAgent = Agent(
  name="textToAudio",
  port=textToAudioPort,
  seed="callhack-11.0-wdljs-textToAudio",
  endpoint=[f"http://127.0.0.1:{str(textToAudioPort)}/submit"]
)


def parseJson(jsonStr):
    try:
        # Attempt to parse the JSON string
        parsed_data = json.loads(jsonStr)
        return parsed_data
    except json.JSONDecodeError as e:
        # Handle parsing error, such as malformed JSON
        print(f"Failed to parse JSON: {e}")
        return None

@textToAudioAgent.on_event("startup")
async def starUp_printing(ctx: Context):
    ctx.logger.info(f"textToAudio agent running, address:{textToAudioAgent.address}")
  
@textToAudioAgent.on_message(model=Message)
async def textToAudio_message_handler(ctx: Context, sender: str, msg: Message):
    data = parseJson(msg.jsonStr)
    
    # input validation
    errorInput = False
    if data == None:
        errorInput = True
    elif "transcript" not in data:
        errorInput = True
    elif "translation" not in data:
        errorInput = True
    elif "language" not in data:
        errorInput = True
    elif not isinstance(data["transcript"], str):
        errorInput = True
    elif not isinstance(data["translation"], str):
        errorInput = True
    elif not isinstance(data["language"], str):
        errorInput = True
      
    if errorInput:
        ctx.logger.error(f"textToAudio received invalid input:{msg.jsonStr}")
        await ctx.send(sender, Response(jsonStr="", errorStr="Error Input"))
        return
    
    # correct input
    audioPath = cartesiaTextToSpeech(data["transcript"], data["language"], data["translation"])
    await ctx.send(sender, Response(jsonStr=audioPath, errorStr=""))
    

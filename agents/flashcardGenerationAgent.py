import json
from uagents import Agent, Context, Model
from textToAudioAgent import textToAudioAgent
from geminiAccess import getDescriptionUseGemini, generateQuizUseGemini


def parseJson(jsonStr):
    try:
        # Attempt to parse the JSON string
        parsed_data = json.loads(jsonStr)
        return parsed_data
    except json.JSONDecodeError as e:
        # Handle parsing error, such as malformed JSON
        print(f"Failed to parse JSON: {e}")
        return None
      
def isDuplicate(word):
  return False # pending implementation

def getRecipientAddress(agent):
    recipient_address = (
      f"test-agent://{agent.address}"
    )
    return recipient_address
  
class Message(Model):
    jsonStr: str

class Response(Model):
    jsonStr: str
    errorStr: str

flashCardGenPort = 8082
flashCardGenAgent = Agent(
    name="flashCardGen",
    port=flashCardGenPort,
    seed="callhack-11.0-wdljs-flashCardGen",
    endpoint=["http://127.0.0.1:{flashCardGenPort}/submit"]
)


@flashCardGenAgent.on_event("startup")
async def starUp_printing(ctx: Context):
    ctx.logger.info(f"flashCardGen agent running, address:{flashCardGenAgent.address}")


@flashCardGenAgent.on_message(model=Message)
async def flashCardGen_message_handler(ctx: Context, sender: str, msg: Message):
    data = parseJson(msg.jsonStr)
    
    # input validation
    errorInput = False
    if data == None:
        errorInput = True
    elif "time_start" not in data:
        errorInput = True
    elif "time_end" not in data:
        errorInput = True
    elif "keywords" not in data:
        errorInput = True
        
    if errorInput:
        ctx.logger.error(f"flashCardGen received invalid input:{msg.jsonStr}")
        await ctx.send(sender, Response(jsonStr="", errorStr="Error Input"))
        return

    # correct input
    try:
      time_start = data["time_start"]
      time_end = data["time_end"]
      
      count = 0
      for keyword in data["keywords"]:
        if count >= 2:
          return # limit the rate of descriptions
        if isDuplicate(keyword["text"]):
          continue 
        
        data = {
          "transcript":keyword["text"],
          "language":data["language"]
        }
        
        # get description and quiz
        description_data = getDescriptionUseGemini(data["transcript"], data["language"])
        quiz_data = generateQuizUseGemini(data["transcript"], data["language"])
        
        # generate audio
        recipient_address = getRecipientAddress(textToAudioAgent)
        data_jsonStr = json.dumps(data)
        response = await ctx.send(recipient_address, Message(jsonStr=data_jsonStr))
        if response.errorStr != "":
          # there is an error
          continue # skip this key
        audioPath = response.jsonStr
        
        # construct final data
        # save to database
        
        # response
        
    except Exception as e:
      print(e)
    await ctx.send(sender, Message(message="Hello there alice."))

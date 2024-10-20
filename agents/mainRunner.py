import json
from uagents import Agent, Bureau, Context, Model
from textToAudioAgent import textToAudioAgent


class Message(Model):
    jsonStr: str
    
starUpAgent = Agent(
  name="startUp",
  port="8180",
  seed="dasdafs",
  endpoint=["http://127.0.0.1:8180/submit"]
)
@starUpAgent.on_event("startup")
async def test_agents(ctx: Context):
  data = {
    "transcript":"茉莉花",
    "language":"zh"
  }
  print("-- send to textToAudio")
  data_jsonStr = json.dumps(data)
  recipient_address = (
    f"test-agent://{textToAudioAgent.address}"
  )
  response = await ctx.send(recipient_address, Message(jsonStr=data_jsonStr))
  
  print(f"response:{response}")

print(textToAudioAgent.address)
bureau = Bureau()
bureau.add(starUpAgent)
bureau.add(textToAudioAgent)
 
if __name__ == "__main__":
    bureau.run()
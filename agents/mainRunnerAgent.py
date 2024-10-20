import json
from uagents import Agent, Bureau, Context, Model
from videoListenerAgent import videoListenerAgent
from keywordGeneratorAgent import keywordGeneratorAgent

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
    "url":"https://www.youtube.com/watch?v=C_y7zQUZ7pM",
    "languageTo":"english",
    "languageFrom":"chinese",
  }
  data_jsonStr = json.dumps(data)
  print("-- send to videListener")
  recipient_address = (
    f"test-agent://{videoListenerAgent.address}"
  )
  response = await ctx.send(recipient_address, Message(jsonStr=data_jsonStr))
  
  print(f"response:{response}")

print(videoListenerAgent.address)
bureau = Bureau()
bureau.add(starUpAgent)
bureau.add(videoListenerAgent)
bureau.add(keywordGeneratorAgent)
 
if __name__ == "__main__":
    bureau.run()
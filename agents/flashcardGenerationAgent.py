from uagents import Agent, Context, Model
 
class Message(Model):
    jsonStr: str

flashCardGenPort = 8082
flashCardGenAgent = Agent(
  name="flashCardGen",
  port=flashCardGenPort,
  seed="callhack-11.0-wdljs-flashCardGen",
  endpoint=["http://127.0.0.1:{flashCardGenPort}/submit"]
)


@flashCardGenAgent.on_message(model=Message)
async def flashCardGen_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    
    
    await ctx.send(sender, Message(message="Hello there alice."))
    
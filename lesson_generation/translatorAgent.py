from uagents import Agent, Context, Model

class ContextPrompt(Model):
  context: str
  text: str

class Response(Model):
  text: str


agent = Agent()


AI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"


code = "\"飞机\""

prompt = ContextPrompt(
    context="Provide Translation and Explanation of below mandarin word  in english",
    text=code,
)


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, prompt)


@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")


if __name__ == "__main__":
    agent.run()
from dotenv import load_dotenv 
load_dotenv() 
from agents.user_agent import UserAgent
import chainlit as cl

agent = UserAgent()

@cl.on_message
async def main(message: cl.Message):
    response = agent.handle_input(message.content)

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()
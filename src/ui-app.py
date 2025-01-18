from dotenv import load_dotenv 
load_dotenv() 
from agents.user_agent import UserAgent
import chainlit as cl

agent = UserAgent(use_chainlit=True)

@cl.on_message
async def main(message: cl.Message):
    response = await agent.handle_input(message.content)

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="No internet connection",
            message="I have no internet connection, can you help me?",
            icon="/public/idea.svg",
            ),
        cl.Starter(
            label="Unable to print",
            message="I can't print using my printer, what could be wrong?",
            icon="/public/idea.svg",
            ),
        ]
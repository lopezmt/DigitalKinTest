from dotenv import load_dotenv 
load_dotenv() 
from agents.user_agent import UserAgent
import asyncio

async def main():
    print("Bienvenue dans le système de support technique !")
    agent = UserAgent()

    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["quit", "exit"]:
            print("Merci d'avoir utilisé notre support technique. Au revoir !")
            break
        
        # Await the async handle_input method
        response = await agent.handle_input(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    asyncio.run(main())
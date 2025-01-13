from dotenv import load_dotenv 
load_dotenv() 
from agents.user_agent import UserAgent
from agents.agent_a import AgentA

def main():
    print("Bienvenue dans le système de support technique !")
    agent_a = UserAgent()

    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["quit", "exit"]:
            print("Merci d'avoir utilisé notre support technique. Au revoir !")
            break
        response = agent_a.handle_user_input(user_input)
        print(f"Agent A : {response}")

if __name__ == "__main__":
    main()

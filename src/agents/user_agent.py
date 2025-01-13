

from agents.agent import Agent
name = "user_agent"
systemPrompt = "Tu es un assistant serviable et qui souhaite aider ces utilisateur. En cas de besoin tu peux demander aux agents mis à ta disposition."
description = "Assistant communiquant directement avec l'utilisateur"
def UserAgent():
    return Agent(
        name=name,
        system_prompt=systemPrompt, 
        description=description,
        agents=None
    )
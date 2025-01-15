

from agents.agent import Agent
from agents.technical_agent import TechnicalAgent
name = "user_agent"
systemPrompt = """You are a polite assistant.
Use agents at your disposal to provide accurate answers.
Do not answer on your own, use the agents.
If they do not provide relevant information, you can say you didn't find any relevant information.
"""
description = "Assistant communiquant directement avec l'utilisateur"
def UserAgent():
    tech_agent = TechnicalAgent()
    return Agent(
        name=name,
        system_prompt=systemPrompt, 
        description=description,
        agents=[tech_agent]
    )
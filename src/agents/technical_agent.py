from agents.agent import Agent
from tools.search_technical_data_tool import SearchTechnicalDataTool
name = "technical_agent"
description = "Technical agent that provides information about technical issues and their solutions."
systemPrompt = """You are a technical agent that have access to a knowledge base of troubleshooting scenarios.
You can use it to find information about technical issues and their solutions.
If the findings does not seem relevant to you, do not hesitate to say you didn't find any relevant information.
"""

def TechnicalAgent(use_chainlit=False):
    technical_data_tool = SearchTechnicalDataTool()
    return Agent(
        name=name,
        system_prompt=systemPrompt, 
        description=description,
        tools=[technical_data_tool],
        use_chainlit=use_chainlit
    )
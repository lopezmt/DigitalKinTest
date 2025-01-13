import json
from openai import OpenAI
client = OpenAI()

class Agent:
    def __init__(self, name, description, system_prompt, agents):
        self.system_prompt = system_prompt
        self.description = description
        self.name = name
        self.history = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.tools = []

    def handle_user_input(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(model="gpt-4-0613",
                                                  messages=self.history,
                                                  functions=None,
                                                  function_call=None)

        return response.choices[0].message.content
    
    def get_function_description(self):
        # function description to be used with openai api
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
                    },
                },
            },
        }
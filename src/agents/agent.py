import json
from openai import OpenAI
client = OpenAI()

class Agent:
    def __init__(self, system_prompt, description, agents):
        self.system_prompt = system_prompt
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

        if "function_call" in response.choices[0].message:
            function_call = response.choices[0].message.function_call
            arguments = json.loads(function_call["arguments"])

            self.history.append(
                {"role": "assistant", "content": f"Appel de la fonction: {function_call['name']} avec les arguments {arguments}."}
            )

        return response.choices[0].message.content
import json
from openai import OpenAI
client = OpenAI()

class Agent:
    def __init__(self, name, description, system_prompt, agents = [], tools = []):
        self.system_prompt = system_prompt
        self.description = description
        self.name = name
        self.history = [
            {"role": "system", "content": self.system_prompt}
        ]
        self.agents = agents
        self.tools = tools

        self.function_descriptions = []
        self.function_descriptions = [agent.get_function_description() for agent in self.agents]
        self.function_descriptions += [tool.get_function_description() for tool in self.tools]

    def handle_input(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        response = self.completion()

        #handle function call
        while (response.choices[0].message.tool_calls
            and len(response.choices[0].message.tool_calls) > 0):
            self.history.append(response.choices[0].message)
            #We consider only one tool call for now
            tool_call = response.choices[0].message.tool_calls[0]
            agentName = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            query = arguments.get('query')

            agent = self.get_agent(agentName)
            if agent:
                print(f"Calling agent {agentName} with query: {query}")
                answer = agent.handle_input(query)

            tool = self.get_tool(agentName)
            if tool:
                print(f"Calling tool {agentName} with query: {query}")
                answer = tool.execute(query)
            function_call_result_message = {
                "role": "tool",
                "content": answer,
                "tool_call_id": tool_call.id
            }
            self.history.append(function_call_result_message)
            
            response = self.completion()
        self.history.append(response.choices[0].message)

        return response.choices[0].message.content
    
    def get_agent(self, name):
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None
    
    def get_tool(self, name):
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None
    
    def completion(self):
        response = client.chat.completions.create(model="gpt-4o-mini",
                                                  messages=self.history,
                                                  tools=self.function_descriptions if len(self.function_descriptions) > 0 else None,
        )
        return response
    
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
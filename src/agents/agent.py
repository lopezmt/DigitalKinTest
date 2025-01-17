import json
from openai import AsyncOpenAI

client = AsyncOpenAI()

class Agent:
    def __init__(self, name, description, system_prompt, agents=None, tools=None, use_chainlit=False):
        self.system_prompt = system_prompt
        self.description = description
        self.name = name
        self.use_chainlit = use_chainlit
        # Dynamically import chainlit if it is used
        # This is done to avoid importing chainlit when using the command line interface
        # when imported with the command line interface, chainlit produce a lot of outputs that are not desired
        if self.use_chainlit:
            import chainlit as cl
            self.cl = cl
        self.history = [{"role": "system", "content": self.system_prompt}]
        self.agents = agents if agents else []
        self.tools = tools if tools else []

        self.function_descriptions = [
            agent.get_function_description() for agent in self.agents
        ] + [
            tool.get_function_description() for tool in self.tools
        ]

    async def handle_input(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        response = await self.completion()

        # Handle function calls
        while (
            response is not None
            and response.choices[0].message.tool_calls
            and len(response.choices[0].message.tool_calls) > 0
        ):
            response = await self.handle_tool_call(response)

        if response is not None:
            self.history.append(response.choices[0].message)
            return response.choices[0].message.content
        else:
            return "An error occurred during completion."

    async def handle_tool_call(self, tool_call):
        self.history.append(tool_call.choices[0].message)
        tool_call = tool_call.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        query = arguments.get('query')

        # Find the appropriate agent or tool
        agent = self.get_agent(function_name)
        if agent:
            if self.use_chainlit:
                async with self.cl.Step(name=f"{function_name} agent") as step:
                    answer = await agent.handle_input(query)
                    step.input = query
                    step.output = answer
            else:
                print(f"Calling agent {function_name} with query: {query}")
                answer = await agent.handle_input(query)

        tool = self.get_tool(function_name)
        if tool:
            if self.use_chainlit:
                async with self.cl.Step(name=f"{function_name} tool") as step:
                    answer = tool.execute(query)
                    step.input = query
                    step.output = answer
            else:
                print(f"Calling tool {function_name} with query: {query}")
                answer = tool.execute(query)


        function_call_result_message = {
            "role": "tool",
            "content": answer,
            "tool_call_id": tool_call.id
        }
        self.history.append(function_call_result_message)

        return await self.completion()
    
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

    async def completion(self):
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.history,
                tools=self.function_descriptions if self.function_descriptions else None,
            )
            return response
        except Exception as e:
            print(f"An error occurred during completion: {e}")
            return None

    def get_function_description(self):
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
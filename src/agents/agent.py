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
            response.choices[0].message.tool_calls
            and len(response.choices[0].message.tool_calls) > 0
        ):
            self.history.append(response.choices[0].message)
            tool_call = response.choices[0].message.tool_calls[0]
            agent_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            query = arguments.get('query')

            # Find the appropriate agent or tool
            agent = self.get_agent(agent_name)
            if agent:
                if self.use_chainlit:
                    async with self.cl.Step(name=f"{agent_name} agent") as step:
                        answer = await agent.handle_input(query)
                        step.input = query
                        step.output = answer
                else:
                    print(f"Calling agent {agent_name} with query: {query}")
                    answer = await agent.handle_input(query)

            tool = self.get_tool(agent_name)
            if tool:
                if self.use_chainlit:
                    async with self.cl.Step(name=f"{agent_name} tool") as step:
                        print(f"Calling tool {agent_name} with query: {query}")
                        answer = tool.execute(query)
                        step.input = query
                        step.output = answer
                else:
                    print(f"Calling tool {agent_name} with query: {query}")
                    answer = tool.execute(query)


            function_call_result_message = {
                "role": "tool",
                "content": answer,
                "tool_call_id": tool_call.id
            }
            self.history.append(function_call_result_message)

            response = await self.completion()

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

    async def completion(self):
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            tools=self.function_descriptions if self.function_descriptions else None,
        )
        return response

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
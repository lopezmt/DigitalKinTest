class Tool:
    def __init__(self, name, description, function):
        self.name = name
        self.description = description
        self.function = function

    def execute(self, query):
        # execute the function with the arguments
        return self.function(query)

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


from array import array
from typing import List, Dict

from openai import OpenAI

from coder import Coder
from user import User
from tool import Tool, Parameter
from pydantic import BaseModel

client = OpenAI()



coder = Tool(
    name="coder_agent",
    description="Writes, test and return code performing task given by user. ",
    parameters=[
        Parameter(type="array", name="input", description="Arguments to the code. For example if the request is about weather forecast the arguments could be the location and day ", required=True ),
        Parameter(type="array", name="output", description="The expected output of the code in array format. For example if the request is about weather forecast the output is the min and max for the given day and location", required=True),
        Parameter(type="string", name="logic", description="Describes what the code should do. For example if the request is about weather forecast the code should call the OpenWeatherMap API, fetch the e=weather forecast and format it", required=True)
    ],
    actor=Coder())



class Agent(BaseModel):
    #user_interact: User
    messages: List[Dict[str,str]] = [
        {"role": "system",
         "content":
"""You are a helpful assistant with different tools to help users. When the user ask something: 
Pick the best tool for the job and use it. Your goal is to help the user quickly and accurately."""
        }]

    tools: List[Tool] = []

    def tool_match(self):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages,
            tools=[tool.dump() for tool in self.tools],
            temperature=0,
            #tool_choice="required",  # forces tool call
        )
        if completion.choices[0].finish_reason != "tool_calls":
            return completion.choices[0].message.content

        fcts = {}
        for tool_call in completion.choices[0].message.tool_calls:
            fct_name = tool_call.function.name
            fct_argument = tool_call.function.arguments
            fcts[fct_name] = fct_argument
        return fcts




    def start(self, user: User):
        message = "What can i help you with?"
        u_message = user.ask(message)
        self.messages.extend([{
            "role": "assistant", "content": message
        }, {"role": "user", "content": u_message}])
        self.ask()
    def ask(self):
        user = User()
        while True:
            resp = self.tool_match()
            if isinstance(resp, Dict):
                print(f"It's a hit!! delegating to tool: {resp}")
                for fct, arguments in resp.items():
                    self.delegate(fct, arguments)
                break
            else:
                user_input = user.ask(resp)
                self.messages.extend([
                    {"role": "assistant", "content": resp},
                    {"role": "user", "content": user_input}
                ])
                #print(self.messages)
    def delegate(self, fct, arguments):
        for tool in self.tools:
            if tool.name == fct:
                resp = tool.actor.run(arguments)
                print(f"response from Actor[{tool.name}]:\n {resp}")


user = User()
fred = Agent(tools=[coder])
fred.start(user)






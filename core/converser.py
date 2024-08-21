from typing import Dict, List, Tuple, Any, Type
from pydantic import BaseModel, Field
from core.actor import Actor
from core.completion import Completion, OpenAICompletion


class Message(BaseModel):
    role: str # system, user, assistant
    content: str

    def out(self):
        return { "role": self.role, "content": self.content }


class UserMessage(Message):
    def __init__(self, content):
        super().__init__(role="user", content=content)

class AssistantMessage(Message):
    def __init__(self, content):
        super().__init__(role="assistant", content=content)


class SystemMessage(Message):
    def __init__(self, content):
        super().__init__(role="system", content=content)

class Converser:
    examples: Dict[str, str] = {}
    messages: List[Message] = []
    completion: Completion
    actors: List[Actor] = []

    def __init__(self, completion, instruction,
                 examples: Dict[str,str]=None,
                 actors: List[Actor]=None):
        self.completion = completion
        self.messages.append(SystemMessage(instruction))
        if examples is not None:
            self.examples = examples
        if actors is not None:
            self.actors = actors

    def response(self, str: str, response_obj:Type[BaseModel] =None,) -> str:
        self.messages.append(UserMessage(content=str))
        if response_obj is not None:
            resp = self.completion.parse(messages=[msg.out() for msg in self.messages], response_format=response_obj)
            self.messages.append(AssistantMessage(content=resp.json()))

        else:
            resp = self.completion.complete(messages=[msg.out() for msg in self.messages])
            self.messages.append(AssistantMessage(content=resp))

        return resp

    def tool(self, str: str) -> tuple[Actor, Any] | None:
        self.messages.append(UserMessage(content=str))
        fcts = self.completion.force_tool(
            messages=[msg.out() for msg in self.messages],
            tools=[actor.tool() for actor in self.actors])

        for actor in self.actors:
            for fct in fcts:
                if fct["name"] == actor.name:
                    return actor, fct["arguments"]
        return None


    def last_message(self):
        if len(self.messages) > 0:
            return self.messages[-1].content
        else:
            return None

# completion = OpenAICompletion()
# c = Converser(completion=completion, instruction = "you are a helpful assistant")
# resp = c.response("what color is the sea")
# print(c.messages)

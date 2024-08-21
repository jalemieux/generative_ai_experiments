from typing import Dict, List, Tuple, Any, Type
from pydantic import BaseModel, Field
from core.actor import Actor
from core.completion import Completion, OpenAICompletion
import json

class Message(BaseModel):
    role: str # system, user, assistant
    content: str

    def __str__(self):
        return f"{self.role}: {self.content}"

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
    examples: Dict[str, str]
    messages: List[Message]
    completion: Completion
    actors: List[Actor]
    persist: str

    def __init__(self, completion, instruction=None,
                 persist=None,
                 examples: Dict[str,str]=None,
                 actors: List[Actor]=None):
        self.completion = completion
        self.persist = persist
        self.messages = []
        if instruction is not None:
            self._add_message(SystemMessage(instruction))
        if examples is not None:
            self.examples = examples
        if actors is not None:
            self.actors = actors

    def _add_message(self, msg: Message):
        self.messages.append(msg)
        if self.persist is not None:
            self.save(self.persist)


    def response(self, str: str, response_obj:Type[BaseModel] =None,) -> str:
        self._add_message(UserMessage(content=str))
        if response_obj is not None:
            resp = self.completion.parse(messages=[msg.out() for msg in self.messages], response_format=response_obj)
            self._add_message(AssistantMessage(content=resp.json()))

        else:
            resp = self.completion.complete(messages=[msg.out() for msg in self.messages])
            self._add_message(AssistantMessage(content=resp))

        return resp

    def tool(self, str: str) -> tuple[Actor, Any] | None:
        self._add_message(UserMessage(content=str))
        fcts = self.completion.force_tool(
            messages=[msg.out() for msg in self.messages],
            tools=[actor.tool() for actor in self.actors])

        self._add_message(AssistantMessage(content=fcts))
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

    def dump(self, fp):
        with open(fp, 'w') as f:
            f.write("\n".join([ str(m) for m in self.messages]))

    def save(self, fp):
        with open(fp, 'w') as f:
            json.dump([message.dict() for message in self.messages], f, indent=4)

    @staticmethod
    def load_messages(fp) -> List[Message]:
        with open(fp, 'r') as f:
            data = json.load(f)
            return [Message(**m) for m in data]




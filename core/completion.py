from typing import List, Dict, Type
from openai import OpenAI

from typing import Optional, List, Dict

from openai._base_client import SyncAPIClient
from pydantic import BaseModel, Field
import re


class Parameter(BaseModel):
    type: str
    name: str
    description: str
    required: bool = Field(default=True)
    enum: Optional[List[str]] = None


class Tool(BaseModel):
    name: str
    description: str
    parameters: List[Parameter]

    def dump(self) -> Dict:
        out = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            }
        }
        for parameter in self.parameters:
            required = []
            chunk = {
                "type": parameter.type,
                "description": parameter.description
            }
            if parameter.type == "array":
                chunk["items"] = {"type": "string"}

            if parameter.enum is not None:
                chunk["enum"] = parameter.enum

            out["function"]["parameters"]["properties"][parameter.name] = chunk

            if parameter.required is True:
                required.append(parameter.name)

        return out


class Completion:
    def complete(self, messages: List[Dict[str, str]]) -> str:
        pass

    def parse(self, messages: List[Dict[str, str]], response_format: Type[BaseModel] = None) -> str:
        pass

    def force_tool(self, messages: List[Dict[str, str]], tools: List[Tool]) -> List:
        pass

    def _compress_messages(self, messages):
        # TODO: summarize if length exceeds treshold
        compressed_messages: List[Dict[str, str]] = []
        for msg in messages:
            compressed_content = re.sub(r'\s+', ' ', msg["content"]).strip()
            compressed_messages.append({"role": msg["role"], "content": compressed_content})
        return compressed_messages


class OpenAICompletion(Completion):
    client: SyncAPIClient
    parse_model: str
    completion_model: str
    tool_model: str
    default_model: str
    default_temperature: str

    def __init__(self,
                 completion_model=None,
                 parse_model=None,
                 tool_model=None,
                 default_model=None,
                 default_temperature=None
                 ):
        self.default_model = default_model or "gpt-4o"
        self.completion_model = completion_model or self.default_model
        self.parse_model = parse_model or self.default_model
        self.tool_model = tool_model or self.default_model
        self.default_temperature = default_temperature or 0
        client = OpenAI()

    def parse(self, messages: List[Dict[str, str]], response_format: Type[BaseModel] = None, ) -> str:
        completion = self.client.beta.chat.completions.parse(
            model=self.parse_model,
            messages=self._compress_messages(messages),
            temperature=0,
            response_format=response_format
        )
        return completion.choices[0].message.parsed

    def complete(self, messages: List[Dict[str, str]]) -> str:
        completion = self.client.chat.completions.create(
            model=self.completion_model,
            messages=self._compress_messages(messages),
            temperature=0,
        )
        return completion.choices[0].message.content

    def force_tool(self, messages: List[Dict[str, str]], tools: List[Tool]) -> List:
        completion = self.client.chat.completions.create(
            model=self.tool_model,
            messages=self._compress_messages(messages),
            tools=[tool.dump() for tool in tools],
            temperature=0,
            tool_choice="required",  # forces tool call
        )
        fcts = []
        for tool_call in completion.choices[0].message.tool_calls:
            fcts.append({"name": tool_call.function.name, "arguments": tool_call.function.arguments})
        return fcts


class OllamaCompletion(OpenAICompletion):

    def __init__(self, model, url=None, **args):
        super().__init__(default_model=model, **args)
        self.client = OpenAI(
            base_url=url or "http://127.0.0.1:11434/v1",
            api_key="ollama")

    def parse(self, messages: List[Dict[str, str]], response_format: Type[BaseModel] = None, ) -> str:
        raise NotImplementedError("not implemented")

    def force_tool(self, messages: List[Dict[str, str]], tools: List[Tool]) -> List:
        raise NotImplementedError("not implemented")

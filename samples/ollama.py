from openai import OpenAI
import os
from core.converser import SystemMessage, UserMessage, AssistantMessage, Converser
from core.completion import Completion, OllamaCompletion
client = OpenAI(base_url="http://127.0.0.1:11434/v1",
                api_key="ollama")

ollama = OllamaCompletion(model="llama3.1", default_temperature=0.0)


bob = Converser(completion=ollama,
                instruction="you are a helpful assistant",
                persist="./bob.json")
print(bob.completion)
bob.response("are you sentient?")
print(bob.last_message())
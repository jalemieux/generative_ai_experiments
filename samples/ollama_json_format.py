from typing import Type, Optional

from core.completion import OllamaCompletion, Completion
from core.converser import Converser
from pydantic import BaseModel, Field
import json
import re
class Extractor:
    pass

class IntentClassification(BaseModel):
    primary_intent: Optional[str] = None #= Field(description="primary intent of the author",)
    primary_intent_explanation: Optional[str] = None #= Field(description="explanation of the primary intent classification")
    secondary_intent: Optional[str] = None #= Field(description="secondary intent of the author")
    secondary_intent_explanation: Optional[str] = None #= Field(description="explanation of the secondary intent classification")

p = """
You are a text analysis expert specializing in intent classification. Your task is to analyze the content of a given web page and identify the underlying intents behind the information presented. Please perform the following steps:
Intent Identification: 
Analyze the content and classify the primary and secondary intents of the author. Determine what the author is trying to achieve with this content (e.g., inform, persuade, entertain, promote a product, etc.).
Intent Categorization:
For each identified intent, provide a brief explanation of why you classified it as such, referencing specific parts of the content that led to your conclusion.
Present your findings clearly, listing each intent and its corresponding explanation.

"""
class JSONFormatter:
    """converts text to a given json format"""
    p = f"""
You are an expert in data structuring and JSON formatting. Your task is to process the given input and output the result in a specific JSON format. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Format the Output: Structure your response as JSON in the following format:
```json
{{json_model}}
```
Populate the JSON: Replace the placeholder keys and values with relevant data extracted or derived from the input.
Ensure Correctness: Make sure the JSON is correctly formatted, with appropriate data types (e.g., strings, numbers, arrays, objects) as required by the format.
"""
    def __init__(self, completion: Completion):
        self.converser = Converser(
            completion=completion,
        )

    def convert(self, type: Type[BaseModel], input: str) -> BaseModel:
        self.converser.reset()
        t = type()
        self.converser.set_instruction(self.p.format(json_model=t.json()))
        self.converser.response(f"input: {input}")
        content = self.converser.last_message()
        content_json = re.search(r"```json(.*?)```", content, re.DOTALL).group(1).strip()
        return type(**json.loads(content_json))


ollama = OllamaCompletion(model="llama3.1", default_temperature=0.0)


with open("email.txt", 'r') as f:
    email= f.read()
formatter = JSONFormatter(completion=ollama)
obj = formatter.convert(IntentClassification, email)
print(obj.json())


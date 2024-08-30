import json
from typing import Optional, Type

from pydantic import BaseModel

from core.completion import Completion



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
        from core.converser import Converser
        self.converser = Converser(
            completion=completion,
        )

    def convert(self, type: Type[BaseModel], input: str) -> BaseModel:
        self.converser.reset()
        t = type()
        self.converser.set_instruction(self.p.format(json_model=t.json()))
        self.converser.response(f"input: {input}")
        content = self.converser.last_message()
        return type(**json.loads(content))


class NameExtractor:
    
    """extracts name from a given string"""
    p = f"""
You are an expert in name extraction. Your task is to process the given input and extract the person's name. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Name: Identify and extract the name from the input.
Ensure Correctness: Make sure the name is correctly extracted and formatted.
"""

    def __init__(self, completion: Completion):
        from core.converser import Converser
        self.converser = Converser(
            completion=completion,
            instruction=self.p,
        )


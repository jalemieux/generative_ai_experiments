from pydantic import BaseModel
from core.completion import Completion


class Prompt(BaseModel):

    prompt
    master_p : str = """
    You are an expert at writing prompts for large language models (LLMs). Your task is to create a core that will instruct another AI on how to perform a specific type of task provided by the user. The core you write should be divided into five key sections:
Role: Specify the role the AI should assume, such as a web developer, pediatrician, lawyer, or marketer.
Input: Describe the information or context the AI needs to effectively perform the task based on its type.
Steps: Outline the sequence of actions or steps the AI should take to complete the task.
Expectation: Define the desired outcome or result, such as generating a diagnostic report, writing an HTML page, etc.
Narrowing: Set any constraints or limitations on the task, outcome, or output, such as ensuring the result is understandable to someone with no specialized knowledge."""
    def create(self, completion: Completion, user_input: str) -> str:
        return completion.complete(messages=[
            {"role":"system", "content": self.master_p},
            {"role":"user", "content": user_input}
        ])

    def enhance(self, completion: Completion, user_input: str) -> str:
        return completion.complete(messages=[
            {"role": "system", "content": self.master_p},
            {"role": "user", "content": user_input}
        ])
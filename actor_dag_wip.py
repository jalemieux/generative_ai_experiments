import re
from typing import Type, Optional, List, Dict

from core.completion import OllamaCompletion, Completion
from core.converser import Converser
from pydantic import BaseModel
import json


class Actor:
    converser: Converser

    def __init__(self, name, problem_description):
        self.name = name
        self.problem_description = problem_description
        self.downstream_actors = []

    def register_downstream_actor(self, actor):
        """Register a downstream actor."""
        self.downstream_actors.append(actor)

    def solution(self, request):
        """Implements core logic of this actor"""
        return None

    def solve_problem(self, request, context):
        """Solve the problem and determine the next actor to call."""
        print(f"{self.name}: Solving problem: {self.problem_description}")
        result = self.solution(request)
        context[self.name] = result
        print(f"{self.name}: Problem solved with result: {result}")

        # Determine which downstream actor to call based on the result or description
        if len(self.downstream_actors) == 1:
            actor = self.downstream_actors[0]
            print(f"{self.name}: Passing to {actor.name} based on result: {result}")
            actor.solve_problem(result, context)

        else:
            return
            #raise NotImplementedError
            # for actor in self.downstream_actors:
            #     if actor.problem_description in result:
            #         print(f"{self.name}: Passing to {actor.name} based on result: {result}")
            #         actor.solve_problem(context)

    def describe_problem(self):
        """Expose the description of the problem this actor solves."""
        return self.problem_description


class JsonFormatter(Actor):
    """converts text to json format"""
    type: Type[BaseModel]
    p: str = f"""
    You are an expert in data structuring and JSON formatting. Your task is to process the given input and output the result in a specific JSON format. Please follow these steps:
    Analyze the Input: Carefully read and understand the provided input.
    Format the Output: Structure your response as JSON 
    Populate the JSON: Replace the placeholder keys and values with relevant data extracted or derived from the input.
    Ensure Correctness: Make sure the JSON is correctly formatted, with appropriate data types (e.g., strings, numbers, arrays, objects) as required by the format.
    """

    def __init__(self, completion: Completion, type: Type[BaseModel] = None):
        super().__init__(name="json_formatter",
                         problem_description="formats text to json")
        self.converser = Converser(completion)
        self.type = type

    def solution(self, request):
        self.converser.reset()
        prompt = self.p
        if self.type is not None:
            prompt = prompt + self.type().json()
        self.converser.set_instruction(prompt)
        resp_raw = self.converser.response(f"input: {request}")
        # Search for the pattern in the string
        return re.search(r'```json\s*(\{.*?\})\s*```', resp_raw, re.DOTALL).group(1)


class Clarification(Actor):
    """disambiguate a user request"""
    p: str = f"""
You are a text analysis expert specializing in intent classification. Your task is to analyze the user request and identify the underlying intents behind the information presented. Please perform the following steps:
Intent Identification: Analyze the content and classify the primary and secondary intents of the author. Determine what the author is trying to achieve with this content (e.g., inform, persuade, entertain, promote a product, etc.).
Intent Categorization: For each identified intent, provide a brief explanation of why you classified it as such, referencing specific parts of the content that led to your conclusion.
Present your findings clearly, listing each intent and its corresponding explanation."""

    def __init__(self, completion: Completion):
        self.converser = Converser(completion, instruction=self.p)
        super().__init__(name="clarifier",
                         problem_description="disambiguate user request")

    def solution(self, request):
        return self.converser.response(f"user request: {request}")



class RainbowColors(BaseModel):
    """colors of the rainbow"""
    colors: Optional[List[str]] = None


class Intent(BaseModel):
    """broken down intent"""
    name: Optional[str] = None
    description: Optional[str] = None
    phrases: List[str] = None
    insights: List[Dict[str, str]] = None


class UserIntents(BaseModel):
    """User intents"""
    intents: List[Intent] = None
    overall_intent: str = None


ollama = OllamaCompletion(model="llama3.1", default_temperature=0.0)
# ollama_converser = Converser(ollama)
# actor_a = JsonFormatter(ollama_converser, RainbowColors)
context = {}

actor_0 = Clarification(ollama)
actor_1 = JsonFormatter(ollama, UserIntents)
actor_0.register_downstream_actor(actor_1)

actor_0.solve_problem("what s the colr of the rinabow to my eye", context)

print(context)

# # Create actors
# actor_a = Actor(name="Actor A", problem_description="Problem A", solution_fn=solution_fn_a)
# actor_b = Actor(name="Actor B", problem_description="Problem B", solution_fn=solution_fn_b)
# actor_c = Actor(name="Actor C", problem_description="Problem C", solution_fn=solution_fn_c)
#
# # Register downstream actors
# actor_a.register_downstream_actor(actor_b)
# actor_a.register_downstream_actor(actor_c)
#
# # Example context to hold results
# context = {}
#
# # Start the workflow from actor_a
# actor_a.solve_problem(context)

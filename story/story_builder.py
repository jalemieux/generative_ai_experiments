import sys
from pathlib import Path

# Construct the path to directory2
core_path = Path(__file__).resolve().parent.parent / 'core'
sys.path.insert(0, str(core_path))


from typing import List, Optional
from pydantic import BaseModel

from entities import Character


class Story(BaseModel):
    description: Optional[str] = None
    supporting_characters: Optional[List[Character]] = None
    antagonists: Optional[List[Character]] = None
    plot: Optional[str] = None
    lessons: Optional[List[str]] = None

prompt_story_builder = {
    "story" : f"""
You are an expert in story description. Your task is to process the given input and extract the story description. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Story Description: Identify and extract the story description from the input.
Ensure Correctness: Make sure the story description is correctly extracted and formatted.
""",
}

from completion import OpenAICompletion
from utils import user_input

parse_completion = OpenAICompletion(parse_model="gpt-4o-2024-08-06")


def build_story():
    user_input("Hi there! I'm here to help you create a story. Let's get started!", requires_answer=False)
    new_story = Story()
    input = user_input("What is the story about?")
    new_story = parse_completion.parse([
        {"role": "system", 
         "content": prompt_story_builder["story"]
        }, { "role": "user", "content": input }], Story)
    return new_story

story = build_story()
print(story)

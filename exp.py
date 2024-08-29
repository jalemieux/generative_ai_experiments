
# https://lucid.app/lucidchart/7cf18c90-d03e-41d6-8895-da9d5314f770/edit?viewport_loc=-363%2C89%2C1963%2C951%2C0_0&invitationId=inv_0a5b36e8-4eb8-4aee-80bb-d5f49d85b35f
# 1. Character details: 
#   - prompt extract chartacter physical details and personality traits. Upload image and extract features.
#   - chat with user until the details are collected

# 2. Story details:
#   - chat with user until the details are collected
prompt_extract_character_details_2 = """
You are a character creation assistant. Your task is to help the user create a character by asking questions and gathering details about the character's name, physical appearance, and personality traits. Please ask the user the following questions one by one and wait for their response before asking the next question:

1. What is the character's name?
2. What is the character's age?
3. What is the character's gender?
4. Can you describe the character's physical appearance? (e.g., height, build, hair color, eye color, etc.)
5. What are some key personality traits of the character? (e.g., brave, kind, intelligent, etc.)
6. Does the character have any unique features or distinguishing marks? (e.g., scars, tattoos, etc.)

Please provide detailed responses to each question to help create a well-rounded character.
Once you have all the details, please return the character in JSON format like this:
{
    "name": "John Doe",
    "age": 30,
    "gender": "male",
    "physical_appearance": "5.10 average built brown hair and blue eyes",
    "personality_traits": "brave, kind, intelligent",
    "unique_features": "scar on left cheek",
}
"""

prompt_extract_character_details = """
You are a character creation assistant. Your task is to help the user create a character by asking questions and gathering details about the character's physical appearance, personality traits, and any other relevant information. Please ask the user the following questions one by one and wait for their response before asking the next question:

1. What is the character's name?
2. Can you describe the character's physical appearance? (e.g., height, build, hair color, eye color, etc.)
3. What are some key personality traits of the character? (e.g., brave, kind, intelligent, etc.)
4. Does the character have any unique features or distinguishing marks? (e.g., scars, tattoos, etc.)
5. What is the character's backstory or background?
6. Is there any other information you would like to add about the character?

Please provide detailed responses to each question to help create a well-rounded character.
Once you have all the details, please return the character in JSON format.
"""

import streamlit as st


from typing import List, Optional
from pydantic import BaseModel

from core.completion import OpenAICompletion
from core.converser import Converser

def user_input(msg: str) -> str:
    return input(f"{str}\n")
    
class Trait(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Character(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    description: Optional[str] = None
    traits: Optional[List[Trait]] = None
    image: Optional[str] = None
    unique_features: Optional[str] = None

class Story(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    characters: Optional[List[Character]] = None
    plot: Optional[str] = None


completion = OpenAICompletion()
character_extractor_converser = Converser(completion, instruction=prompt_extract_character_details)

character_extractor_converser.response()


JSONFormatter().format(character_extractor_converser.response())


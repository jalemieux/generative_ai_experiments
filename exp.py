
# https://lucid.app/lucidchart/7cf18c90-d03e-41d6-8895-da9d5314f770/edit?viewport_loc=-363%2C89%2C1963%2C951%2C0_0&invitationId=inv_0a5b36e8-4eb8-4aee-80bb-d5f49d85b35f
# 1. Character details: 
#   - prompt extract chartacter physical details and personality traits. Upload image and extract features.
#   - chat with user until the details are collected

# 2. Story details:
#   - chat with user until the details are collected

# √ TODO: get character details from user : char_builder.py
# TODO: get story details from user
# TODO: generate story
# TODO: generate image
# TODO: generate audio
# TODO: publish content 





import streamlit as st


from typing import List, Optional
from pydantic import BaseModel

from core.completion import OpenAICompletion
from core.converser import Converser
from core.utility import NameExtractor

def user_input(msg: str, requires_answer: bool = True) -> str:
    if requires_answer is False:
        print(f"{msg}\n")
    else:
        return input(f"{msg}\n")
    



class PersonName(BaseModel):
    name: Optional[str] = None


completion = OpenAICompletion()
parse_completion = OpenAICompletion(parse_model="gpt-4o-2024-08-06")
#name_extractor = NameExtractor(completion)
name_extractor = Converser(completion, instruction=prompt_name_extraction)
character_conv = Converser(completion, instruction=prompt_extract_character_details)

user_input("Hi there! I'm here to help you create a character for your story. Let's get started!", requires_answer=False)
char_name_raw = user_input("What is the character's name?")

char_name = parse_completion.parse([{"role": "system", "content": prompt_name_extraction.format(input=char_name_raw)}], Character)

print(char_name)
# user_input("Great! Now let's gather some details about the character's physical appearance, personality traits, and any other relevant information.", requires_answer=False)

# char_age_raw = user_input("What is the character's age?")
# char_age = character_extractor_converser.ask(char_age_raw)

# char_gender_raw = user_input("What is the character's gender?")
# char_gender = character_extractor_converser.ask(char_gender_raw)
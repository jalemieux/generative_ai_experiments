

import sys
from pathlib import Path

# Construct the path to directory2
core_path = Path(__file__).resolve().parent.parent / 'core'
sys.path.insert(0, str(core_path))


import pprint
from typing import List, Optional

from pydantic import BaseModel

from completion import OpenAICompletion

from entities import Character, Trait

# TODO: optimize this prompt!!!
prompt_character_builder = { 
    "name" : f"""
You are an expert in name extraction. Your task is to process the given input and extract the person's name. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Name: Identify and extract the name from the input.
Ensure Correctness: Make sure the name is correctly extracted and formatted.
Input: {{input}}
""",
    "age" : f"""
You are an expert in age extraction. Your task is to process the given input and extract the age. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Age: Identify and extract the age from the input.
Ensure Correctness: Make sure the age is correctly extracted and formatted.

Input: {{input}}
""",
    "gender" : f"""
You are an expert in gender extraction. Your task is to process the given input and extract the gender. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Gender: Identify and extract the gender from the input.
Ensure Correctness: Make sure the gender is correctly extracted and formatted.

Input: {{input}}
""",    
    "physical_description" : f"""
You are an expert in description extraction. Your task is to process the given input and extract the description. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Description: Identify and extract the description from the input.
Ensure Correctness: Make sure the description is correctly extracted and formatted.

Input: {{input}}
""",    
    "personality_traits" : f"""
You are an expert in trait extraction. Your task is to process the given input and extract the traits. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Traits: Identify and extract the traits from the input.
Ensure Correctness: Make sure the traits are correctly extracted and formatted.
""",
    "image" : f"""
You are an expert in image extraction. Your task is to process the given input and extract the image. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Image: Identify and extract the image from the input.
Ensure Correctness: Make sure the image is correctly extracted and formatted.

Input: {{input}}
""",
    "unique_features" : f"""
You are an expert in unique feature extraction. Your task is to process the given input and extract the unique features. Please follow these steps:
Analyze the Input: Carefully read and understand the provided input.
Extract the Unique Features: Identify and extract the unique features from the input.
Ensure Correctness: Make sure the unique features are correctly extracted and formatted.

Input: {{input}}
""",
}


from utils import user_input

parse_completion = OpenAICompletion(parse_model="gpt-4o-2024-08-06")

import sqlite3

conn = sqlite3.connect('characters.db')
c = conn.cursor()


user_input("Hi there! I'm here to help you create a character for your story. Let's get started!", requires_answer=False)
new_char = Character()
#for key in prompt_character_builder.keys():
for key in Character.__annotations__.keys():
    raw_input = user_input(f"What is the character's {key}?")
    parsed_input = parse_completion.parse([
        {"role": "system", "content": prompt_character_builder[key].format(input=raw_input)}], Character)
    setattr(new_char, key, getattr(parsed_input, key))

# Use parameterized queries to safely insert the character data into the database
c.execute('''INSERT INTO characters (name, age, gender, physical_description, personality_traits, image, unique_features) 
             VALUES (?, ?, ?, ?, ?, ?, ?)''', 
          (new_char.name, new_char.age, new_char.gender, new_char.physical_description, 
           ','.join([trait.name for trait in new_char.personality_traits]) if new_char.personality_traits else None, 
           new_char.image, new_char.unique_features))

conn.commit()
conn.close()

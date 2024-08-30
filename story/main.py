from typing import Optional, List

from openai import OpenAI
from pydantic import BaseModel

from core.completion import OllamaCompletion
from core.converser import Converser

class Trait(BaseModel):
    """describes a personality trait"""
    trait: Optional[str] = None

class Character(BaseModel):
    name: Optional[str] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    physical_appearance: Optional[str] = None
    personality: Optional[List[Trait]] = None

    def __str__(self):
        return f"{self.name} is a {self.age} {self.gender}, who looks like {self.physical_appearance}. They are {", ".join([ t .trait for t in self.personality])}"



simple_story_gen_prompt = f"""
Write a heartwarming children’s story given the following details: 
Main characters: 
{{characters}}
Story setting:
{{setting}}
Adventure:
{{adventure}}
Supporting Characters:
{{supporting_characters}}
Lessons: 
{{lessons}}
The story be written with simple language and vivid descriptions to engage young readers.
"""

extract_scenes_from_story_prompt = f"""
You are given a story by the user, your task is to extract details from 3 different scenes that can be used pater on to create illustration.
For each scene, please provide the following information:

Characters: Who is in this scene? Describe their clothing, pose, action and emotion.
Setting: Describe the surroundings. Include details about the environment, time of day, weather, and any significant objects or background elements.
"""
#
# class Scene:
#     characters: Optional[List[str]] = None
#     setting: Optional[str] = None
# class Scenes:
#     scenes: List[Scene] = None




client = OpenAI(base_url="http://127.0.0.1:11434/v1",
                api_key="ollama")

ollama = OllamaCompletion(model="llama3.1", default_temperature=0.2)


def generate_story(characters: List[Character],
                   supporting_characters: List[Character],
                   setting: str,
                   adventure: str,
                   lessons:str):
    story_prompt = simple_story_gen_prompt.format(
        characters=[char.str() for char in characters],
        supporting_characters=[char.str() for char in supporting_characters],
        lessons=lessons,
        adventure=adventure,
        setting=setting
    )
    print(story_prompt)
    # story_teller = Converser(completion=ollama,
    #             instruction=simple_story_gen_prompt,
    #             persist="./story_teller.json")
    #story = story_teller.response("")

ogen = Character(name="ogen",
                 age="6",
                 gender="boy",
                 physical_apperance="tall slim white tanned kids with freckles brow eyes and brow hair"
                 personality=)

generate_story(characters=)

#
# scene_detail_extractor = Converser(completion=ollama,
#                 instruction=extract_scenes_from_story_prompt,
#                 persist="./scene_detail_extractor.json")
# details = scene_detail_extractor.response(f"Story: {story}")
#
# print(details)
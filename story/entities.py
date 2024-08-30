    
from typing import List, Optional
from pydantic import BaseModel


class Trait(BaseModel):
    name: Optional[str] = None

class Character(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    physical_description: Optional[str] = None
    personality_traits: Optional[List[Trait]] = None
    image: Optional[str] = None
    unique_features: Optional[str] = None
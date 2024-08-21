from pydantic import BaseModel
from typing import Dict

class Actor(BaseModel):
    name: str = "Actor"
    def run(self, *args) -> Dict:
        pass

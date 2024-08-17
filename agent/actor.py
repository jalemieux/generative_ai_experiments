from pydantic import BaseModel
from typing import Dict

class Actor(BaseModel):
    def run(self, *args) -> Dict:
        pass

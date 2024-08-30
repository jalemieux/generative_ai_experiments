from core.completion import Completion
from core.converser import Converser


class Instructor(Converser):
    def __init__(self, completion: Completion, instruction: str):
        super().__init__(completion, instruction)

    
        
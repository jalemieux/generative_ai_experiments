from pydantic import BaseModel
class Actor:
    name: str = "Actor"

    def run(self, *args):
        pass

    def tool(self):
        pass
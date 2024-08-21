from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from core.actor import Actor


class Parameter(BaseModel):
    type: str
    name: str
    description: str
    required: bool = Field(default=True)
    enum: Optional[List[str]] = None





class Tool(BaseModel):
    name: str
    description: str
    parameters: List[Parameter]
    actor: Optional[Actor] = None

    def dump(self) -> Dict:
        out = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
            }
        }
        for parameter in self.parameters:
            required = []
            chunk = {
                "type": parameter.type,
                "description": parameter.description
            }
            if parameter.type == "array":
                chunk["items"] = {"type": "string"}

            if parameter.enum is not None:
                chunk["enum"] = parameter.enum

            out["function"]["parameters"]["properties"][parameter.name] = chunk

            if parameter.required is True:
                required.append(parameter.name)

        return out


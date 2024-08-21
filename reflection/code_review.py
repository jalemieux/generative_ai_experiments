# What, why, how
#
# Bob writes code and explanation based on requirements
# Fred is asked to write his own code based on same requirements, then asked to compare his code with Bob
# Fred provide his code review with a list of bugs and whether the code is correct.
# Frank reviews Bob code and explanation, and Fred's review to determine whether the review was correct

from core.converser import Converser
from core.completion import OpenAICompletion
from pydantic import BaseModel, Field

from typing import List
import json

class AICode(BaseModel):
    python_code: str
    explanation: str

class Bug(BaseModel):
    python_code: str
    explanation: str
class CodeReview(BaseModel):
    bugs: List[Bug]
    """summary of bugs"""
    review_comments: str = Field(description="summary of bugs")
    accepted: bool

client = OpenAICompletion()
# Bob is the dev
bob = Converser(client, instruction="write python code that minimize the number of tokens in a string")
bob_code = bob.response("", response_obj=AICode) # python_code, explanation

fred = Converser(client,instruction= "Write python code that implements the provided requirements: ")
fred_code = fred.response("requirements: minimize the number of tokens in a string", response_obj=AICode)

# Fred is the reviewer
fred_review = fred.response(
    f"compare your code with the code provided and evaluate if the code provided has any bugs. Code:{{code}}".format(code=bob_code.python_code),
    response_obj=CodeReview
    )

# Frank is the manager
frank = Converser(client, instruction="Review the provided code and code review and evaluate if the review is correct.")
frank_resp = frank.response(f"code: ```{bob_code.python_code}```, code review: {fred_review.json()}")
print(frank.last_message())






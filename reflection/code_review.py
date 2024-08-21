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
    def __str__(self):
        return f"```{self.python_code}```{self.explanation}\n"
class CodeReview(BaseModel):
    bugs: List[Bug]
    """summary of bugs"""
    review_comments: str = Field(description="summary of bugs")
    """true if the code is ok, false if there is at least 1 bug"""
    accepted: bool = Field(description="true if the code is ok, false if there is at least 1 bug")

client = OpenAICompletion()
#Bob is the dev
bob = Converser(client, instruction="write python code that minimize the number of tokens in a string",
                persist="./bob.json")
bob_code = bob.response("", response_obj=AICode) # python_code, explanation

# # Fred is the reviewer
fred = Converser(client,instruction= "Write python code that implements the provided requirements: ",
                 persist="./fred.json")
fred_code = fred.response("requirements: minimize the number of tokens in a string", response_obj=AICode)

fred_review = fred.response(
    f"compare your code with the code provided and evaluate if the code provided has any bugs. Code:{{code}}".format(code=bob_code.python_code),
    response_obj=CodeReview
    )
# back to Bob for code fix
feedback_to_bob = f"""
Evaluate the following code review feedback and fix your code accordingly.
Code Review: {{comments}}
Bugs (if any): 
{{bugs}}
Code passed review: {{status}}
""".format(
    comments=fred_review.review_comments,
    bugs="\n".join([str(bug) for bug in fred_review.bugs]),
    status=fred_review.accepted
)

bob.response(feedback_to_bob)


# # Frank is the reviewer's reviewer
# frank = Converser(client, instruction="you are given code, and a code review. your task is evaluate if the review correctly accepts or reject the code.")
# frank_resp = frank.response(f"code: ```{bob_code.python_code}```, code review: bugs: {{bugs}}, {fred_review.json()}.")







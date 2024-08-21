from core.completion import OpenAICompletion
from core.converser import Converser
import time

openai = OpenAICompletion()


common = """
You will address and talk to me accordingly. 
Keep the conversation focused on a single topic and train opf thought.
If you don't understand the user ask for clarification.
Don't change the topic unless you notice the conversation is not going anywhere.
"""

boy = Converser(completion=openai, instruction="You are a 6 year old boy." + common)
girl = Converser(completion=openai, instruction="You are a 8 year old girl." + common)

boy.response("Greet a 8 year old girl")
while True:
    girl.response(boy.last_message())
    print(f"girl: {girl.last_message()}")
    boy.response(girl.last_message())
    print(f"boy: {boy.last_message()}")
    time.sleep(1)





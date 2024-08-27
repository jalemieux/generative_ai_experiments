from typing import List, Dict
from openai import OpenAI
from core.utility import Actor
import json
import re
openai_client = OpenAI()


class Coder(Actor):
    name = "coder"

    llm1_messages: List[Dict[str, str]] = [
        {"role": "system", "content": "You are a helpful assistant that specializes in producing bug free python code."
                                      "The user will provide you with the input, logic to be implemented, and expected output."
                                      "Your output should be python code only."
                                      "if you include usage examples, comment them out. "
                                      "any instructions should be in comments."
                                      "the code should be executable in a interpreter without having to modify it."}
    ]
    llm2_messages: List[Dict[str, str]] = [
        {"role": "system",
         "content": "You are a helpful assistant that reviews the user's python code, describes any syntax errors and bugs"
                    " Be clear, detailed enough about the issues to be resolved."
                    "if no issues are found, you should restrict your output to only: OK"
         }
    ]
    llm3_messages: List[Dict[str, str]] = [
        {"role": "system",
         "content": "You are a helpful assistant that writes unit tests for python code. Given input and expected output"
                    " by the user write unit tests to the best of your ability."
                    "Your output should be python code only."
         }
    ]

    def completion(self, messages):
        completion = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            #tools=[tool.dump() for tool in self.tools],
            temperature=0,
            #tool_choice="required",  # forces tool call
        )
        return completion.choices[0].message.content

    def validation_loop(self, messages_gen, messages_val):
        while True:
            # Generation
            response = self.completion(messages_gen)
            messages_gen.append({"role": "system", "content": response})
            print(f"response: {response}")
            # Validation
            messages_val.append({"role": "user", "content": response})
            response_review = self.completion(messages_val)
            print(f"response review feedback: {response_review}")
            messages_val.append({"role": "system", "content": response_review})

            # todo: need to find a better way to detect end condition
            if response_review.rstrip()[-2:] == "OK":
                print("response satisfactory...")
                break

        return response


    def run(self, *args) -> Dict:
        arguments = json.loads(args[0])
        input = ", ".join(arguments["input"])
        output = ", ".join(arguments["output"])
        logic = ", ".join(arguments["logic"])
        u_message = f"intput: {input}\nlogic: {logic}\n expected output: {output}"

        #todo:
        # 1 - becoming clear to me as i debug this code that the validator's messages are not to be carried from one validation loop to another.
        # 2 - the messages here are not summarized when reaching the LLM context window. That's fine as long as the loop doesn't go thru too many iterations.

        # ask LLM to write code, ask another LLM to validate it
        self.llm1_messages.append({"role": "user", "content": u_message})
        code = self.validation_loop(self.llm1_messages, [self.llm2_messages[0]])

        # ask LLM to write test code, ask another LLM to validate it
        self.llm3_messages.append({"role": "user", "content": code})
        test_code = self.validation_loop(self.llm3_messages, [self.llm2_messages[0]])

        code_match = re.search(r"```python(.*?)```", code, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()

        test_code_match = re.search(r"```python(.*?)```", test_code, re.DOTALL)
        if test_code_match:
            test_code = test_code_match.group(1).strip()

        return {"code": code, "test_code": test_code}

    # LLM to write unit test

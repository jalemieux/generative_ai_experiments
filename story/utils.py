def user_input(msg: str, requires_answer: bool = True) -> str:
    if requires_answer is False:
        print(f"{msg}\n")
    else:
        return input(f"{msg}\n")


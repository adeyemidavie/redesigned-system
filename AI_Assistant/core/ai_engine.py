import ollama

MODEL = "gemma3:4b"


def ask_ai(messages):

    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    return response["message"]["content"]
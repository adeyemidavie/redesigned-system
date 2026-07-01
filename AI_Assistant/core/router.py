def route(message):

    message = message.lower()

    if message.startswith("open "):
        return "command"

    if any(
        x in message
        for x in [
            ".pdf",
            ".docx",
            ".txt",
            ".csv"
        ]
    ):
        return "file"

    if any(
        x in message
        for x in [
            "image",
            "photo",
            "picture",
            "screenshot"
        ]
    ):
        return "vision"

    return "chat"
from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from core.ai_engine import ask_ai
from core.storage import (
    init_db,
    create_chat,
    save_message,
    get_messages,
    get_chats,
    rename_chat,
    delete_chat
)

from core.tools import handle_command

app = Flask(__name__)

init_db()

CURRENT_CHAT = create_chat()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    global CURRENT_CHAT

    data = request.json

    user_message = data["message"]

    save_message(
        CURRENT_CHAT,
        "user",
        user_message
    )

    command = handle_command(user_message)

    if command:

        save_message(
            CURRENT_CHAT,
            "assistant",
            command
        )

        return jsonify({
            "reply": command
        })

    history = get_messages(
        CURRENT_CHAT
    )

    ai_reply = ask_ai(
        history
    )

    save_message(
        CURRENT_CHAT,
        "assistant",
        ai_reply
    )

    return jsonify({
        "reply": ai_reply
    })


@app.route("/new-chat", methods=["POST"])
def new_chat():

    global CURRENT_CHAT

    CURRENT_CHAT = create_chat()

    return jsonify({
        "chat_id": CURRENT_CHAT
    })


@app.route("/chats")
def chats():

    return jsonify(
        get_chats()
    )


@app.route(
    "/delete-chat/<int:chat_id>",
    methods=["POST"]
)
def remove(chat_id):

    delete_chat(chat_id)

    return jsonify({
        "success": True
    })


@app.route(
    "/rename-chat",
    methods=["POST"]
)
def rename():

    data = request.json

    rename_chat(
        data["chat_id"],
        data["title"]
    )

    return jsonify({
        "success": True
    })


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )
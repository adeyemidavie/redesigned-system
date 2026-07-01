const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendButton = document.getElementById("send-btn");
const newChatButton = document.getElementById("new-chat-btn");
const fileInput = document.getElementById("file-input");
const previewArea = document.getElementById("preview-area");

/* ----------------------------
   Auto Resize Textarea
-----------------------------*/

messageInput.addEventListener("input", () => {

    messageInput.style.height = "auto";
    messageInput.style.height = messageInput.scrollHeight + "px";

});

/* ----------------------------
   Add Message
-----------------------------*/

function addMessage(role, text) {

    const message = document.createElement("div");
    message.className = `message ${role}`;

    message.innerHTML = `

        <div class="message-content">

            ${
                role === "assistant"
                ? '<div class="avatar">🤖</div>'
                : ''
            }

            <div>

                <div class="bubble">

                    ${text}

                </div>

            </div>

            ${
                role === "user"
                ? '<div class="avatar">👤</div>'
                : ''
            }

        </div>

    `;

    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;

}

/* ----------------------------
   Typing Bubble
-----------------------------*/

function addTyping() {

    const div = document.createElement("div");

    div.className = "message assistant";

    div.id = "typing";

    div.innerHTML = `

        <div class="message-content">

            <div class="avatar">

                🤖

            </div>

            <div class="bubble">

                <div class="typing">

                    <span></span>

                    <span></span>

                    <span></span>

                </div>

            </div>

        </div>

    `;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;

}

/* ----------------------------
   Remove Typing
-----------------------------*/

function removeTyping() {

    const typing = document.getElementById("typing");

    if (typing) typing.remove();

}

/* ----------------------------
   Send Message
-----------------------------*/

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) return;

    if (chatBox.querySelector(".welcome")) {

        chatBox.innerHTML = "";

    }

    addMessage("user", message);

    messageInput.value = "";

    messageInput.style.height = "56px";

    addTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: message

            })

        });

        const data = await response.json();

        removeTyping();

        addMessage(

            "assistant",

            data.reply

        );

    }

    catch (err) {

        removeTyping();

        addMessage(

            "assistant",

            "❌ Connection error."

        );

        console.error(err);

    }

}

/* ----------------------------
   New Chat
-----------------------------*/

async function newChat() {

    try {

        await fetch("/new-chat", {

            method: "POST"

        });

    } catch {}

    chatBox.innerHTML = `

        <div class="welcome">

            <h1>

                👋 New Chat

            </h1>

            <p>

                Ask me anything.

            </p>

        </div>

    `;

}

/* ----------------------------
   File Upload Preview
-----------------------------*/

fileInput.addEventListener(

    "change",

    () => {

        previewArea.innerHTML = "";

        [...fileInput.files].forEach(file => {

            const card = document.createElement("div");

            card.className = "preview-card";

            if (file.type.startsWith("image")) {

                const img = document.createElement("img");

                img.src = URL.createObjectURL(file);

                card.appendChild(img);

            }

            const name = document.createElement("div");

            name.innerHTML = `

                <strong>${file.name}</strong>

                <br>

                ${(file.size / 1024).toFixed(1)} KB

            `;

            card.appendChild(name);

            previewArea.appendChild(card);

        });

    }

);

/* ----------------------------
   Drag & Drop
-----------------------------*/

document.addEventListener(

    "dragover",

    e => {

        e.preventDefault();

    }

);

document.addEventListener(

    "drop",

    e => {

        e.preventDefault();

        fileInput.files = e.dataTransfer.files;

        fileInput.dispatchEvent(

            new Event("change")

        );

    }

);

/* ----------------------------
   Enter Key
-----------------------------*/

messageInput.addEventListener(

    "keydown",

    e => {

        if (

            e.key === "Enter"

            &&

            !e.shiftKey

        ) {

            e.preventDefault();

            sendMessage();

        }

    }

);

/* ----------------------------
   Buttons
-----------------------------*/

sendButton.addEventListener(

    "click",

    sendMessage

);

newChatButton.addEventListener(

    "click",

    newChat

);
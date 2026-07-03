const chatWindow = document.getElementById("chat-window");
const questionBox = document.getElementById("question");
const sendButton = document.getElementById("send-button");


function addMessage(text, cssClass) {

    const message = document.createElement("div");

    message.className = `message ${cssClass}`;

    message.textContent = text;

    chatWindow.appendChild(message);

    chatWindow.scrollTop = chatWindow.scrollHeight;

    return message;

}


async function askQuestion() {

    const question = questionBox.value.trim();

    if (!question) {
        return;
    }

    addMessage(
        question,
        "user",
    );

    questionBox.value = "";

    const assistantMessage = addMessage(
        "",
        "assistant",
    );

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/ask/stream",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({
                    question: question,
                }),
            }
        );

        const reader = response.body.getReader();

        const decoder = new TextDecoder();

        while (true) {

            const { done, value } = await reader.read();

            if (done) {
                break;
            }

            assistantMessage.textContent += decoder.decode(
                value,
                {
                    stream: true,
                },
            );

            chatWindow.scrollTop = chatWindow.scrollHeight;

        }

    }

    catch (error) {

        assistantMessage.textContent =
            "Unable to connect to FastAPI.";

        console.error(error);

    }

}


sendButton.addEventListener(
    "click",
    askQuestion,
);


questionBox.addEventListener(
    "keydown",
    function (event) {

        if (
            event.key === "Enter"
            &&
            !event.shiftKey
        ) {

            event.preventDefault();

            askQuestion();

        }

    },
);
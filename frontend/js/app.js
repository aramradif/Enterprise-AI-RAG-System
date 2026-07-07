import {
    evaluateQuestion,
    streamQuestion,
} from "./api.js";

const workspace = document.getElementById("workspace");
const navButtons = document.querySelectorAll(".nav-item");

let chatMessages = [];

function renderChatView() {
    workspace.innerHTML = `
        <section id="chat-section">
            <div id="chat-window"></div>

            <div class="input-area">
                <textarea
                    id="question"
                    placeholder="Ask a question..."
                ></textarea>

                <button id="send-button">
                    Send
                </button>
            </div>
        </section>
    `;

    initializeChat();
    restoreChatMessages();
}

function renderEvaluationView() {
    workspace.innerHTML = `
        <section class="evaluation-view">

            <h2>Enterprise Evaluation Dashboard</h2>

            <p>
                Ask a question and inspect retrieval latency, LLM latency,
                token usage, document count, and estimated cost.
            </p>

            <div class="evaluation-input">
                <textarea
                    id="evaluation-question"
                    placeholder="Ask an evaluation question..."
                ></textarea>

                <button id="evaluation-button">
                    Evaluate
                </button>
            </div>

            <div id="evaluation-results"></div>

        </section>
    `;

    initializeEvaluation();
}

function renderPlaceholderView(title, description) {
    workspace.innerHTML = `
        <section class="placeholder-view">
            <h2>${title}</h2>
            <p>${description}</p>

            <div class="placeholder-card">
                Coming in a future milestone.
            </div>
        </section>
    `;
}

function setActiveButton(selectedButton) {
    navButtons.forEach((button) => {
        button.classList.remove("active");
    });

    selectedButton.classList.add("active");
}

function initializeNavigation() {
    navButtons.forEach((button) => {
        button.addEventListener("click", () => {
            setActiveButton(button);

            const view = button.dataset.view;

            if (view === "chat") {
                renderChatView();
            }

            if (view === "evaluation") {
                renderEvaluationView();
            }

            if (view === "sessions") {
                renderPlaceholderView(
                    "Sessions",
                    "Review conversation sessions and memory state."
                );
            }

            if (view === "logs") {
                renderPlaceholderView(
                    "Logs",
                    "Inspect structured request logs and observability data."
                );
            }

            if (view === "settings") {
                renderPlaceholderView(
                    "Settings",
                    "Configure models, retrieval behavior, and system parameters."
                );
            }
        });
    });
}

function restoreChatMessages() {
    const chatWindow = document.getElementById("chat-window");

    chatMessages.forEach((message) => {
        const messageElement = document.createElement("div");

        messageElement.className = `message ${message.cssClass}`;
        messageElement.textContent = message.text;

        chatWindow.appendChild(messageElement);
    });

    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function initializeChat() {
    const chatWindow = document.getElementById("chat-window");
    const questionBox = document.getElementById("question");
    const sendButton = document.getElementById("send-button");

    function addMessage(text, cssClass, saveMessage = true) {
        const message = document.createElement("div");

        message.className = `message ${cssClass}`;
        message.textContent = text;

        chatWindow.appendChild(message);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        if (saveMessage) {
            chatMessages.push({
                text: text,
                cssClass: cssClass,
            });
        }

        return message;
    }

    async function askQuestion() {
        const question = questionBox.value.trim();

        if (!question) {
            return;
        }

        addMessage(question, "user");

        questionBox.value = "";

        const assistantMessage = addMessage("", "assistant");

        const assistantIndex = chatMessages.length - 1;

        try {
            const reader = await streamQuestion(question);
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();

                if (done) {
                    break;
                }

                const chunk = decoder.decode(value, {
                    stream: true,
                });

                assistantMessage.textContent += chunk;

                chatMessages[assistantIndex].text =
                    assistantMessage.textContent;

                chatWindow.scrollTop = chatWindow.scrollHeight;
            }
        }

        catch (error) {
            assistantMessage.textContent =
                "Unable to connect to FastAPI.";

            chatMessages[assistantIndex].text =
                assistantMessage.textContent;

            console.error(error);
        }
    }

    sendButton.addEventListener("click", askQuestion);

    questionBox.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            askQuestion();
        }
    });
}

function initializeEvaluation() {
    const questionBox = document.getElementById("evaluation-question");
    const button = document.getElementById("evaluation-button");
    const results = document.getElementById("evaluation-results");

    async function runEvaluation() {
        const question = questionBox.value.trim();

        if (!question) {
            return;
        }

        results.innerHTML = `
            <div class="placeholder-card">
                Running evaluation...
            </div>
        `;

        try {
            const data = await evaluateQuestion(question);

            const metrics = data.metrics;

            results.innerHTML = `
                <div class="evaluation-answer">
                    <h3>Answer</h3>
                    <p>${data.answer}</p>
                </div>

                <div class="metrics-grid">

                    <div class="metric-card">
                        <span>Retrieval Time</span>
                        <strong>${metrics.retrieval.retrieval_time_ms} ms</strong>
                    </div>

                    <div class="metric-card">
                        <span>LLM Time</span>
                        <strong>${metrics.generation.llm_time_ms} ms</strong>
                    </div>

                    <div class="metric-card">
                        <span>Documents Retrieved</span>
                        <strong>${metrics.retrieval.documents_retrieved}</strong>
                    </div>

                    <div class="metric-card">
                        <span>Context Length</span>
                        <strong>${metrics.retrieval.context_length_chars}</strong>
                    </div>

                    <div class="metric-card">
                        <span>Prompt Tokens</span>
                        <strong>${metrics.generation.prompt_tokens}</strong>
                    </div>

                    <div class="metric-card">
                        <span>Completion Tokens</span>
                        <strong>${metrics.generation.completion_tokens}</strong>
                    </div>

                    <div class="metric-card">
                        <span>Total Tokens</span>
                        <strong>${metrics.generation.total_tokens}</strong>
                    </div>

                    <div class="metric-card">
                        <span>Estimated Cost</span>
                        <strong>$${metrics.cost.estimated_cost_usd}</strong>
                    </div>

                </div>
            `;
        }

        catch (error) {
            results.innerHTML = `
                <div class="placeholder-card">
                    Unable to run evaluation.
                </div>
            `;

            console.error(error);
        }
    }

    button.addEventListener("click", runEvaluation);

    questionBox.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            runEvaluation();
        }
    });
}

initializeNavigation();
initializeChat();
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
                renderPlaceholderView(
                    "Evaluation Dashboard",
                    "Monitor retrieval latency, LLM latency, token usage, and estimated cost."
                );
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
                renderSettingsView();
                    
                    
                
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
function renderSettingsView() {
    workspace.innerHTML = `
        <section class="settings-view">
            <div class="page-heading">
                <h2>Platform Settings</h2>
                <p>
                    Review the current AI configuration, knowledge base,
                    conversation features, evaluation tools, and platform status.
                </p>
            </div>

            <div class="settings-grid">
                <div class="settings-card">
                    <h3>AI Configuration</h3>

                    <div class="setting-row">
                        <span>Model</span>
                        <strong>GPT-4o-mini</strong>
                    </div>

                    <div class="setting-row">
                        <span>Streaming</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Temperature</span>
                        <strong>0.7</strong>
                    </div>

                    <div class="setting-row">
                        <span>Top-K Retrieval</span>
                        <strong>3</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Knowledge Base</h3>

                    <div class="setting-row">
                        <span>Vector Database</span>
                        <strong>ChromaDB</strong>
                    </div>

                    <div class="setting-row">
                        <span>Embedding Model</span>
                        <strong>text-embedding-3-small</strong>
                    </div>

                    <div class="setting-row">
                        <span>Document Types</span>
                        <strong>PDF, DOCX, TXT, MD</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Conversation</h3>

                    <div class="setting-row">
                        <span>Conversation Memory</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Session History</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>AI Summaries</span>
                        <strong>Enabled</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Evaluation & Observability</h3>

                    <div class="setting-row">
                        <span>Evaluation Metrics</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Request Logging</span>
                        <strong>Enabled</strong>
                    </div>

                    <div class="setting-row">
                        <span>Cost Tracking</span>
                        <strong>Enabled</strong>
                    </div>
                </div>

                <div class="settings-card">
                    <h3>Platform Information</h3>

                    <div class="setting-row">
                        <span>Platform Version</span>
                        <strong>v1.9.0</strong>
                    </div>

                    <div class="setting-row">
                        <span>Backend</span>
                        <strong>FastAPI</strong>
                    </div>

                    <div class="setting-row">
                        <span>Environment</span>
                        <strong>Development</strong>
                    </div>
                </div>
            </div>
        </section>
    `;
}
initializeNavigation();
initializeChat();
import {
    clearSessionMessages,
    createSession,
    deleteSession,
    evaluateQuestion,
    getLogs,
    getSession,
    getSessions,
    streamQuestion,
} from "./api.js";


const workspace = document.getElementById("workspace");
const navButtons = document.querySelectorAll(".nav-item");

let activeSessionId = "enterprise-demo";
let chatMessages = [];


function escapeHtml(value) {
    const element = document.createElement("div");

    element.textContent = String(value ?? "");

    return element.innerHTML;
}


function formatDateTime(timestamp) {
    const date = new Date(timestamp);

    return date.toLocaleString([], {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
    });
}


function formatTime(timestamp) {
    const date = new Date(timestamp);

    return date.toLocaleTimeString([], {
        hour: "numeric",
        minute: "2-digit",
    });
}


function renderChatView() {
    workspace.innerHTML = `
        <section id="chat-section">

            <div class="chat-session-bar">
                <span>
                    Active Session:
                    <strong id="active-session-label">
                        ${escapeHtml(activeSessionId)}
                    </strong>
                </span>
            </div>

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

            <div class="evaluation-session-label">
                Active Session:
                <strong>${escapeHtml(activeSessionId)}</strong>
            </div>

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


async function renderSessionsView() {
    workspace.innerHTML = `
        <section class="evaluation-view">

            <div class="dashboard-header">

                <div>
                    <h2>Enterprise Sessions Dashboard</h2>

                    <p>
                        Create, inspect, clear, and delete conversation
                        sessions and their message histories.
                    </p>
                </div>

                <div class="session-header-actions">

                    <button
                        id="create-session-button"
                        class="secondary-action-button"
                    >
                        ＋ New Session
                    </button>

                    <button
                        id="refresh-sessions-button"
                        class="primary-action-button"
                    >
                        ↻ Refresh
                    </button>

                </div>

            </div>

            <div id="sessions-results">
                <div class="placeholder-card">
                    Loading sessions...
                </div>
            </div>

        </section>
    `;

    const createButton = document.getElementById(
        "create-session-button"
    );

    const refreshButton = document.getElementById(
        "refresh-sessions-button"
    );

    createButton.addEventListener(
        "click",
        handleCreateSession
    );

    refreshButton.addEventListener(
        "click",
        renderSessionsView
    );

    const results = document.getElementById(
        "sessions-results"
    );

    try {
        const sessions = await getSessions();

        if (!sessions.length) {
            results.innerHTML = `
                <div class="placeholder-card">
                    <h3>No sessions found</h3>

                    <p>
                        Create a new session or send a chat message
                        to begin.
                    </p>
                </div>
            `;

            return;
        }

        const totalSessions = sessions.length;

        const totalMessages = sessions.reduce(
            (sum, session) => {
                return sum + Number(
                    session.message_count || 0
                );
            },
            0
        );

        const activeSessionExists = sessions.some(
            (session) => {
                return session.session_id === activeSessionId;
            }
        );

        const newestSession = sessions[0];

        const rows = sessions
            .map((session, index) => {
                const isActive =
                    session.session_id === activeSessionId;

                return `
                    <tr class="${isActive ? "active-session-row" : ""}">

                        <td>${index + 1}</td>

                        <td>
                            <div class="session-id-cell">
                                <strong>
                                    ${escapeHtml(session.session_id)}
                                </strong>

                                ${
                                    isActive
                                        ? `
                                            <span class="active-session-badge">
                                                Active
                                            </span>
                                        `
                                        : ""
                                }
                            </div>
                        </td>

                        <td>
                            ${Number(session.message_count)}
                        </td>

                        <td>
                            ${formatDateTime(session.created_at)}
                        </td>

                        <td>
                            ${formatDateTime(session.last_active_at)}
                        </td>

                        <td>
                            <div class="session-row-actions">

                                <button
                                    class="session-action-button view-session-button"
                                    data-session-id="${escapeHtml(
                                        session.session_id
                                    )}"
                                >
                                    View
                                </button>

                                <button
                                    class="session-action-button use-session-button"
                                    data-session-id="${escapeHtml(
                                        session.session_id
                                    )}"
                                >
                                    Use in Chat
                                </button>

                                <button
                                    class="session-action-button clear-session-button"
                                    data-session-id="${escapeHtml(
                                        session.session_id
                                    )}"
                                >
                                    Clear
                                </button>

                                <button
                                    class="session-action-button danger-session-button delete-session-button"
                                    data-session-id="${escapeHtml(
                                        session.session_id
                                    )}"
                                >
                                    Delete
                                </button>

                            </div>
                        </td>

                    </tr>
                `;
            })
            .join("");

        results.innerHTML = `
            <div class="metrics-grid sessions-summary-grid">

                <div class="metric-card">
                    <span>Total Sessions</span>
                    <strong>${totalSessions}</strong>
                </div>

                <div class="metric-card">
                    <span>Total Messages</span>
                    <strong>${totalMessages}</strong>
                </div>

                <div class="metric-card">
                    <span>Active Session</span>
                    <strong>
                        ${
                            activeSessionExists
                                ? escapeHtml(activeSessionId)
                                : "None"
                        }
                    </strong>
                </div>

                <div class="metric-card">
                    <span>Latest Activity</span>
                    <strong>
                        ${formatTime(newestSession.last_active_at)}
                    </strong>
                </div>

            </div>

            <div class="sessions-table-wrapper">

                <table class="logs-table sessions-table">

                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Session ID</th>
                            <th>Messages</th>
                            <th>Created</th>
                            <th>Last Active</th>
                            <th>Actions</th>
                        </tr>
                    </thead>

                    <tbody>
                        ${rows}
                    </tbody>

                </table>

            </div>
        `;

        initializeSessionActions();
    }

    catch (error) {
        results.innerHTML = `
            <div class="placeholder-card error-card">
                Unable to load sessions.
            </div>
        `;

        console.error(error);
    }
}


async function handleCreateSession() {
    const button = document.getElementById(
        "create-session-button"
    );

    button.disabled = true;
    button.textContent = "Creating...";

    try {
        const session = await createSession();

        activeSessionId = session.session_id;
        chatMessages = [];

        await renderSessionsView();
    }

    catch (error) {
        alert(error.message);

        button.disabled = false;
        button.textContent = "＋ New Session";

        console.error(error);
    }
}


function initializeSessionActions() {
    const viewButtons = document.querySelectorAll(
        ".view-session-button"
    );

    const useButtons = document.querySelectorAll(
        ".use-session-button"
    );

    const clearButtons = document.querySelectorAll(
        ".clear-session-button"
    );

    const deleteButtons = document.querySelectorAll(
        ".delete-session-button"
    );

    viewButtons.forEach((button) => {
        button.addEventListener("click", () => {
            renderSessionDetail(
                button.dataset.sessionId
            );
        });
    });

    useButtons.forEach((button) => {
        button.addEventListener("click", () => {
            useSessionInChat(
                button.dataset.sessionId
            );
        });
    });

    clearButtons.forEach((button) => {
        button.addEventListener("click", () => {
            handleClearSession(
                button.dataset.sessionId
            );
        });
    });

    deleteButtons.forEach((button) => {
        button.addEventListener("click", () => {
            handleDeleteSession(
                button.dataset.sessionId
            );
        });
    });
}


async function renderSessionDetail(sessionId) {
    workspace.innerHTML = `
        <section class="evaluation-view">

            <div class="dashboard-header">
            <div>
    <h2>Conversation History</h2>

    <p id="session-status">
        Loading conversation...
    </p>
</div>


                <button
                    id="back-to-sessions-button"
                    class="primary-action-button"
                >
                    ← Back to Sessions
                </button>

            </div>

            <div id="session-detail-results">
                <div class="placeholder-card">
                    Loading conversation...
                </div>
            </div>

        </section>
    `;

    document
        .getElementById("back-to-sessions-button")
        .addEventListener(
            "click",
            renderSessionsView
        );

    const results = document.getElementById(
        "session-detail-results"
    );

    try {
        const session = await getSession(sessionId);
        const status = document.getElementById("session-status");

status.style.display = "none";

        const messages = session.messages
            .map((message, index) => {
                const roleClass =
                    message.role === "user"
                        ? "session-user-message"
                        : "session-assistant-message";

                const roleLabel =
                    message.role === "user"
                        ? "User"
                        : "Assistant";

                return `
                    <article class="session-message ${roleClass}">

                        <div class="session-message-header">
                            <span>
                                ${message.role === "user" ? "👤" : "🤖"}
                                ${roleLabel}
                            </span>

                            <span>
                                Message ${index + 1}
                            </span>
                        </div>

                        <p>
                            ${escapeHtml(message.content)}
                        </p>

                    </article>
                `;
            })
            .join("");

        results.innerHTML = `
            <div class="session-detail-header">

                <div>
                    <span>Session ID</span>
                    <strong>
                        ${escapeHtml(session.session_id)}
                    </strong>
                </div>

                <div>
                    <span>Messages</span>
                    <strong>${session.message_count}</strong>
                </div>

                <div>
                    <span>Created</span>
                    <strong>
                        ${formatDateTime(session.created_at)}
                    </strong>
                </div>

                <div>
                    <span>Last Active</span>
                    <strong>
                        ${formatDateTime(session.last_active_at)}
                    </strong>
                </div>

            </div>

            <div class="session-detail-actions">

                <button
                    id="use-detail-session-button"
                    class="primary-action-button"
                >
                    Use in Chat
                </button>

                <button
                    id="clear-detail-session-button"
                    class="secondary-action-button"
                >
                    Clear Messages
                </button>

                <button
                    id="delete-detail-session-button"
                    class="danger-action-button"
                >
                    Delete Session
                </button>

            </div>

            <div class="conversation-history">

                ${
                    messages
                    || `
                        <div class="placeholder-card">
                            This session does not contain any messages.
                        </div>
                    `
                }

            </div>
        `;

        document
            .getElementById("use-detail-session-button")
            .addEventListener("click", () => {
                useSessionInChat(session.session_id);
            });

        document
            .getElementById("clear-detail-session-button")
            .addEventListener("click", () => {
                handleClearSession(
                    session.session_id,
                    true
                );
            });

        document
            .getElementById("delete-detail-session-button")
            .addEventListener("click", () => {
                handleDeleteSession(
                    session.session_id
                );
            });
    }

    catch (error) {
        results.innerHTML = `
            <div class="placeholder-card error-card">
                Unable to load this session.
            </div>
        `;

        console.error(error);
    }
}


function useSessionInChat(sessionId) {
    activeSessionId = sessionId;
    chatMessages = [];

    const chatButton = document.querySelector(
        '[data-view="chat"]'
    );

    if (chatButton) {
        setActiveButton(chatButton);
    }

    renderChatView();
}


async function handleClearSession(
    sessionId,
    reopenDetail = false,
) {
    const confirmed = window.confirm(
        `Clear all messages from session "${sessionId}"?`
    );

    if (!confirmed) {
        return;
    }

    try {
        await clearSessionMessages(sessionId);

        if (sessionId === activeSessionId) {
            chatMessages = [];
        }

        if (reopenDetail) {
            await renderSessionDetail(sessionId);
            return;
        }

        await renderSessionsView();
    }

    catch (error) {
        alert(error.message);
        console.error(error);
    }
}


async function handleDeleteSession(sessionId) {
    const confirmed = window.confirm(
        `Permanently delete session "${sessionId}"?`
    );

    if (!confirmed) {
        return;
    }

    try {
        await deleteSession(sessionId);

        if (sessionId === activeSessionId) {
            activeSessionId = "enterprise-demo";
            chatMessages = [];
        }

        await renderSessionsView();
    }

    catch (error) {
        alert(error.message);
        console.error(error);
    }
}


async function renderLogsView() {
    workspace.innerHTML = `
        <section class="evaluation-view">

            <div class="dashboard-header">

                <div>
                    <h2>Enterprise Logs Dashboard</h2>

                    <p>
                        View saved RAG request logs, latency, token usage,
                        estimated cost, and request status.
                    </p>
                </div>

                <button id="refresh-logs-button">
                    ↻ Refresh
                </button>

            </div>

            <div id="logs-results">
                <div class="placeholder-card">
                    Loading logs...
                </div>
            </div>

        </section>
    `;

    document
        .getElementById("refresh-logs-button")
        .addEventListener(
            "click",
            renderLogsView
        );

    const results = document.getElementById(
        "logs-results"
    );

    try {
        const logs = await getLogs();

        if (!logs.length) {
            results.innerHTML = `
                <div class="placeholder-card">
                    No logs found yet.
                </div>
            `;

            return;
        }

        const totalRequests = logs.length;

        const totalRetrieval = logs.reduce(
            (sum, log) => {
                return sum + Number(
                    log.retrieval_time_ms || 0
                );
            },
            0
        );

        const totalLlm = logs.reduce(
            (sum, log) => {
                return sum + Number(
                    log.llm_time_ms || 0
                );
            },
            0
        );

        const totalTokens = logs.reduce(
            (sum, log) => {
                return sum + Number(
                    log.total_tokens || 0
                );
            },
            0
        );

        const totalCost = logs.reduce(
            (sum, log) => {
                return sum + Number(
                    log.estimated_cost_usd || 0
                );
            },
            0
        );

        const successCount = logs.filter(
            (log) => {
                return log.status === "success";
            }
        ).length;

        const avgRetrieval = Math.round(
            totalRetrieval / totalRequests
        );

        const avgLlm = Math.round(
            totalLlm / totalRequests
        );

        const avgTokens = Math.round(
            totalTokens / totalRequests
        );

        const successRate = Math.round(
            (successCount / totalRequests) * 100
        );

        const rows = logs
            .slice()
            .reverse()
            .map((log, index) => `
                <tr>
                    <td>${index + 1}</td>

                    <td>
                        ${formatDateTime(log.timestamp)}
                    </td>

                    <td class="question-cell">
                        ${escapeHtml(log.question)}
                    </td>

                    <td>
                        ${Math.round(log.retrieval_time_ms)} ms
                    </td>

                    <td>
                        ${Math.round(log.llm_time_ms)} ms
                    </td>

                    <td>${log.total_tokens}</td>

                    <td>
                        $${Number(
                            log.estimated_cost_usd
                        ).toFixed(6)}
                    </td>

                    <td>
                        <span class="status-badge status-success">
                            Success
                        </span>
                    </td>
                </tr>
            `)
            .join("");

        results.innerHTML = `
            <div class="metrics-grid logs-summary-grid">

                <div class="metric-card">
                    <span>Total Requests</span>
                    <strong>${totalRequests}</strong>
                </div>

                <div class="metric-card">
                    <span>Avg Retrieval</span>
                    <strong>${avgRetrieval} ms</strong>
                </div>

                <div class="metric-card">
                    <span>Avg LLM</span>
                    <strong>${avgLlm} ms</strong>
                </div>

                <div class="metric-card">
                    <span>Avg Tokens</span>
                    <strong>${avgTokens}</strong>
                </div>

                <div class="metric-card">
                    <span>Total Tokens</span>
                    <strong>${totalTokens}</strong>
                </div>

                <div class="metric-card">
                    <span>Total Cost</span>
                    <strong>
                        $${totalCost.toFixed(6)}
                    </strong>
                </div>

                <div class="metric-card">
                    <span>Success Rate</span>
                    <strong>${successRate}%</strong>
                </div>

                <div class="metric-card">
                    <span>Latest Request</span>
                    <strong>
                        ${formatTime(
                            logs[logs.length - 1].timestamp
                        )}
                    </strong>
                </div>

            </div>

            <table class="logs-table">

                <thead>
                    <tr>
                        <th>#</th>
                        <th>Time</th>
                        <th>Question</th>
                        <th>Retrieval</th>
                        <th>LLM</th>
                        <th>Tokens</th>
                        <th>Cost</th>
                        <th>Status</th>
                    </tr>
                </thead>

                <tbody>
                    ${rows}
                </tbody>

            </table>
        `;
    }

    catch (error) {
        results.innerHTML = `
            <div class="placeholder-card error-card">
                Unable to load logs.
            </div>
        `;

        console.error(error);
    }
}


function renderPlaceholderView(
    title,
    description,
) {
    workspace.innerHTML = `
        <section class="placeholder-view">

            <h2>${escapeHtml(title)}</h2>

            <p>${escapeHtml(description)}</p>

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
                renderSessionsView();
            }

            if (view === "logs") {
                renderLogsView();
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
    const chatWindow = document.getElementById(
        "chat-window"
    );

    chatMessages.forEach((message) => {
        const messageElement = document.createElement(
            "div"
        );

        messageElement.className =
            `message ${message.cssClass}`;

        messageElement.textContent = message.text;

        chatWindow.appendChild(messageElement);
    });

    chatWindow.scrollTop =
        chatWindow.scrollHeight;
}


function initializeChat() {
    const chatWindow = document.getElementById(
        "chat-window"
    );

    const questionBox = document.getElementById(
        "question"
    );

    const sendButton = document.getElementById(
        "send-button"
    );

    function addMessage(
        text,
        cssClass,
        saveMessage = true,
    ) {
        const message = document.createElement(
            "div"
        );

        message.className =
            `message ${cssClass}`;

        message.textContent = text;

        chatWindow.appendChild(message);

        chatWindow.scrollTop =
            chatWindow.scrollHeight;

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

        addMessage(
            question,
            "user"
        );

        questionBox.value = "";

        const assistantMessage = addMessage(
            "",
            "assistant"
        );

        const assistantIndex =
            chatMessages.length - 1;

        sendButton.disabled = true;
        sendButton.textContent = "Sending...";

        try {
            const reader = await streamQuestion(
                question,
                activeSessionId,
            );

            const decoder = new TextDecoder();

            while (true) {
                const {
                    done,
                    value,
                } = await reader.read();

                if (done) {
                    break;
                }

                const chunk = decoder.decode(
                    value,
                    {
                        stream: true,
                    },
                );

                assistantMessage.textContent += chunk;

                chatMessages[assistantIndex].text =
                    assistantMessage.textContent;

                chatWindow.scrollTop =
                    chatWindow.scrollHeight;
            }
        }

        catch (error) {
            assistantMessage.textContent =
                error.message
                || "Unable to connect to FastAPI.";

            chatMessages[assistantIndex].text =
                assistantMessage.textContent;

            console.error(error);
        }

        finally {
            sendButton.disabled = false;
            sendButton.textContent = "Send";
            questionBox.focus();
        }
    }

    sendButton.addEventListener(
        "click",
        askQuestion
    );

    questionBox.addEventListener(
        "keydown",
        function (event) {
            if (
                event.key === "Enter"
                && !event.shiftKey
            ) {
                event.preventDefault();
                askQuestion();
            }
        }
    );
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

        button.disabled = true;
        button.textContent = "Evaluating...";

        results.innerHTML = `
            <div class="placeholder-card">
                Running evaluation...
            </div>
        `;

        try {
            const data = await evaluateQuestion(
                question,
                activeSessionId
            );

            const metrics = data.metrics;
            const fullAnswer = String(
    data.answer || ""
);

const cleanAnswer = fullAnswer
    .split("\n\nSources:")[0]
    .trim();

            const citationsHtml =
                data.citations && data.citations.length
                    ? `
                        <div class="evaluation-citations">
                            <h3>Sources</h3>
                            <ul>
                                ${data.citations
                                    .map(
                                        citation => `
                                        <li>
                                            <strong>${escapeHtml(citation.source)}</strong>
                                            — Chunk ${citation.chunk}
                                        </li>
                                    `
                                    )
                                    .join("")}
                            </ul>
                        </div>
                    `
                    : "";

            const routingType =
    metrics.routing?.prompt_type === "conversation_memory"
        ? "Conversation Memory"
        : "Document RAG";

            results.innerHTML = `
                <div class="evaluation-answer">

                    <h3>Answer</h3>

                    <p>
                        ${escapeHtml(cleanAnswer)}
                    </p>

                    ${citationsHtml}

                </div>

                <div class="metrics-grid">

                    <div class="metric-card">
                        <span>Retrieval Time</span>
                        <strong>${Number(metrics.retrieval.retrieval_time_ms).toFixed(2)} ms</strong>
                    </div>

                    <div class="metric-card">
                        <span>LLM Time</span>
                        <strong>${Number(metrics.generation.llm_time_ms).toFixed(2)} ms</strong>
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
                        <strong>$${Number(metrics.cost.estimated_cost_usd).toFixed(6)}</strong>
                    </div>

                    <div class="metric-card">
                        <span>Prompt Type</span>
                        <strong>${routingType}</strong>
                    </div>

                </div>
            `;

        } catch (error) {

            results.innerHTML = `
                <div class="placeholder-card error-card">
                    ${escapeHtml(
                        error.message ||
                        "Unable to run evaluation."
                    )}
                </div>
            `;

            console.error(error);

        } finally {

            button.disabled = false;
            button.textContent = "Evaluate";

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
renderChatView();
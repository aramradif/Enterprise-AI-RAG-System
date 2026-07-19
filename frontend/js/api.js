const API_BASE_URL = "http://127.0.0.1:8000";


async function parseErrorResponse(
    response,
    fallbackMessage,
) {
    try {
        const data = await response.json();

        return data.detail || fallbackMessage;
    }

    catch {
        return fallbackMessage;
    }
}


export async function streamQuestion(
    question,
    sessionId = "default",
) {
    const response = await fetch(
        `${API_BASE_URL}/ask/stream`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                question: question,
                session_id: sessionId,
            }),
        }
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Streaming request failed.",
        );

        throw new Error(message);
    }

    if (!response.body) {
        throw new Error(
            "The streaming response did not include a body."
        );
    }

    return response.body.getReader();
}


export async function evaluateQuestion(
    question,
    sessionId = "default",
) {
    const response = await fetch(
        `${API_BASE_URL}/evaluate`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                question: question,
                session_id: sessionId,
            }),
        }
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Evaluation request failed.",
        );

        throw new Error(message);
    }

    return response.json();
}


export async function getLogs() {
    const response = await fetch(
        `${API_BASE_URL}/logs`
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Logs request failed.",
        );

        throw new Error(message);
    }

    return response.json();
}


export async function getSessions() {
    const response = await fetch(
        `${API_BASE_URL}/sessions`
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Unable to load sessions.",
        );

        throw new Error(message);
    }

    return response.json();
}


export async function getSession(
    sessionId,
) {
    const response = await fetch(
        `${API_BASE_URL}/sessions/${encodeURIComponent(sessionId)}`
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Unable to load the selected session.",
        );

        throw new Error(message);
    }

    return response.json();
}


export async function createSession() {
    const response = await fetch(
        `${API_BASE_URL}/sessions`,
        {
            method: "POST",
        }
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Unable to create a session.",
        );

        throw new Error(message);
    }

    return response.json();
}


export async function clearSessionMessages(
    sessionId,
) {
    const response = await fetch(
        `${API_BASE_URL}/sessions/${encodeURIComponent(sessionId)}/messages`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Unable to clear the session messages.",
        );

        throw new Error(message);
    }
}


export async function deleteSession(
    sessionId,
) {
    const response = await fetch(
        `${API_BASE_URL}/sessions/${encodeURIComponent(sessionId)}`,
        {
            method: "DELETE",
        }
    );

    if (!response.ok) {
        const message = await parseErrorResponse(
            response,
            "Unable to delete the session.",
        );

        throw new Error(message);
    }
}
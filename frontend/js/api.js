export async function streamQuestion(question) {
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

    return response.body.getReader();
}


export async function evaluateQuestion(question) {
    const response = await fetch(
        "http://127.0.0.1:8000/evaluate",
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

    if (!response.ok) {
        throw new Error("Evaluation request failed.");
    }

    return response.json();
}
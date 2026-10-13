
const form = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const messages = document.getElementById("messages");
const statusText = document.getElementById("status");
const sendButton = document.getElementById("send-button");

function addMessage(text, sender) {
    const message = document.createElement("div");

    message.className = `message ${sender}`;
    message.textContent = text;

    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) return;

    addMessage(question, "user");

    questionInput.value = "";
    questionInput.focus();

    sendButton.disabled = true;
    statusText.textContent = "Searching your knowledge dataset...";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed.");
        }

        addMessage(data.answer, "bot");

        if (!data.found) {
            statusText.textContent =
                "No sufficiently relevant dataset answer was found.";
        } else {
            statusText.textContent =
                `Matched: ${data.matched_question} | Score: ${data.score}`;
        }

    } catch (error) {
        addMessage(
            "Sorry, something went wrong. Please try again.",
            "bot"
        );

        statusText.textContent = error.message;
    } finally {
        sendButton.disabled = false;
    }
});

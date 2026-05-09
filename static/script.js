const chatbotBtn = document.getElementById("chatbot_btn");
const simulatorBtn = document.getElementById("simulator_btn");
const sendBtn = document.getElementById("send_button");
const answer = document.getElementById("gemini_answer");

if (chatbotBtn) {
    chatbotBtn.addEventListener("click", () => {
        window.location.href = "/chatbot";
    });
}

if (simulatorBtn) {
    simulatorBtn.addEventListener("click", () => {
        window.location.href = "/simulator";
    });
}

if (sendBtn) {
    sendBtn.addEventListener("click", async () => {
        const promptInput = document.getElementById("prompt_input");
        const prompt = promptInput ? promptInput.value.trim() : "";

        if (!prompt) {
            if (answer) {
                answer.innerText = "Please write a prompt first.";
            }
            return;
        }

        if (answer) {
            answer.innerText = "Thinking...";
        }

        try {
            const response = await fetch("/api/chatbot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();

            if (answer) {
                if (data.reply) {
                    answer.innerText = data.reply;
                } else {
                    answer.innerText = data.error || "Something went wrong.";
                }
            }
        } catch (error) {
            if (answer) {
                answer.innerText = "Connection error: " + error.message;
            }
        }
    });
}
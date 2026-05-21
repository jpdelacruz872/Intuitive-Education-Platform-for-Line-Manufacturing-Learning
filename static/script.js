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
            answer.innerHTML = "Conectando con Sentinela...<br><br>";
        }

        try {
            const response = await fetch("/api/chatbot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ prompt: prompt })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = "";
            let outputHTML = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });

                // Procesar líneas completas (separadas por \n\n)
                const lines = buffer.split("\n\n");
                buffer = lines.pop() || "";

                for (const line of lines) {
                    if (line.startsWith("data: ")) {
                        try {
                            const data = JSON.parse(line.slice(6));

                            if (data.error) {
                                outputHTML += `<span style="color: red;"><strong>Error:</strong> ${data.error}</span><br>`;
                            } else if (data.content) {
                                // Mostrar contenido de forma clara
                                outputHTML += `${data.content}<br>`;
                            } else {
                                // Mostrar otros campos disponibles
                                const keys = Object.keys(data).filter(k => k !== 'timestamp' && k !== 'metadata');
                                for (const key of keys) {
                                    if (data[key] && typeof data[key] === 'string') {
                                        outputHTML += `${data[key]}<br>`;
                                    }
                                }
                            }

                            // Actualizar en tiempo real
                            answer.innerHTML = outputHTML;
                            // Auto-scroll al final
                            answer.parentElement.scrollTop = answer.parentElement.scrollHeight;
                        } catch (e) {
                            console.warn("Failed to parse SSE:", e);
                        }
                    }
                }
            }
        } catch (error) {
            if (answer) {
                answer.innerText = "Connection error: " + error.message;
            }
        }
    });
}
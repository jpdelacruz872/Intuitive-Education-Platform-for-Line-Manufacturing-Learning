const chatbot_btn = document.getElementById('chatbot_btn');
const send_btn = document.getElementById('send_button');
const answer = document.getElementById('gemini_answer');
const servidor_btn = document.getElementById('simulator_btn');

chatbot_btn.addEventListener('click', () => {
    window.location.href = '/chatbot';
});

servidor_btn.addEventListener('click', () => {
    window.location.href = '/simulator';
});

send_btn.addEventListener('click', async () => {
    const prompt = document.getElementById('prompt_input').value;

    const response = await fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({prompt: prompt})
    });

    const data = await response.json();

    if (data.reply){
        answer.innerText = data.reply;
    }
    else {
        answer.innerText = data.error;
    }
});

if (answer) {
    answer.innerText = 'Thinking...';
}
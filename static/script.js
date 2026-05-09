function downloadFile(content, filename) {
    const data = new Blob([content], {type: 'text/plain'});
    const url = window.URL.createObjectURL(data);
    const link = document.createElement('a');

    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
}

const chatbot_btn = document.getElementById('chatbot_btn');
const send_btn = document.getElementById('send_button');
const answer = document.getElementById('gemini_answer');
const servidor_btn = document.getElementById('simulator_btn');
const download_py = document.getElementById('download_py');

chatbot_btn.addEventListener('click', () => {
    window.location.href = '/chatbot';
});

servidor_btn.addEventListener('click', () => {
    window.location.href = '/simulator';
});

if (send_btn) {
    send_btn.addEventListener('click', async () => {
        answer.style.display = 'inline-block'
        answer.innerText = 'Thinking...'

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

        if (data.model === 'gemini-2.0-pro') {
            download_py.style.display = 'inline-block'
            download_py.onclick = () => downloadFile(data.reply, "controller.py")
        }
        else {
            download_py.style.display = 'none'
        }
    });
}


if (answer) {
    answer.style.display = 'none';
}
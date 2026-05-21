import json

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

SENTINELA_API = "https://sentinela-909652673285.us-central1.run.app/api/chat"



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


@app.route("/simulator")
def simulator():
    return render_template("server.html")

@app.route("/flowchart")
def flowchart():
    return render_template("diagram.html")

@app.route("/api/chatbot", methods=["POST"])
def chat():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt was provided."}), 400

    def generate():
        try:
            payload = {
                "message": prompt,
                "user_id": "anonymous",
                "user_name": "Usuario UNAM",
                "interaction_mode": "chat",
            }

            response = requests.post(SENTINELA_API, json=payload, timeout=30, stream=True)

            if response.status_code != 200:
                yield f"data: {json.dumps({'error': f'Sentinela error: {response.status_code}'})}\n\n"
                return

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8') if isinstance(line, bytes) else line

                    if line.startswith('data: '):
                        try:
                            event_data = json.loads(line[6:])
                            # Enviar todo tal como viene de Sentinela
                            yield f"data: {json.dumps(event_data)}\n\n"
                        except:
                            pass

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return Response(generate(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no'
    })


if __name__ == "__main__":
    app.run(debug=True)
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai

load_dotenv()

app = Flask(__name__)
CORS(app)

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None


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


@app.route("/api/chatbot", methods=["POST"])
def chat():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt was provided."}), 400

    if client is None:
        return jsonify({"error": "GEMINI_API_KEY is not configured."}), 500

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
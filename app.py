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

@app.route("/flowchart")
def flowchart():
    return render_template("diagram.html")

@app.route("/api/chatbot", methods=["POST"])
def chat():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "No prompt was provided."}), 400

    if client is None:
        return jsonify({"error": "GEMINI_API_KEY is not configured."}), 500

    review_prompt = f"""
Categorize the following user prompt into one of the following two categories:
'CODE' or 'DOUBT'.

If the user wants to chat, solve a doubt, or ask a general-purpose question,
classify it as 'DOUBT'.

If the user wants to control a robot, generate Webots code, or create a robot
controller, classify it as 'CODE'.

Only answer with one word: CODE or DOUBT.

User prompt: {prompt}
"""

    try:
        category_answer = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=review_prompt
        )

        category = category_answer.text.strip().upper()

        if "CODE" in category:
            chosen_model = "gemini-2.0-pro"
            final_prompt = f"""
You are a coding expert in manufacturing lines, automation, and Webots simulator.

Generate a Python Webots controller for the following request:

{prompt}

FOR YOUR ANSWER FORMAT:
- Only provide Python code.
- Do not include Markdown.
- Do not include explanations.
- Do not wrap the code in triple backticks.
- The code should be ready to save as controller.py and use inside Webots.
"""

        else:
            chosen_model = "gemini-2.0-flash"
            final_prompt = f"""
You are a teacher and expert in manufacturing lines, automation, robotics,
and the Webots simulator.

Help a student with the following question:

{prompt}
"""

        response = client.models.generate_content(
            model=chosen_model,
            contents=final_prompt
        )

        return jsonify({
            "reply": response.text,
            "model": chosen_model
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
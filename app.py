import os
from dotenv import load_dotenv
from google import genai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulator')
def simulator():
    return render_template('server.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chatbot', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')

    try:
        response = client.models.generate_content(
            model ='gemini-2.0-flash',
            contents=prompt
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True )
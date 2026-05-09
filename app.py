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
    review_prompt = f"""
Categorize the following user prompt into one of the following two categories: 
'CODE' or 'DOUBT'. If the user wants to chat, solve a doubt or for any general 
porpouse situation, classify it as 'DOUBT', if it wants to control a robot or 
generate code, classify it as 'CODE'. Also, DO NOT MENTION IN YOUR ANY PART OF 
YOUR ANSWER THE WORD 'DOUBT' OR 'CODE' IF YOU DO NOT CLASSIFY IT AS THAT, BECAUSE 
IT CAN CONFUSE ME. 

User prompt: {prompt}
"""
    category_answer = client.models.generate_content(
        model = 'gemini-2.0-flash',
        contents=review_prompt
    )

    category = category_answer.text.strip().upper()

    if 'CODE' in category:
        choosen_model = 'gemini-2.0-pro'
        final_prompt = f"""You are a coding expert in manufacturing lines
        and automation. Also, you are expert in webots simulator. Please
        help me with the following:
        
        {prompt}
FOR YOUR ANSWER FORMAT, ONLY PROVIDE THE PYTHON CODE OF THE WEBOTS CONTROLLER
IN TXT FORMAT, FOLLOWING PYTHON SINTAXES AND STRUCTURE, SO THAT I CAN CHANGE
THE EXTENTION FROM .TXT TO .PY, PUT IT INTO TE APPROPIATE FOLDER, AND WEBOTS
WILL BE ABLE TO USE IT TO CONTROL THE ROBOT"""

    elif 'DOUBT' in category:
        choosen_model = 'gemini-2.0-flash'
        final_prompt = f"""You are a teacher, expert in manufacturing lines
        and automation. Also, you are expert in webots simulator. Please help
        a student with the following question:

        {prompt}"""

    try:
        response = client.models.generate_content(
            model = choosen_model,
            contents=final_prompt
        )
        return jsonify({'reply': response.text,
                        'model': choosen_model})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True )
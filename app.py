from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

# Load knowledge base
def load_knowledge_base(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
    except FileNotFoundError:
        data = {"questions": []}  # Create an empty knowledge base if the file does not exist
    return data

knowledge_base = load_knowledge_base('knowledge_base.json')

def find_best_match(user_question: str, questions: list) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q['question'] == question:
            return q['answer']
    return None  # Return None if question not found

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('user_input', '')
    
    if user_input.lower() == 'quit':
        response = {'bot_response': 'Goodbye!'}
    else:
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        
        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            response = {'bot_response': answer}
        else:
            response = {'bot_response': 'sorry, i don\'t know'}
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

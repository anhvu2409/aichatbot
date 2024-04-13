from flask import Flask, render_template, request
import json
from difflib import SequenceMatcher

app = Flask(__name__)

def load_knowledge_base(file_path):
    # Tải cơ sở tri thức từ file json
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Không thể tải dữ liệu: {str(e)}")
        return None

def find_closest_match(input_question, knowledge_base):
    # Tìm câu hỏi gần nhất trong cơ sở tri thức so với câu hỏi đầu vào
    max_ratio = 0
    closest_question = None
    for question in knowledge_base.keys():
        ratio = SequenceMatcher(None, input_question, question).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
            closest_question = question
    return closest_question if max_ratio > 0.6 else None

def get_response(question, knowledge_base):
    # Lấy câu trả lời cho câu hỏi từ cơ sở tri thức
    closest_question = find_closest_match(question, knowledge_base)
    if closest_question:
        return knowledge_base[closest_question]
    else:
        return None

def update_knowledge_base(question, answer, knowledge_base):
    # Cập nhật cơ sở tri thức với câu hỏi và câu trả lời mới
    knowledge_base[question] = answer
    with open('knowledge_base.json', 'w', encoding='utf-8') as file:
        json.dump(knowledge_base, file, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    knowledge_base = load_knowledge_base('knowledge_base.json')
    response = get_response(user_input, knowledge_base)
    if response:
        return response
    else:
        return "Tôi không hiểu, Bạn có thể dạy cho tôi không?"

if __name__ == '__main__':
    app.run(debug=True)


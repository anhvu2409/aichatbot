import json
from difflib import SequenceMatcher

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

def start_chat(knowledge_base):
    # Bắt đầu cuộc trò chuyện với bot
    while True:
        user_input = input('Bạn: ')
        if user_input.lower() == 'quit':
            break
        response = get_response(user_input, knowledge_base)
        if response:
            print(f'Chatbot: {response}')
        else:
            print('Chatbot: Tôi không hiểu, Bạn có thể dạy cho tôi không?')
            new_answer = input('Nhập câu trả lời hoặc ghi "skip" để bỏ qua: ')
            if new_answer.lower() != 'skip':
                update_knowledge_base(user_input, new_answer, knowledge_base)
                print('Chatbot: Cảm ơn, Tôi đã biết cách trả lời câu hỏi này.')

if __name__ == '__main__':
    knowledge_base = load_knowledge_base('knowledge_base.json')  # Tải cơ sở tri thức từ file 'knowledge_base.json'
    start_chat(knowledge_base)  # Bắt đầu cuộc trò chuyện với bot


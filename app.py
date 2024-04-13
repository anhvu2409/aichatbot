# Import các module cần thiết từ Flask
from flask import Flask, render_template, request, jsonify

# Import các hàm từ module 'main'
from main import load_knowledge_base, find_closest_match, get_response

# Định nghĩa lớp ChatBotApp
class ChatBotApp:
    # Phương thức khởi tạo
    def __init__(self, knowledge_base_file):
        # Khởi tạo ứng dụng Flask
        self.app = Flask(__name__)
        # Tải cơ sở tri thức từ file JSON
        self.knowledge_base = load_knowledge_base(knowledge_base_file)
        # Thiết lập các route cho ứng dụng
        self.setup_routes()

    # Phương thức thiết lập các route
    def setup_routes(self):
        # Route cho trang chủ
        @self.app.route("/")
        def home():
            return render_template("index.html")

        # Route để xử lý các câu hỏi từ người dùng
        @self.app.route("/ask", methods=["POST"])
        def ask():
            if request.method == "POST":
                data = request.get_json()
                user_input = data["question"]
                if self.knowledge_base is None:
                    return jsonify({"answer": "Tôi không thể trả lời câu hỏi này"})
                best_match = find_closest_match(user_input, self.knowledge_base.keys())
                if best_match:
                    answer = get_response(best_match, self.knowledge_base)
                    return jsonify({"answer": f"{answer}"})
                else:
                    return jsonify({"answer": "Xin lỗi, Bạn có thể hỏi tôi câu khác được không?"})

    # Phương thức chạy ứng dụng
    def run(self, debug=False):
        self.app.run(debug=debug)

# Điểm bắt đầu của chương trình
if __name__ == "__main__":
    # Khởi tạo một đối tượng ChatBotApp và chạy ứng dụng
    bot_app = ChatBotApp('knowledge_base.json')
    bot_app.run(debug=True)

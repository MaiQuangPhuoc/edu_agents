from flask import Flask, request, jsonify
from flask_cors import CORS
import docx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..","..")))
from pydantic_settings import BaseSettings
from src.clients.llm import LLMClient
from langchain_core.messages import HumanMessage

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.state import AgentProfile , State 
from src.agents.profile_collector import ProfileCollector
from langchain_core.runnables import RunnableConfig

app = Flask(__name__)
CORS(app)  # Cho phép truy cập từ frontend

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

llm_client=LLMClient(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_provider="groq"
)

agent = ProfileCollector(llm_client)
profile_agent = agent(State)

@app.route("/chat", methods=["POST"])
def chat():
        
        # print('===== bắt dau =======')
        data = request.get_json()
        user_message = data.get("message", "")


        while True:
            print(f"đã nhận--: {user_message}")
            response = profile_agent.invoke(
                {"messages": user_message},
                config=RunnableConfig(configurable={"thread_id": "test_thread"})
            )

            ai_reply = response["messages"][-1].content if isinstance(response, dict) else response
            print(f"Hệ thống: {ai_reply}")
            
         
            if user_message.strip().lower() in ["exit", "quit", "q"]:
                break  
            return jsonify({"reply": ai_reply})

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "Không tìm thấy file trong yêu cầu", 400

    file = request.files["file"]

    if file.filename == "":
        return "Tên file trống", 400

    if file and file.filename.lower().endswith((".doc", ".docx")):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Đọc nội dung file Word (chỉ hỗ trợ .docx)
        if file.filename.lower().endswith(".docx"):
            doc = docx.Document(file_path)
            content = "\n".join([p.text for p in doc.paragraphs])
        else:
            content = "(Không hỗ trợ đọc nội dung file .doc, chỉ .docx)"

        # lấy ra tên file ( chưa lấy đc link ) và nội dung 
        # dùng mánh khóe : link local +_ tên file , vidu 
        # file_name = 'EDUAGENT/abc...' + file.filename
        print(f"Đã nhận file {file.filename}")
        print("Nội dung:")
        print(content[:1000])  # in thử 1000 ký tự đầu

        return f"Server đã nhận file {file.filename}.\nNội dung:\n{content[:500]}"
    else:
        return " Không hỗ trợ loại file này", 400


if __name__ == "__main__":
    app.run(port=8000)
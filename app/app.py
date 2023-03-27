import openai
from flask import Flask, jsonify, render_template, request

from .config import OPENAI_API_KEY

# OpenAI APIの初期化
openai.api_key = OPENAI_API_KEY


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# GPT-3 APIを使用してテキストを生成する関数
def generate_text(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=120,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message


# チャットボットの実装
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data["text"]
    message = generate_text(prompt)
    return jsonify({"text": message})

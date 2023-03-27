import openai
from flask import Flask, jsonify, render_template, request

from .config import API_KEY

# OpenAI APIの初期化
openai.api_key = API_KEY


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


def generate_chat_text(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            # {"role": "user", "content": "Who won the world series in 2020?"},
            # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": prompt}
        ]
    )
    message = response['choices'][0]['message']['content']
    return message


# チャットボットの実装
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data["text"]
    message = generate_chat_text(prompt)
    return jsonify({"text": message})

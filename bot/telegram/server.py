from flask import Flask, request
import requests
from API import Plataform
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from fake_news_models.BertModelFakeNews import BertModelFakeNews

app = Flask(__name__)
API = Plataform()
model = BertModelFakeNews()

@app.route("/webhook", methods=['POST'])
def webhook():
    update = request.get_json()
    if 'message' in update:
        id = update['message']['chat']['id']
        text = update['message']['text']
        if text.startswith("/prever"):
            news = text.replace("/prever", "").strip()
            if news:
                result = model.predict(news)
                probs = model.predict_proba(news)
                response = f"A notícia parece ser {result} com {(probs[result]*100):.2f}% de probalidade."
            else:
                response = "Por favor, envie a notícia após o comando /prever."
            notify(id, response)
    return "OK", 200

def notify(chat_id, text:str):
     data = {"chat_id": chat_id, "text": text}
     requests.post(API.get_URL() + "sendMessage", json=data)               

if __name__ == '__main__':
    app.run(port=5000)
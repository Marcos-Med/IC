from flask import Flask, request
from handlers import *

app = Flask(__name__) ## Instancia um server

handlers = { #Comandos executados pelo BOT
    "/start": StartHandler(),
    "/prever": PredictHandler(),
    "/help": HelpHendler()
}

@app.route("/webhook", methods=['POST']) #endpoint de comunicação
def webhook():
    update = request.get_json()
    if 'message' in update:
        if 'text' in update['message'] and update['message']['text'].startswith("/"):
            id = update['message']['chat']['id']
            text = update['message']['text']
            list = text.split()
            if len(list) == 1: 
                handlers[list[0]].response(id)
            else:
                handlers[list[0]].response(id, " ".join(list[1:]))
    return "OK", 200
       
if __name__ == '__main__':
    app.run(port=5000)
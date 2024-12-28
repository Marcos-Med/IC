import sys
import os
import requests
from API import Plataform
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))) 
from fake_news_models.LogisticModelFakeNews import LRModelFakeNews

class SendMessage():
    def __init__(self):
        self.__API = Plataform()
    def notify(self, response:str, chat_id): #Notificação com texto puro
        data = {
            "chat_id": chat_id,
            "text": response
        }
        return requests.post(self.__API.get_URL() + "sendMessage", json=data)
    
class SendPhoto():
    def __init__(self):
        self.__API = Plataform()
    def notify(self, response:str, chat_id, photo_url): #Notificação com imagem
        data = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": response
        }
        return requests.post(self.__API.get_URL() + "sendPhoto", json=data)

class StartHandler(): #Executa comando /start
    def __init__(self):
        self.__sender = SendPhoto()

    def response(self, chat_id):
        response = f"Olá, eu sou o FakeBot! 🤖📰\nMinha missão é ajudar você a identificar se uma notícia é verdadeira ou falsa, promovendo mais confiança nas informações que circulam por aí. 🌐🔍\nUse o comando \\help para descobrir tudo o que posso fazer.\nVamos combater juntos a desinformação! 💡✅"
        return self.__sender.notify(response, chat_id, "https://i.postimg.cc/VkM9MQhG/Designer.jpg")

    
class PredictHandler(): # Realiza a predição com o modelo LogisticRegression
    def __init__(self):
        self.__model = LRModelFakeNews()
        self.__sender = SendMessage()

    def response(self, chat_id, text:str):
        if text:
            result = self.__model.predict(text)
            probs = self.__model.predict_proba(text)
            response = f"A notícia parece ser {result} com {(probs[result]*100):.2f}% de probalidade."
        else:
            response = "Por favor, envie a notícia após o comando /prever."
        return self.__sender.notify(response, chat_id)
    
class HelpHendler(): # Executa o comando /help
    def __init__(self):
        self.__commands = { # Lista as funcionalidades do BOT
            "/start": "Exibe a mensagem inicial do bot com informações sobre sua missão.",
            "/prever [notícia]": "Analisa a notícia enviada e retorna se é verdadeira ou falsa. Exemplo: /prever O governo anunciou uma nova política de impostos.",
            "/help": "Lista todos os comandos disponíveis e como usá-los." 
        }
        self.__sender = SendMessage()

    def response(self, chat_id):
        response = "🛠️ Comandos disponíveis no FakeBot:\n\n"
        for command, description in self.__commands.items():
            response += f"{command}\n{description}\n\n"
        response += "💡 Observação:\nCertifique-se de enviar notícias claras para obter os melhores resultados. 🚀"
        return self.__sender.notify(response, chat_id)
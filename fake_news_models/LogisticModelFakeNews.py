import joblib
import torch
from fake_news_models.Model import Model
from transformers import AutoModel, AutoTokenizer

class LRModelFakeNews(Model): #Classe que representa o Preditor de Notícias Falsas com Regressão Logística
    def __init__(self):
        #Carrega o modelo Pré Treinado BERTimbau
        self.__model = AutoModel.from_pretrained("neuralmind/bert-base-portuguese-cased", num_labels=2)
        self.__model.eval() #Modo avaliação
        self.__tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
        #Carrega a camada treinado de Regressão Logística
        self.__layerLogisticRegression = joblib.load("logistic_model.joblib")
    
    def _getEmbeddings(self, sentence: str):
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("A entrada deve ser uma string não vazia.")
        # Método que devolve os embeddings do Modelo BERTimbau
        inputs = self.__tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.__model(**inputs)
        return outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    
    def predict(self, sentence: str) -> str:
        #Realiza a predição da Notícia
        embedding = self._getEmbeddings(sentence)
        return "FAKE" if self.__layerLogisticRegression.predict([embedding])[0] == 0 else "REAL"
    
    def predict_proba(self, sentence) -> dict:
        #Devolve a probabilidade de cada classe de notícia
        embedding = self._getEmbeddings(sentence)
        probs = self.__layerLogisticRegression.predict_proba([embedding])
        return {
            "FAKE": probs[0][0],
            "REAL": probs[0][1]
        }   
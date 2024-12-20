from abc import ABC, abstractmethod

class Model(ABC): #Classe abstrata para Modelo de Predição

    @abstractmethod
    #Devolve os Embeddings
    def _getEmbeddings(self, sentence: str):
        pass

    @abstractmethod
    #Realiza a predição
    def predict(self, sentence: str) -> str:
        pass

    @abstractmethod
    #Devolve a probabilidade para cada classe de Notícia
    def predict_proba(self, sentence: str) -> dict:
        pass
from fake_news_models.Model import Model
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class BertModelFakeNews(Model):
    def __init__(self):
        #Carrega o modelo com Fine Tuning
        self.__model = AutoModelForSequenceClassification.from_pretrained("../model_BERTimbau", num_labels=2)
        self.__model.eval() #Modo avaliação
        self.__tokenizer = AutoTokenizer.from_pretrained("../tokenizer_BERTimbau")

    def _getEmbeddings(self, sentence:str):
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError("A entrada deve ser uma string não vazia.")
        #Devolve a saída do Modelo Fine Tuning BERTimbau
        inputs = self.__tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.__model(**inputs)
        return outputs.logits

    def predict(self, sentence:str)->str:
        #Realiza a predição
        outputs = self._getEmbeddings(sentence)
        probs = torch.nn.functional.softmax(outputs, dim=-1)
        predicts = torch.argmax(probs, dim=-1)
        return "FAKE" if predicts[0] == 0 else "REAL"
        

    def predict_proba(self, sentence:str) -> dict:
        #Devolve as probabilidades
        outputs = self._getEmbeddings(sentence)
        probs = torch.nn.functional.softmax(outputs, dim=-1)
        return {
            "FAKE": probs[0][0].item(),
            "REAL": probs[0][1].item()
        }
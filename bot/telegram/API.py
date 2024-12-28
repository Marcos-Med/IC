class Plataform(): #Guarda token para o telegram
    def __init__(self):
        self.__token = "8096356826:AAH9Oj2YMYz6f-f-EHrIGe1A3V0e9h-3V2A"
    def get_token(self) -> str:
        return self.__token
    def get_URL(self) -> str:
        return f"https://api.telegram.org/bot{self.get_token()}/"
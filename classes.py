class Cliente:
    def __init__(self,username,socket):
        self.username = username
        self.socket = socket
        self.arquivos = []



class Arquivo:
    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        self.localizacao = []


class Servidor:
    def __init__(self,id,socket):
        self.id = id
        self.socket = socket
        self.arquivos = []
        
    def __repr__(self):
        return f'Servidor {self.id}'
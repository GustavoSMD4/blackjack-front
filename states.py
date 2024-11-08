import requests
import flet as ft

class States:
    def __init__(self, page):
        self.__transferencia = None
        self.__usuarioLogado = None
        self.page: ft.Page = page

    @classmethod
    def newStates(cls, page):
        states = cls(page)
        states.__transferencia = {}
        return states
    
    def login(self, usuario, senha):
        response = requests.post("https://gustavosmd4blackjack.pythonanywhere.com/usuario/login", json=dict(usuario=usuario, senha=senha))
        
        if response.status_code != 200:
            self.page.open(ft.SnackBar(ft.Text(response.json().get("error"))))
            return
        
        self.__usuarioLogado = response.json().get("body")
        
    def criarConta(self, usuario, senha, nome):
        response = requests.post("https://gustavosmd4blackjack.pythonanywhere.com/usuario/create", json=dict(usuario=usuario, senha=senha, nome=nome))
        
        if response.status_code != 200:
            self.page.open(ft.SnackBar(ft.Text(response.json().get("error"))))
            return
        
        self.login(usuario, senha)
        
    def updateSaldo(self, saldo: float):
        response = requests.post("https://gustavosmd4blackjack.pythonanywhere.com/usuario/addsaldo", json=dict(usuario=self.__usuarioLogado["usuario"], saldo=saldo))
        
        if response.status_code != 200:
            self.page.open(ft.SnackBar(ft.Text(response.json().get("error"))))
            return
        
        self.__usuarioLogado = response.json().get("body")
    
    def getUsuarioLogado(self):
        return self.__usuarioLogado
    
    def getTransferencia(self):
        return self.__transferencia
    
    def setTransferencia(self, key, value):
        """Método para adicionar ou atualizar uma entrada no dicionário de transferências."""
        if self.__transferencia is None:
            self.__transferencia = {}
        self.__transferencia[key] = value
    
    def getTransferenciaByKey(self, key):
        """Método para obter uma entrada específica do dicionário de transferências por chave."""
        return self.__transferencia.get(key, None)
    
    def removeTransferencia(self, key):
        """Método para remover uma entrada do dicionário de transferências."""
        if key in self.__transferencia:
            del self.__transferencia[key]

    def clearTransferencia(self):
        """Método para limpar todas as entradas no dicionário de transferências."""
        self.__transferencia.clear()


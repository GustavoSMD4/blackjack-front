class States:
    def __init__(self):
        self.__transferencia = None

    @classmethod
    def newStates(cls):
        states = cls()
        states.__transferencia = {}
        return states
    
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


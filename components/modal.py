import flet as ft

class Modal:
    def __init__(self, page: ft.Page, parametros) -> None:
        self.page = page
        self.__modal: ft.AlertDialog | None = None
        self.__parametros = parametros
    
    @classmethod
    def newModal(cls, page: ft.Page, parametros = None):
        modal = cls(page, parametros)
        modal.__buildModal()
        return modal
    
    def getModal(self):
        return self.__modal
    
    def setTitle(self, title: str | ft.Control):
        if isinstance(title, str):
            self.__modal.title = ft.Text(title)
            return
        self.__modal.title = title
        return
        
    def setContent(self, content: str | ft.Control):
        if isinstance(content, str):
            self.__modal.content = ft.Text(content)
            return
        
        self.__modal.content = content
        return
        
    def setOnDismiss(self, text: str):
        self.__modal.on_dismiss = lambda _: ft.Text(text)
        return
        
    def setActionAoConfirmar(self, funcao):
        for button in self.__modal.actions:
            if button.key == "confirmar":
                if self.__parametros is not None:
                    button.on_click = lambda _: self.__handleConfirmar(funcao, self.__parametros)
                else:
                    button.on_click = lambda _: self.__handleConfirmar(funcao)
                return
            
    def setActionAoCancelar(self, funcao):
        for button in self.__modal.actions:
            if button.key == "cancelar":
                if self.__parametros is not None:
                    button.on_click = lambda _: self.__handleConfirmar(funcao, self.__parametros)
                else:
                    button.on_click = lambda _: self.__handleConfirmar(funcao)
                return
            
    def removeActionButtons(self):
        self.__modal.actions = None
                
    def __buildModal(self):
        self.__modal = ft.AlertDialog()
        self.__modal.title = ft.Text("Por favor, confirme.")
        self.__modal.content = ft.Text("Realmente quer confirmar essa ação?")
        self.__modal.actions_alignment = ft.MainAxisAlignment.END
        self.__modal.on_dismiss = lambda _: ft.Text("Ok")
        self.__modal.actions = [
            ft.TextButton("Cancelar", key="cancelar", on_click=lambda _: self.page.close(self.__modal)),
            ft.TextButton("Confirmar", key="confirmar", on_click=lambda _: self.page.close(self.__modal)),
        ]
        
        return
        
    def __handleConfirmar(self, funcao, *args):
        funcao(*args)
        self.page.close(self.__modal)
        return
    
    
        
        
        
        

import flet as ft

from states import States

class NumeroJogadoresView(ft.View):
    def __init__(self, page: ft.Page, states: States):
        super().__init__()
        
        self.route = "/"
        self.scroll = "auto"
        self.page = page
        self.states = states
        self.__jogadores: list[str] = []

        self.__build()
    
    
    def __build(self):
        
        def addJogador(e):
            self.__jogadores.append(nome.value)
            self.states.setTransferencia("jogadores", self.__jogadores)
            self.page.go("/blackjack")
        
        nome = ft.TextField(label="Nome do jogador")
        
        self.controls=[
            nome,
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Continuar",
                        icon=ft.icons.SAVE,
                        on_click=addJogador
                    ),
                    
                    # ft.ElevatedButton(
                    #     text="jogar",
                    #     icon=ft.icons.SAVE,
                    #     on_click=self.__handleClickContinuar
                    # ),
                    
                ]
            ),
            
        ]
        
    # def __handleClickContinuar(self, e):
    #     self.states.setTransferencia("jogadores", self.__jogadores)
    #     self.page.go("/blackjack")
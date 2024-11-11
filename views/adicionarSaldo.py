import flet as ft

from states import States

class AdicionarSaldoView(ft.View):
    def __init__(self, page: ft.Page, states: States):
        super().__init__()
        
        self.route = "/addsaldo"
        self.scroll = "auto"
        self.page = page
        self.states = states
        
        self.saldoField = ft.TextField(label="Valor adicionar")
        
        self.botaoConfirmar = ft.ElevatedButton(
            text="Confirmar",
            icon=ft.icons.ADD,
            bgcolor="blue",
            on_click=lambda _: self.__handleConfirmar()
        )
        
        self.botaoCancelar = ft.ElevatedButton(
            text="Cancelar",
            icon=ft.icons.CANCEL,
            on_click=lambda _: self.page.go("/blackjack")
        )
        
        self.__build()
        
    def __handleConfirmar(self):
        self.states.updateSaldo(float(self.saldoField.value))
        self.page.go("/blackjack")
        
    def __build(self): 
        body = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value=f"Adicionar saldo para {self.states.getUsuarioLogado()['usuario']}", size=20, weight="bold"),
                    self.saldoField,
                    
                    ft.Row(
                        controls=[
                            self.botaoCancelar,
                            self.botaoConfirmar,
                        ]
                    )
                    
                ]
            )
        )
        
        self.controls = [
            body
        ]
        
    
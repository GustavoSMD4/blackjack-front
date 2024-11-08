import flet as ft

from states import States

class CriarContaView(ft.View):
    def __init__(self, page: ft.Page, states: States):
        super().__init__()
        
        self.route = "/criarconta"
        self.scroll = "auto"
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page = page
        self.states = states
        
        self.nomeField = ft.TextField(label="Nome", width=300, max_length=100)
        self.usuarioField = ft.TextField(label="Usuário", width=300, max_length=30)
        self.senhaField = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True, max_length=100)
        self.botaoLogin = ft.ElevatedButton(
            text="Confirmar",
            icon=ft.icons.CREATE,
            bgcolor="blue",
            width=150,
            on_click=lambda _: self.__handleConfirmar()
        )
        
        self.botaoCancelar = ft.ElevatedButton(
            text="Cancelar",
            icon=ft.icons.CANCEL,
            width=150,
            on_click=lambda _: self.page.go("/")
        )
        
        self.__build()
        
    def __handleConfirmar(self):
        self.states.criarConta(self.usuarioField.value.strip(), self.senhaField.value.strip(), self.nomeField.value.strip())
        
        if self.states.getUsuarioLogado():
            self.page.go("/blackjack")
    
    def __build(self):
        
        body = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Criar conta", size=20, weight="bold"),
                    self.nomeField,
                    self.usuarioField,
                    self.senhaField,
                    ft.Row(
                        controls=[
                            self.botaoCancelar,
                            self.botaoLogin
                        ]
                    )
                ]
            )
        )
        
        self.controls = [
            body
        ]
    
    
    
    
import flet as ft

from states import States

class LoginView(ft.View):
    def __init__(self, page: ft.Page, states: States):
        super().__init__()
        
        self.route = "/"
        self.scroll = "auto"
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page = page
        self.states = states
        
        self.usuarioField = ft.TextField(label="Usuário", width=300)
        self.senhaField = ft.TextField(label="Senha", width=300, password=True, can_reveal_password=True)
        self.botaoLogin = ft.ElevatedButton(
            text="Login",
            icon=ft.icons.LOGIN,
            bgcolor="blue",
            width=300,
            on_click=lambda _: self.__handleLogin()
        )
        
        self.botaoCriarConta = ft.ElevatedButton(
            text="Criar conta",
            icon=ft.icons.CREATE,
            bgcolor="blue",
            width=300,
            on_click=lambda _: self.page.go("/criarconta")
        )
        
        self.__build()
        
    def __handleLogin(self):
        self.states.login(self.usuarioField.value.strip(), self.senhaField.value.strip())
        self.page.go("/blackjack")
        
    def __build(self):
        body = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Login", size=20, weight="bold", text_align=ft.TextAlign.CENTER),
                    self.usuarioField,
                    self.senhaField,
                    self.botaoLogin,
                    self.botaoCriarConta
                ]
            )
        )
        
        self.controls = [
            body
        ]




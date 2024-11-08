import flet as ft

from states import States
from views.criarConta import CriarContaView
from views.jogoView import JogoView
from views.loginView import LoginView

def main(page: ft.Page):
    page.title = "Blackjack"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#FFFAFA"
    page.scroll="auto"
    
    states = States.newStates(page)
    
    def onRouteChange(e: ft.RouteChangeEvent):
        page.views.clear()
        
        if page.route == "/":
            states.__usuarioLogado = None
            page.views.append(LoginView(page, states))
        
        if states.getUsuarioLogado() == None and page.route != "/criarconta":
            page.go("/")
            
        if page.route == "/criarconta":
            page.views.append(CriarContaView(page, states))
        
        if page.route == "/blackjack":
            page.views.append(JogoView(page, states))
        
        page.update()
        
    page.on_route_change = onRouteChange
    page.go(page.route)

ft.app(target=main)
import flet as ft

from states import States
from views.jogoView import JogoView
from views.numerosJogadores import NumeroJogadoresView

def main(page: ft.Page):
    page.title = "Blackjack"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#FFFAFA"
    page.scroll="auto"
    
    states = States.newStates()
    
    def onRouteChange(e: ft.RouteChangeEvent):
        page.views.clear()
        
        if page.route == "/blackjack":
            page.views.append(JogoView(page, states))
            
        if page.route == "/":
            page.views.append(NumeroJogadoresView(page, states))
        
        page.update()
        
    page.on_route_change = onRouteChange
    page.go(page.route)
    
if __name__ == "__main__":
    ft.app(target=main)
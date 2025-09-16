import flet as ft

from classes.blackjack import Blackjack
from classes.carta import Carta
from classes.jogador import Jogador
from states import States

class JogoViewControls:
    def __init__(self, page: ft.Page, states: States, jogador: Jogador, blackjack: Blackjack):
        self.page = page
        self.states = states
        self.blackjack = blackjack
        self.__jogador = jogador
        self.__columnCartasJogador = None
        self.__columnCartasDealer = None
        self.textoNomeJogador = None
        self.textoNomeDealer = None

    def controls(self):
        """Constrói a interface do jogo com as cartas e botões atualizados."""
        self.__buildContainerCartasDealer()
        self.__buildContainerCartasJogador()
        
        containerDealer = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.__columnCartasDealer]
        )
        
        containerJogador = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[self.__columnCartasJogador]
        )

        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    containerDealer,
                    ft.Divider(thickness=10, color="black"),
                    containerJogador
                ]
            )
        )

    def __buildContainerCartasJogador(self):
        """Constrói o container de cartas do jogador."""
        self.textoNomeJogador = ft.Text(
            f"{self.__jogador.getNomeJogador()} - tem {self.__jogador.getValorMao()}",
            weight="bold",
            size=20,
            text_align=ft.TextAlign.CENTER
        )
        
        self.__columnCartasJogador = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.textoNomeJogador,
                ft.Text(
                    value=f"Valor da aposta: {self.__jogador.getValorAposta()}",
                    weight="bold",
                    size=16,
                    text_align=ft.TextAlign.CENTER
                ),
                self.__getImagensCartas(self.__jogador.getCards())
            ]
        )

    def __buildContainerCartasDealer(self):
        """Constrói o container de cartas do dealer."""
        self.textoNomeDealer = ft.Text(
            f"{self.blackjack.dealer.getNomeJogador()} - tem {self.blackjack.dealer.getValorMao()}",
            weight="bold",
            size=20,
            text_align=ft.TextAlign.CENTER
        )
        
        self.__columnCartasDealer = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.textoNomeDealer,
                self.__getImagensCartas(self.blackjack.dealer.getCards())
            ]
        )

    def __getImagensCartas(self, cartas: list[Carta]):
        """Gera a lista de imagens das cartas, com 3 cartas por linha."""
        column = ft.Column(scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        rowCartas = ft.Row(scroll="auto", alignment=ft.MainAxisAlignment.CENTER)

        contador = 0

        for carta in cartas:
            rowCartas.controls.append(
                ft.Image(f"{carta.getNomeImagem()}", width=130, height=200, fit=ft.ImageFit.FIT_HEIGHT)
            )
            contador += 1

            if contador == 3:
                column.controls.append(rowCartas)
                rowCartas = ft.Row(scroll="auto", alignment=ft.MainAxisAlignment.CENTER)
                contador = 0

        if contador > 0:
            column.controls.append(rowCartas)

        return column

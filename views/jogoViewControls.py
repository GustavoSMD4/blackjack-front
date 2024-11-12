import os
import sys
import time
import flet as ft

from classes.blackjack import Blackjack
from classes.carta import Carta
from classes.jogador import Jogador
from components.modal import Modal
from states import States

class JogoViewControls:
    def __init__(self, page: ft.Page, states: States, jogador: Jogador, blackjack: Blackjack):
        self.page = page
        self.states = states
        self.blackjack = blackjack
        self.__jogador = jogador
        self.__columnCartasJogador = None
        self.nomeJogador = None
        self.__columnCartasDealer = None
        
    def controls(self):
        """Constrói a interface do jogo com as cartas e botões atualizados."""
        self.__buildContainerCartasDealer()
        self.__buildContainerCartasJogador()
        
        containerDealer = ft.Column(
            controls=[self.__columnCartasDealer]
        )
        
        containerJogador = ft.Column(
            controls=[self.__columnCartasJogador]
        )

        return ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    containerDealer,
                    ft.Divider(thickness=10, color="black"),
                    containerJogador
                ]
            )
        )

    def __buildContainerCartasJogador(self):
        """Constrói o container de cartas do jogador."""
        self.nomeJogador = ft.Text(f"{self.__jogador.getNomeJogador()} - tem {self.__jogador.getValorMao()}", weight="bold", size=20, text_align=ft.TextAlign.CENTER)
        
        self.__columnCartasJogador = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.nomeJogador,
                ft.Text(value=f"Valor da aposta: {self.__jogador.getValorAposta()}", weight="bold", size=16),
                self.__getImagensCartas(self.__jogador.getCards())
            ]
        )

    def __buildContainerCartasDealer(self):
        """Constrói o container de cartas do dealer."""
        self.nomeJogador = ft.Text(f"{self.blackjack.dealer.getNomeJogador()} - tem {self.blackjack.dealer.getValorMao()}", weight="bold", size=20, text_align=ft.TextAlign.CENTER)
        
        self.__columnCartasDealer = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.nomeJogador,
                self.__getImagensCartas(self.blackjack.dealer.getCards())
            ]
        )

    def __getImagensCartas(self, cartas: list[Carta]):
        """Gera a lista de imagens das cartas, com 3 cartas por linha."""
        column = ft.Column(scroll="auto")
        rowCartas = ft.Row(scroll="auto")
    
        # Contador para adicionar uma nova linha a cada 3 cartas
        contador = 0
    
        for carta in cartas:
            # Adiciona a carta à linha atual
            rowCartas.controls.append(
                ft.Image(f"{carta.getNomeImagem()}", width=130, height=200, fit=ft.ImageFit.FIT_HEIGHT)
            )
            contador += 1
        
            # Quando 3 cartas são adicionadas à linha, adiciona a linha à coluna e cria uma nova linha
            if contador == 3:
                column.controls.append(rowCartas)
                rowCartas = ft.Row(scroll="auto")  # Cria uma nova linha para as próximas cartas
                contador = 0  # Reseta o contador
    
        # Adiciona a última linha (caso não tenha completado 3 cartas na última linha)
        if contador > 0:
            column.controls.append(rowCartas)
    
        return column
    
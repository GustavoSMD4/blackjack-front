import os
import sys
import time
import flet as ft

from classes.baralho import Baralho
from classes.blackjack import Blackjack
from classes.carta import Carta
from components.modal import Modal
from states import States

class JogoView(ft.View):
    def __init__(self, page: ft.Page, states: States):
        super().__init__()
        
        self.route = "/blackjack"
        self.scroll = "auto"
        self.page = page
        self.states = states
        self.blackjack = Blackjack(self.states.getTransferenciaByKey("jogadores"), 4)
        self.__jogador = self.blackjack.jogadores[0]
        self.__columnCartasJogador = None
        self.nomeJogador = None
        self.__jogadorPodeComprar = True
        self.__columnCartasDealer = None
        
        # Criação dos botões com a lógica correta
        self.__create_buttons()
        self.__build()

    def __create_buttons(self):
        """Recria os botões, com a lógica de habilitar/desabilitar correta."""
        self.__botaoComprar = ft.ElevatedButton(
            icon=ft.icons.ADD, text="Comprar",
            icon_color=ft.colors.BLUE,
            on_click=self.__handleAddCartaJogador,
            disabled=not self.blackjack.verificarJogadorPodeContinuar(self.__jogador)
        )

        self.__botaoParar = ft.ElevatedButton(
            icon=ft.icons.STOP,
            text="Parar",
            icon_color=ft.colors.RED,
            on_click=self.__handleParar
        )

        self.__botaoDoubleDown = ft.ElevatedButton(
            icon=ft.icons.DOUBLE_ARROW, text="Dobrar",
            icon_color=ft.colors.GREEN,
            tooltip="Ao dobrar você vai receber somente mais uma carta!",
            on_click=self.__handleDoubleDown
        )

        self.__botaoReiniciar = ft.ElevatedButton(
            text="Reiniciar",
            icon=ft.icons.RESTART_ALT,
            icon_color=ft.colors.BLUE,
            on_click=self.__handleReset
        )

    def __build(self):
        """Constrói a interface do jogo com as cartas e botões atualizados."""
        self.__buildContainerCartasDealer()
        self.__buildContainerCartasJogador()

        containerDealer = ft.Column(
            controls=[self.__columnCartasDealer]
        )
        
        containerJogador = ft.Column(
            controls=[self.__columnCartasJogador]
        )

        self.bottom_appbar = ft.BottomAppBar(
            bgcolor=ft.colors.BLUE,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.__botaoComprar,
                    self.__botaoDoubleDown,
                    self.__botaoParar,
                    self.__botaoReiniciar,
                ]
            ),
        )

        self.controls = [ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    containerDealer,
                    ft.Divider(thickness=10, color="black"),
                    containerJogador
                ]
            )
        )]

        self.page.update()

    def __handleAddCartaJogador(self, e):
        """Lógica para quando o jogador comprar uma carta."""
        if not self.blackjack.verificarJogadorPodeContinuar(self.__jogador):
            self.page.open(ft.SnackBar(ft.Text(f"{self.__jogador.getNomeJogador()} não pode comprar mais!")))
            return
        
        self.blackjack.adicionarCartaJogador(self.__jogador)
        self.__botaoDoubleDown.disabled = True
        self.__build()
        
        if self.__jogador.getValorMao() >= 21:
            self.__jogadaDealer()

    def __handleDoubleDown(self, e):
        """Lógica para quando o jogador dobrar."""
        if self.__jogador.getValorMao() < 21:
            self.blackjack.adicionarCartaJogador(self.__jogador)
            self.__jogadaDealer()

    def __handleParar(self, e):
        """Lógica para quando o jogador parar a sua jogada."""
        self.__jogadaDealer()

    def __handleReset(self, e):
        """Lógica para reiniciar o jogo."""
        self.__resetClasse()
        self.__build()

    def __resetClasse(self):
        """Reseta a classe e reinicializa o estado do jogo."""
        self.blackjack = Blackjack(self.states.getTransferenciaByKey("jogadores"), 4)
        self.__jogador = self.blackjack.jogadores[0]
        self.__columnCartasJogador = None
        self.__columnCartasDealer = None
        
        # Recria os botões com os estados corretos após o reset
        self.__create_buttons()

    def __buildContainerCartasJogador(self):
        """Constrói o container de cartas do jogador."""
        self.nomeJogador = ft.Text(f"{self.__jogador.getNomeJogador()} - tem {self.__jogador.getValorMao()}", weight="bold", size=20, text_align=ft.TextAlign.CENTER)
        
        self.__columnCartasJogador = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.nomeJogador,
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
        """Gera a lista de imagens das cartas."""
        rowCartas = ft.Row()
        for carta in cartas:
            rowCartas.controls.append(
                ft.Image(f"cartas/{carta.getNomeImagem()}")
            )
        return rowCartas

    def __getImagensCartasExecutavel(self, cartas: list[Carta]):
        """Gera a lista de imagens das cartas para a versão executável."""
        rowCartas = ft.Row()
        for carta in cartas:
            if getattr(sys, 'frozen', False):
                caminho_imagem = os.path.join(sys._MEIPASS, 'cartas', carta.getNomeImagem())
            else:
                caminho_imagem = os.path.join(os.path.dirname(__file__), 'cartas', carta.getNomeImagem())
            
            rowCartas.controls.append(
                ft.Image(caminho_imagem)
            )
        return rowCartas

    def __jogadaDealer(self):
        """Lógica para a jogada do dealer após o jogador parar ou dobrar."""
        self.__botaoReiniciar.disabled = True
        self.__botaoComprar.disabled = True
        self.__botaoDoubleDown.disabled = True
        self.__botaoParar.disabled = True
        self.__build()
        
        while self.blackjack.verificarDealerPodeContinuar():
            self.blackjack.adicionarCartaDealaer()
            self.__build()
            time.sleep(2)
        
        mensagem = self.blackjack.verificarVencedor()
        
        modal = Modal.newModal(self.page)
        modal.setTitle(mensagem)
        modal.setContent(mensagem)
        modal.removeActionButtons()
        self.page.open(modal.getModal())
        time.sleep(4)
        self.page.close(modal.getModal())
        
        self.__handleReset(None)

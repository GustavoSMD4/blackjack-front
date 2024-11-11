import os
import sys
import time
import flet as ft

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
        self.blackjack = Blackjack([self.states.getUsuarioLogado()["usuario"]], 4)
        self.__jogador = self.blackjack.jogadores[0]
        self.__columnCartasJogador = None
        self.nomeJogador = None
        self.__columnCartasDealer = None
        self.__valorAposta = ft.TextField(label="Valor aposta(somente números pares)", value="100")
        
        # Criação dos botões com a lógica correta
        self.__create_buttons()
        self.__openModalAposta()

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
        
    def __openModalAposta(self):
        
        def addRemove(e: ft.ControlEvent):
            valor = float(self.__valorAposta.value)
            
            if e.control.key == "add":
                self.__valorAposta.value = valor + 10
                
            if e.control.key == "remove":
                self.__valorAposta.value = valor - 10
            
            self.__valorAposta.update()
            
        
        container = ft.Container(
            content=ft.Column(
                width=500,
                controls=[
                    ft.TextField(value=self.states.getUsuarioLogado()["usuario"], disabled=True, label="Jogador"),
                    ft.Row(
                        controls=[
                            ft.Text("Saldo:", size=18, weight="bold"),
                            ft.Text(self.states.getUsuarioLogado()["saldo"], size=18, weight="bold")
                        ]
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.REMOVE,
                                key="remove",
                                on_click=addRemove
                            ),
                            
                            self.__valorAposta,
                            
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                key="add",
                                on_click=addRemove
                            )
                            
                        ]
                    ),
                    
                    ft.ElevatedButton(
                        text="Adicionar Saldo",
                        icon=ft.icons.MONEY,
                        bgcolor="blue",
                        on_click=lambda _: self.page.go("/addsaldo")
                    )
                ]
            )
        )
        
        modal = Modal.newModal(self.page)
        modal.removeCancelarButton()
        modal.setTitle("Valor da aposta")
        modal.setContent(container)
        modal.setActionAoConfirmar(self.__confirmarAposta)
        self.page.open(modal.getModal())
        
    def __confirmarAposta(self):
        if not self.__valorAposta.value:
            return  

        valor_aposta = float(self.__valorAposta.value)

        if valor_aposta > self.states.getUsuarioLogado()["saldo"]:
            self.page.open(ft.SnackBar(ft.Text("Jogador não tem saldo para realizar essa aposta!")))
            self.__openModalAposta()  # Reabre o modal
            return  # Interrompe a execução do código para evitar reentradas

        if valor_aposta % 2 != 0:
            self.page.open(ft.SnackBar(ft.Text("Aposta só pode ser número par!")))
            self.__openModalAposta()  # Reabre o modal
            return  # Interrompe a execução do código para evitar reentradas

        if valor_aposta <= 0:
            self.page.open(ft.SnackBar(ft.Text("Aposta precisa ser maior que zero!")))
            self.__openModalAposta()  # Reabre o modal
            return  # Interrompe a execução do código para evitar reentradas

        self.__jogador.setValorAposta(valor_aposta)
        self.__build()
        
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
        
        if self.states.getUsuarioLogado()["saldo"] < self.__jogador.getValorAposta() * 2:
            self.page.open(ft.SnackBar(ft.Text("Jogador não tem saldo para dobrar a aposta!")))
            return
        
        if self.__jogador.getValorMao() < 21:
            valorAposta = (self.__jogador.getValorAposta() * 2)
            self.__jogador.setValorAposta(valorAposta)
            self.__valorAposta.value = valorAposta
            self.__valorAposta.update()
            self.blackjack.adicionarCartaJogador(self.__jogador)
            self.__jogadaDealer()

    def __handleParar(self, e):
        """Lógica para quando o jogador parar a sua jogada."""
        self.__jogadaDealer()

    def __handleReset(self, e):
        """Lógica para reiniciar o jogo."""
        self.__resetClasse()
        self.__openModalAposta()

    def __resetClasse(self):
        """Reseta a classe e reinicializa o estado do jogo."""
        self.blackjack = Blackjack([self.states.getUsuarioLogado()["usuario"]], 4)
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
    
    def __atualizarSaldoAposJogada(self, valorAdicionar):
        """Lógica para atualizar o saldo do jogador após uma jogada"""
        self.states.updateSaldo(valorAdicionar)

    def __jogadaDealer(self):
        """Lógica para a jogada do dealer após o jogador parar ou dobrar."""
        self.__botaoComprar.disabled = True
        self.__botaoDoubleDown.disabled = True
        self.__botaoParar.disabled = True
        self.__build()
        
        while self.blackjack.verificarDealerPodeContinuar():
            self.blackjack.adicionarCartaDealaer()
            self.__build()
            time.sleep(2)
        
        resposta = self.blackjack.verificarVencedor()
        
        mensagem = resposta.get("mensagem")
        ganhou = "Empate"
        
        if resposta.get("ganhou") == 1:
            ganhou = f"{self.__jogador.getNomeJogador()} Ganhou!"
            
        if resposta.get("ganhou") == 0:
            ganhou = f"{self.__jogador.getNomeJogador()} Perdeu!"
            
        content = ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=300,
                controls=[
                    ft.Text(ganhou, size=20, weight="bold"),
                    ft.Text(value=f"Total {resposta.get('valor')}", size=20, weight="bold")
                ]
            )
        )
        
        self.__atualizarSaldoAposJogada(resposta.get('valor'))
        
        modal = Modal.newModal(self.page)
        modal.setTitle(mensagem)
        modal.setContent(content)
        modal.removeActionButtons()
        self.page.open(modal.getModal())
        time.sleep(4)
        self.page.close(modal.getModal())
        
        self.__handleReset(None)

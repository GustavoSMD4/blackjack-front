import os
import sys
import time
import flet as ft

from classes.blackjack import Blackjack
from classes.carta import Carta
from classes.jogador import Jogador
from components.modal import Modal
from states import States
from views.jogoViewControls import JogoViewControls

class JogoView(ft.View):
    def __init__(self, page: ft.Page, states: States):
        super().__init__()
        
        self.route = "/blackjack"
        self.scroll = "auto"
        self.page = page
        self.states = states
        self.blackjack = Blackjack([self.states.getUsuarioLogado()["usuario"]], 4)
        self.__jogador = self.blackjack.jogadores[0]
        self.nomeJogador = None
        self.__valorAposta = ft.TextField(label="Valor aposta(somente números pares)", value="100")
        self.__maoDividida = False
        self.__contadorMaoDividida = 1
        self.__maosDivididas: list[Jogador] = None
        
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
            on_click=self.__handleDoubleDown,
            disabled=not self.blackjack.verificarJogadorPodeContinuar(self.__jogador)
        )
        
        self.__botaoSplit = ft.ElevatedButton(
            text="Dividir",
            icon=ft.icons.SPLITSCREEN,
            disabled=not self.blackjack.verificarJogadorPodeDividir(self.__jogador),
            on_click=self.__handleSplit
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
                height=300,
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
        
        self.bottom_appbar = ft.BottomAppBar(
            bgcolor=ft.colors.BLUE,
            height=100,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        controls=[
                            self.__botaoComprar,
                            self.__botaoDoubleDown,
                            self.__botaoSplit,
                        ]
                    ),
                    
                    self.__botaoParar,
                    
                ]
            ),
        )
        
        self.controls = [JogoViewControls(self.page, self.states, self.__jogador, self.blackjack).controls()]
        
        if self.__maoDividida == True:
            self.controls.insert(0, ft.Text("Dividir ainda não está funcionando corretamente!", size=30, weight="bold"))
        
        self.page.update()

    def __handleAddCartaJogador(self, e):
        """Lógica para quando o jogador comprar uma carta."""
        if not self.blackjack.verificarJogadorPodeContinuar(self.__jogador):
            self.page.open(ft.SnackBar(ft.Text(f"{self.__jogador.getNomeJogador()} não pode comprar mais!")))
            return
        
        self.blackjack.adicionarCartaJogador(self.__jogador)
        self.__botaoDoubleDown.disabled = True
        self.__build()
        
        if self.__jogador.getValorMao() >= 21 and self.__maoDividida == False:
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
            
            if self.__maoDividida == False:
                self.__jogadaDealer()

    def __handleSplit(self, e):
        if not self.blackjack.verificarJogadorPodeDividir(self.__jogador):
            self.page.open(ft.SnackBar(ft.Text("Jogador não pode dividir")))
            return
        
        if self.states.getUsuarioLogado()["saldo"] < self.__jogador.getValorAposta() * 2:
            self.page.open(ft.SnackBar(ft.Text("Jogador não tem saldo para dobrar a aposta!")))
            return
        
        self.__botaoSplit.disabled = True
        self.__maoDividida = True
        self.__maosDivididas = self.blackjack.dividirMaoJogador(self.__jogador)
        self.__jogadaDividida()
        
    def __jogadaDividida(self):
        if self.__contadorMaoDividida == 1:
            self.__jogador = self.__maosDivididas[0]
            self.__build()
            return
            
        self.__jogador = self.__maosDivididas[1]
        self.__build()
        
    def __handleParar(self, e):
        """Lógica para quando o jogador parar a sua jogada."""
        if self.__maoDividida == False:
            self.__jogadaDealer()
            return
        
        if self.__contadorMaoDividida == 1:
            self.__contadorMaoDividida = 2
            self.__jogadaDividida()
            return
            
        if self.__contadorMaoDividida == 2:
            self.__jogadaDealer()

    def __handleReset(self, e):
        """Lógica para reiniciar o jogo."""
        self.__resetClasse()
        self.__openModalAposta()

    def __resetClasse(self):
        """Reseta a classe e reinicializa o estado do jogo."""
        self.blackjack = Blackjack([self.states.getUsuarioLogado()["usuario"]], 4)
        self.__jogador = self.blackjack.jogadores[0]
        self.__maoDividida = False
        self.__contadorMaoDividida = 1
        self.__maosDivididas: list[Jogador] = None
        
        # Recria os botões com os estados corretos após o reset
        self.__create_buttons()

    def __atualizarSaldoAposJogada(self, valorAdicionar):
        """Lógica para atualizar o saldo do jogador após uma jogada"""
        self.states.updateSaldo(valorAdicionar)

    def __jogadaDealer(self):
        """Lógica para a jogada do dealer após o jogador parar ou dobrar."""
        self.__botaoComprar.disabled = True
        self.__botaoDoubleDown.disabled = True
        self.__botaoParar.disabled = True
        self.__botaoSplit.disabled = True
        self.__build()
        
        while self.blackjack.verificarDealerPodeContinuar():
            self.blackjack.adicionarCartaDealaer()
            self.__build()
            time.sleep(2)
            
        self.__verificarVencedor()
        
    def __verificarVencedor(self):
        resposta = self.blackjack.verificarVencedor()
        
        mensagem = resposta[0].get("message")
        ganhou = "Empate"
        
        if resposta[0].get("ganhou") == 1:
            ganhou = f"{self.__jogador.getNomeJogador()} Ganhou!"
            
        if resposta[0].get("ganhou") == 0:
            ganhou = f"{self.__jogador.getNomeJogador()} Perdeu!"
            
        content = ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=500,
                height=300,
                controls=[
                    ft.Text(mensagem, weight="bold"),
                    ft.Text(value=f"Total {resposta[0].get('valor')}", size=20, weight="bold")
                ]
            )
        )
        
        self.__atualizarSaldoAposJogada(resposta[0].get('valor'))
        
        modal = Modal.newModal(self.page)
        modal.setTitle(ft.Text(ganhou, size=20, weight="bold"))
        modal.setContent(content)
        modal.removeActionButtons()
        self.page.open(modal.getModal())
        time.sleep(4)
        self.page.close(modal.getModal())
        
        self.__handleReset(None)

from classes.baralho import Baralho
from classes.jogador import Jogador

class Blackjack:
    def __init__(self, nomesJogadores: list[str], qtdeBaralhos: int):
        self.baralho = Baralho.newBaralho(qtdeBaralhos)
        self.jogadores: list[Jogador] = []
        self.dealer = Jogador.newJogador()
        self.dealer.setNomeJogador("Dealer")
        self.dealer.addCard(self.baralho.deal())

        for nome in nomesJogadores:
            jogador = Jogador.newJogador()
            jogador.setNomeJogador(nome)
            jogador.addCard(self.baralho.deal())
            jogador.addCard(self.baralho.deal())
            self.jogadores.append(jogador)

    def jogadaJogador(self, jogador: Jogador):
        if jogador.getCards() == 2 and jogador.getValorMao() == 21:
            return f"{jogador.getNomeJogador()} tem Blackjack!"
        
        return self.verificarJogadorPodeContinuar(jogador)
    
    def adicionarCartaJogador(self, jogador: Jogador):
        jogador.addCard(self.baralho.deal())
        
    def adicionarCartaDealaer(self):
        self.dealer.addCard(self.baralho.deal())

    def verificarJogadorPodeContinuar(self, jogador: Jogador):
        if jogador.getValorMao() == 21:
            return False

        if jogador.getValorMao() > 21:
            return False

        return True

    def verificarDealerPodeContinuar(self):
        if self.dealer.getValorMao() == 21:
            return False

        if self.dealer.getValorMao() > 21:
            return False

        if self.dealer.getValorMao() >= 17:
            return False

        return True

    def verificarVencedor(self):
        for jogador in self.jogadores:
            if len(jogador.getCards()) == 2 and jogador.getValorMao() == 21:
                if len(self.dealer.getCards()) == 2 and self.dealer.getValorMao() == 21:
                    return {
                        "message": f"{jogador.getNomeJogador()} tem blackjack, dealer tem blackjack, empate!",
                        "ganhou": 2,
                        "valor": 0
                    }

            if len(jogador.getCards()) == 2 and jogador.getValorMao() == 21:
                return {
                    "message": f"{jogador.getNomeJogador()} tem blackjack, dealer tem {self.dealer.getValorMao()}, jogador ganhou!",
                    "ganhou": 1,
                    "valor": (jogador.getValorAposta() * 1.5)
                }

            if len(self.dealer.getCards()) == 2 and self.dealer.getValorMao() == 21:
                return {
                    "message": f"{jogador.getNomeJogador()} tem {jogador.getValorMao()}, dealer tem blackjack, dealer ganhou!",
                    "ganhou": 0,
                    "valor": -jogador.getValorAposta()
                }

            if jogador.getValorMao() > 21:
                return {
                    "message": f"{jogador.getNomeJogador()} estourou, dealer Ganhou!",
                    "ganhou": 0,
                    "valor": -jogador.getValorAposta()
                }

            if jogador.getValorMao() <= 21 and self.dealer.getValorMao() > 21:
                return {
                    "message": f"Dealer estourou, {jogador.getNomeJogador()} ganhou!",
                    "ganhou": 1,
                    "valor": jogador.getValorAposta()
                }

            if jogador.getValorMao() == self.dealer.getValorMao():
                return {
                    "message": f"{jogador.getNomeJogador()} tem {jogador.getValorMao()}, Dealer tem {self.dealer.getValorMao()}. Empate!",
                    "ganhou": 2,
                    "valor": 0
                }

            if jogador.getValorMao() < self.dealer.getValorMao() and self.dealer.getValorMao() <= 21:
                return {
                    "message": f"{jogador.getNomeJogador()} tem {jogador.getValorMao()}, Dealer tem {self.dealer.getValorMao()}. Dealer ganhou!",
                    "ganhou": 0,
                    "valor": -jogador.getValorAposta()
                }

            if jogador.getValorMao() > self.dealer.getValorMao() and self.dealer.getValorMao() <= 21:
                return {
                    "message": f"{jogador.getNomeJogador()} tem {jogador.getValorMao()}, Dealer tem {self.dealer.getValorMao()}. Jogador ganhou!",
                    "ganhou": 1,
                    "valor": jogador.getValorAposta()
                }

        return {
            "message": "Resultado inesperado.",
            "ganhou": 2,
            "valor": 0
        }




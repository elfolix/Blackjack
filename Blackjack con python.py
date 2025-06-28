import random


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit  # Corazones, tréboles, etc.
        self.rank = rank  # A, 2, 3, ..., J, Q, K
        self.value = value  # 1-11 según Blackjack

    def __str__(self):
        return f"{self.rank} de {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Corazones", "Diamantes", "Tréboles", "Picas"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        values = {
            "A": 11,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "10": 10,
            "J": 10,
            "Q": 10,
            "K": 10,
        }
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank, values[rank]))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop() if self.cards else None


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # Para manejar el valor del As

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == "A":
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        # Si la suma pasa de 21 y hay un As, cuenta el As como 1 en vez de 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def draw(self, deck):
        card = deck.deal_card()
        if card:
            self.hand.add_card(card)

    def show_hand(self, show_all=True):
        print(f"{self.name} tiene: {self.hand} (Valor: {self.hand.value})")


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Jugador")
        self.dealer = Player("Crupier")

    def start_game(self):
        # Reparte 2 cartas a cada uno
        for _ in range(2):
            self.player.draw(self.deck)
            self.dealer.draw(self.deck)

        self.player.show_hand()
        print(f"Crupier muestra: {self.dealer.hand.cards[0]}")

        # Turno del jugador
        while self.player.hand.value < 21:
            decision = input("¿Quieres otra carta? (s/n): ").lower()
            if decision == "s":
                self.player.draw(self.deck)
                self.player.show_hand()
            else:
                break

        # Turno del crupier
        while self.dealer.hand.value < 17:
            self.dealer.draw(self.deck)

        self.dealer.show_hand()

        self.check_winner()

    def check_winner(self):
        player_val = self.player.hand.value
        dealer_val = self.dealer.hand.value

        if player_val > 21:
            print("Te pasaste de 21. ¡Pierdes!")
        elif dealer_val > 21 or player_val > dealer_val:
            print("¡Ganaste!")
        elif player_val == dealer_val:
            print("Empate.")
        else:
            print("El crupier gana.")

import random

# Symbols for suits
suit_symbols = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}


# Draw a card in text format
def draw_card(card):
    rank = card.rank
    symbol = suit_symbols.get(card.suit, "?")
    top = "┌─────────┐"
    middle = f"│ {rank:<2}      │"
    center = f"│    {symbol}    │"
    bottom = f"│      {rank:>2} │"
    end = "└─────────┘"
    return [top, middle, "│         │", center, "│         │", bottom, end]


# Draw a hidden card
def hidden_card():
    return [
        "┌─────────┐",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "│░░░░░░░░░│",
        "└─────────┘",
    ]


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
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
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == "A":
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def draw(self, deck):
        card = deck.deal_card()
        if card:
            self.hand.add_card(card)

    def show_hand(self, show_all=True):
        print(f"\n{self.name} has:")
        if not show_all:
            cards_to_show = [self.hand.cards[0]] + [None] * (len(self.hand.cards) - 1)
        else:
            cards_to_show = self.hand.cards

        card_lines = []
        for card in cards_to_show:
            if card is None:
                card_lines.append(hidden_card())
            else:
                card_lines.append(draw_card(card))

        for i in range(7):
            print("  ".join(card[i] for card in card_lines))

        if show_all:
            print(f"(Value: {self.hand.value})")


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player = Player("Player")
        self.dealer = Player("Dealer")

    def start_game(self):
        # Deal 2 cards to each
        for _ in range(2):
            self.player.draw(self.deck)
            self.dealer.draw(self.deck)

        self.player.show_hand()
        self.dealer.show_hand(show_all=False)

        # Player's turn
        while self.player.hand.value < 21:
            decision = input("Do you want to hit or stand? (h/s): ").lower()
            if decision == "h":
                self.player.draw(self.deck)
                self.player.show_hand()
            elif decision == "s":
                break
            else:
                print("Please, only write 'h' or 's'.")

        # Dealer's turn
        while self.dealer.hand.value < 17:
            self.dealer.draw(self.deck)

        self.dealer.show_hand(show_all=True)
        self.check_winner()

    def check_winner(self):
        player_val = self.player.hand.value
        dealer_val = self.dealer.hand.value

        print()
        if player_val > 21:
            print("You bust. You lose!")
        elif dealer_val > 21 or player_val > dealer_val:
            print("You win!")
        elif player_val == dealer_val:
            print("Push (tie).")
        else:
            print("Dealer wins.")


if __name__ == "__main__":
    while True:
        game = BlackjackGame()
        game.start_game()

        while True:
            decision = input("Do you want to play again? (y/n): ").lower()
            if decision == "y":
                break
            elif decision == "n":
                print("Thanks for playing!")
                exit()
            else:
                print("Please, only write 'y' or 'n'.")

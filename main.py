from random import shuffle


class Card:
    """
    Lager ett kort som er 1-indexed (ess = 1, 2 = 2, osv.)
    """
    def __init__(self, num: int, suit: str) -> None:
        self.num = num
        self.suit = suit

    def card_value(self) -> int:
        if 2 <= self.num <= 10:
            self.value = self.num

        elif 11 <= self.num <= 13:
            self.value = 10

        elif self.num == 1:
            self.value = 11


class Deck:
    """
    Lager en eller flere kortstokker
    """
    def __init__(self, deck_count: int = 1) -> None:
        self.deck_count = deck_count
        self.suits = "♠♡♣♢"
        self.deck = []

    def create_cards(self) -> dict:
        for num in range(1, 14):
            for suit in self.suits:
                card = Card(num, suit)
                yield card.__dict__

    def create_deck(self):
        self.deck = [card for card in self.create_cards()]*self.deck_count
        shuffle(self.deck)


class Player:
    def __init__(self) -> None:
        self.bankroll = 1000
        self.hand = []


class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.hide = True


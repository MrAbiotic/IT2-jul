class Card:
    """
    Lager ett kort som er 1-indexed (ess = 1, 2 = 2, osv.)
    """
    def __init__(self, card_num: int, suit: str) -> None:
        self.card_num = card_num
        self.suit = suit

    def card_value(self) -> int:
        if 2 <= self.card_num <= 10:
            self.value = self.card_num

        if 11 <= self.card_num <= 13:
            self.value = 10

        if self.card_num == 1:
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
        for i in range(1, 14):
            for k in self.suits:
                return Card(i, k).__dict__

    def create_deck(self):
        for i in range(self.deck_count):
            self.deck.append(self.create_cards())

class Player:
    def __init__(self) -> None:
        self.bankroll = 1000
        self.hand = []

class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.hide = True
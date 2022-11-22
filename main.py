class Card:
    """
    Lager ett kort som er 1-indexed (ess = 1, 2 = 2, osv.)
    """
    def __init__(self, card_num: int, suit: str) -> None:
        self.card_num = card_num
        self.suit = suit

    def card_value(self) -> int:
        if 2 <= self.card_num <= 10:
            return self.card_num

class Deck:
    def __init__(self, deck_count: int = 1) -> None:
        self.deck_count = deck_count
        self.suits = "♠♡♣♢"
        self.deck = []
    
    def create_cards(self) -> list:
        for i in range(1, 14):
            for k in self.suits:
                return [i, k]

    def create_deck(self):
        for i in range(self.deck_count):
            self.deck.append(self.create_cards())

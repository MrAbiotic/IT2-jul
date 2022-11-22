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


print("Hello world")
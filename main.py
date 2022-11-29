from random import shuffle

class Cards:
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
                card = Cards(num, suit)
                yield card.__dict__

    def create_deck(self):
        self.deck = [card for card in self.create_cards()]*self.deck_count
        shuffle(self.deck)


class Player:
    def __init__(self, bankroll, player_num) -> None:
        self.player_num = 0
        self.bankroll = bankroll
        self.hand = []
        self.actions_availible = ["h","hit", "s", "stand", "d", "double"]

    def action(self):
        if self.actions_availible:
            action_in = input(f"Spiller {self.player_num}'s tur:")
            while not action_in in self.actions_availible:
                print(f"Vær vennlig å tast inn en gyldig handling {(str(item) for item in self.actions_availible)}")
                action_in = input(f"Spiller {self.player_num}'s tur:")

            if action_in in ["h", "hit"]:
                Game.get_card() # OBS! Game byttes ut med hva enn spill-objektet er.
            if action_in in ["s", "stand"]:
                Game.get_card() # Samme gjelder her
            if action_in in ["d", "double"] and len(self.hand) == 2 and self.hand[0]==self.hand[1]:
                Game.get_card()
                self.actions_availible.remove("d")
                self.actions_availible.remove("double")


class Dealer(Player):
    def __init__(self) -> None:
        super().__init__()
        self.hide = True
        self.bankroll = self.bankroll * lenght(self.players) * 5


class Game:
    def start_game(self, player_count=1, player_bankroll=1000, deck_count=4):
        self.players = [
                Player(player_bankroll, player_num)
                for player_num, player in enumerate(range(player_count))
                if 1 <= player_count <= 6
        ]
        deck = Deck(deck_count=deck_count)
        deck.create_deck()
        self.deck = deck.deck

        print("Velkommen til Viken Fylkeskommune")

    def get_card(self):
        return self.deck.pop()

def game():
    spill = Game()
    spill.start_game()

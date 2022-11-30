from random import shuffle

class Cards:
    """
    Lager ett kort som er 1-indexed (ess = 1, 2 = 2, osv.)
    """
    def __init__(self, num: int, suit: str) -> None:
        self.num = num
        self.card_name = self.name_card()
        self.suit = suit
        self.card_value()

    def card_value(self) -> int: # type: ignore
        if 2 <= self.num <= 10:
            self.value = self.num

        elif 11 <= self.num <= 13:
            self.value = 10

        elif self.num == 1:
            self.value = 11

    def name_card(self):
        if self.num == 1:
            return "A"
        elif self.num == 11:
            return "J"
        elif self.num == 12:
            return "Q"
        elif self.num == 13:
            return "K"
        else:
            return self.num


class Deck:
    """
    Lager en eller flere kortstokker
    """
    def __init__(self, deck_count: int = 1) -> None:
        self.deck_count = deck_count
        self.suits = "♠♡♣♢"
        self.deck = []

    def create_cards(self) -> dict:  # type: ignore
        for num in range(1, 14):
            for suit in self.suits:
                card = Cards(num, suit)
                yield card.__dict__

    def create_deck(self):
        self.deck = [card for card in self.create_cards()]*self.deck_count
        shuffle(self.deck)


class Player:
    def __init__(self, bankroll, player_num) -> None: # type: ignore
        self.player_num = player_num
        self.bankroll = bankroll
        self.hand = [spill.get_card() for i in range(2)]
        self.actions_availible = ["h","hit", "s", "stand", "d", "double"]
        self.handlist = [hand["value"] for hand in self.hand]

    def player_turn(self):
        self.bet = input(f"Betting ({self.bankroll}): ")
        while len(self.actions_availible) >= 1:
            self.print_hand()
            self.action()
            self.money_back = self.check_hand()

    def action(self):
        print(f"Spiller {self.player_num}'s tur:\n{self.actions_availible}:")
        if self.actions_availible:
            action_in = input(f"Spiller {self.player_num}'s tur \
                        {(str(item) for item in self.actions_availible)}:")
            while not action_in in self.actions_availible:
                print(f"Vær vennlig og tast inn en gyldig handling \
                        {(str(item) for item in self.actions_availible)}")
                action_in = input(f"Spiller {self.player_num}'s tur:")

            if action_in in ["h", "hit"]:
                self.hand.append(spill.get_card())
            if action_in in ["s", "stand"]:
                self.actions_availible = []
            if action_in in ["d", "double"]:
                self.hand.append(spill.get_card())
                self.actions_availible = []
        if "d" in self.actions_availible \
            and "double" in self.actions_availible:
            self.actions_availible.remove("d")
            self.actions_availible.remove("double")

    def print_hand(self):
        for i in self.hand:
            print(f"{i['card_name']}{i['suit']}")
        print(f"\nTotal verdi: {sum(self.handlist)}")

    def check_hand(self):
        print(f"{'#':#^20}")
        self.handlist = [hand["value"] for hand in self.hand]
        if sum(self.handlist) > 21:
            self.check_for_ace()
        self.print_hand()
        if sum(self.handlist) > 21:
            print("BUST")
            return 0
        if sum(self.handlist) == 21:
            print("Blackjack")
            return 1.5
        return 1

    def check_for_ace(self):
        ace_count = self.handlist.count(11)
        for i in range(ace_count):
            if sum(self.handlist)-10*(i+1) < 21:
                for j in range(i+1):
                    self.handlist.append(-10)
                break
            else:
                self.actions_availible = []

class Dealer(Player):
    def __init__(self, bankroll, player_num) -> None: # type: ignore
        self.bankroll = bankroll * len(spill.players) * 5
        self.hand = [spill.get_card() for _ in range(2)]
        self.actions_availible = ["h", "hit", "s", "stand"]

    def action(self):
        if self.actions_availible:
            while sum([hand["value"] for hand in self.hand]) < 16:
                self.hand.append(spill.get_card())


class Game:
    def start_game(self, player_count=1, player_bankroll=1000, deck_count=4):
        deck = Deck(deck_count=deck_count)
        deck.create_deck()
        self.deck = deck.deck
        self.players = [
                Player(player_bankroll, player_num)
                for player_num, player in enumerate(range(player_count))
                if 1 <= player_count <= 6]
        print("Velkommen til Viken Fylkeskommune")

    def turns(self):
        for player in self.players:
            player.player_turn()

    def get_card(self):
        return self.deck.pop()


def main():
    global spill
    spill = Game()
    spill.start_game()


if __name__ == '__main__':
    main()

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
        self.win_value = 21
        self.bet = 0
        self.money_back = 0

    def player_turn(self):
        self.bet = float(input(f"Betting ({self.bankroll},-): "))
        while 0 > self.bet and self.bet > self.bankroll:
            print("Vær vennlig og ikke bruk penger du ikke har")
            self.bet = float(input(f"Betting ({self.bankroll}): "))
        self.bankroll -= self.bet
        while len(self.actions_availible) >= 1:
            self.action()
            self.check_hand()
            self.money_back = self.check_hand()
        self.bankroll_update()

    def action(self):
        self.print_hand()
        print(f"Spiller {self.player_num}'s tur:\n{self.actions_availible}:")
        if self.actions_availible:
            action_in = input(f"Spiller {self.player_num}'s tur \
                        {list(str(item) for item in self.actions_availible)}:")
            while not action_in in self.actions_availible:
                print(f"\n\n\nVær vennlig og tast inn en gyldig handling \
                        {self.actions_availible}")
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
        self.print_dealer_hand()
        print("Din hånd:", end=" ")
        for i in self.hand:
            print(f"{i['card_name']}{i['suit']}", end=" ")
        print(f"\nDin verdi: {sum(self.handlist)}")
        print(f"Dealers verdi: {spill.dealer.handlist[0]}")

    def print_dealer_hand(self):
        print(f"Dealers hånd: {spill.dealer.hand[0]['card_name']}{spill.dealer.hand[0]['suit']}")

    def check_hand(self):
        print(f"{'#':#^20}")
        self.handlist = [hand["value"] for hand in self.hand]
        if sum(self.handlist) > self.win_value:
            self.check_for_ace()
        # self.print_hand()
        if sum(self.handlist) > self.win_value:
            print("BUST")
            self.actions_availible = []
            return 0
        elif sum(self.handlist) == self.win_value:
            print("Blackjack")
            self.actions_availible = []
            return 2.5
        elif spill.dealer.dealer_hand_value < self.win_value:
            if sum(self.handlist) == spill.dealer.dealer_hand_value:
                return 1
            elif sum(self.handlist) > spill.dealer.dealer_hand_value:
                return 2
            else:
                return 1
        return 1

    def check_for_ace(self):
        ace_count = self.handlist.count(11)
        for i in range(ace_count):
            if sum(self.handlist)-10*(i+1) < self.win_value:
                for _ in range(i+1):
                    self.handlist.append(-10)
                break
            else:
                self.actions_availible = []

    def bankroll_update(self):
        self.bankroll += self.bet * self.money_back

    def empty_hand(self):
        self.hand = [spill.get_card() for i in range(2)]
        self.actions_availible = ["h","hit", "s", "stand", "d", "double"]
        self.handlist = [hand["value"] for hand in self.hand]
        self.win_value = 21
        self.bet = 0
        self.money_back = 0


class Dealer(Player):
    def __init__(self, bankroll, player_num) -> None: # type: ignore
        super().__init__(bankroll, player_num)
        self.hand = [spill.get_card() for _ in range(2)]
        self.actions_availible = ["h", "hit", "s", "stand"]
        self.dealer_lock = 16
        self.dealer_hand_value = self.dealer_action()
        # print(self.hand, self.dealer_hand_value)

    def dealer_action(self) -> int:
        while sum(self.handlist) < self.dealer_lock:
            self.hand.append(spill.get_card())

            self.handlist = [hand["value"] for hand in self.hand]
            if sum(self.handlist) > self.dealer_lock:
                self.check_for_ace()

        return sum(self.handlist)

    def dealer_empty_hand(self):
        self.dealer_hand_value = self.dealer_action()


class Game:
    def start_game(self, player_count=1, player_bankroll=1000, deck_count=4):
        deck = Deck(deck_count=deck_count)
        deck.create_deck()
        self.deck = deck.deck
        self.players = [
                Player(player_bankroll, player_num)
                for player_num, player in enumerate(range(player_count))
                if 1 <= player_count <= 6]
        self.dealer = Dealer(-1, -1)
        print("Velkommen til Viken Fylkeskommune")

    def turns(self):
        for player in self.players:
            player.empty_hand()
            player.player_turn()
        self.dealer.empty_hand()
        self.dealer.dealer_empty_hand()

        print(f"Dealers hånd: {self.dealer.dealer_hand_value}")
        for player in self.players:
            print(f"PLayer {player.player_num}'s bankroll: {player.bankroll},-")

    def get_card(self):
        return self.deck.pop()


def main():
    global spill
    spill = Game()
    spill.start_game()

if __name__ == '__main__':
    main()

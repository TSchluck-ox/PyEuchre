from .deck import Card, generate_deck
from .hand import Hand
from .variablecard import VariableCard
from typing import List, Generator, Tuple

def find_repeat(oiq: List[Card]) -> Card:
    for i, item in enumerate(oiq):
        if i+1 == len(oiq):
            break
        if item in oiq[i+1:]:
            return item
        
    return None

def choose_n(iter: list, n: int) -> Generator[Tuple[list, list], None, None]:
    if n == 1:
        for pos, item in enumerate(iter):
            remain = iter[:pos] + iter[pos+1:]
            yield [item], remain
    else:
        for choice, remain in choose_n(iter, n-1):
            for pos, item in enumerate(remain):
                reremain = remain[:pos] + remain[pos+1:]
                yield (choice + [item]), reremain

def generate_partitions(iter: list, b0: int, b1: int, b2: int, b3: int):
    assert len(iter) == b0 + b1 + b2 + b3
    assert all(map(lambda x: x >= 0, (b0, b1, b2, b3)))

    for bin0, the_rest in choose_n(iter, b0):
        for bin1, the_rest in choose_n(the_rest, b1):
            for bin2, bin3 in choose_n(the_rest, b2):
                yield bin0, bin1, bin2, bin3

def remove_known(known: List[Card]):
    deck = generate_deck()
    return list(filter(lambda c: c not in known, deck))

def determine_suit(card: Card, trump: str):
    if card.is_suit(trump, trump):
        return trump
    else:
        return card.suit
    
def print_verbose(*a, verbose: bool = False):
    if verbose:
        print(*a)
    
def currently_winning(trump: str, cards: List[Card], lead_player: int) -> int:
    current_top = cards[0]
    current_winner = 0 # + lead_player at the end
    for i, card in enumerate(cards):
        if i == 0:
            continue
        
        if not Hand.compare_cards(current_top, card, trump):
            current_top = card
            current_winner = i
        
    return (current_winner + lead_player) % 4

class TrickStage:
    def __init__(
            self, knowledge: dict = {}, out_of_play: List[Card] = None, trick_score: int = 0, # +- number of tricks won
            lead_player: int = None, called_player: int = None, trump: str = None,
            player0_hand: List[Card] = None, player1_hand: List[Card] = None,
            player2_hand: List[Card] = None, player3_hand: List[Card] = None,
            player0_played: List[Card] = None, player1_played: List[Card] = None,
            player2_played: List[Card] = None, player3_played: List[Card] = None,
            past_leaders: List[int] = None,
            verbose: bool = False
        ):
        self.lead_player = knowledge.get('lead_player', lead_player)
        self.called_player = knowledge.get('called_player', called_player)
        self.player0_hand = knowledge.get('player0_hand', player0_hand)
        self.trump = knowledge.get('trump', trump)
        if self.lead_player is None:
            raise ZeroDivisionError('no lead player specified')
        if self.called_player is None:
            raise ZeroDivisionError('no called player specified')
        if self.player0_hand is None:
            raise ZeroDivisionError('no player 0 hand')
        if self.trump is None:
            raise ZeroDivisionError('no trump selected')
        self.player1_hand = knowledge.get('player1_hand', player1_hand) or []
        self.player2_hand = knowledge.get('player2_hand', player2_hand) or []
        self.player3_hand = knowledge.get('player3_hand', player3_hand) or []
        self.player0_played = knowledge.get('player0_played', player0_played) or []
        self.player1_played = knowledge.get('player1_played', player1_played) or []
        self.player2_played = knowledge.get('player2_played', player2_played) or []
        self.player3_played = knowledge.get('player3_played', player3_played) or []
        self.out_of_play = knowledge.get('out_of_play', out_of_play) or []
        self.trick_score = knowledge.get('trick_score', trick_score)
        self.past_leaders = knowledge.get('past_leaders', past_leaders) or [0]
        self.verbose = verbose
        self.verify()

    def verify(self):
        all_cards = self.player0_hand + self.player1_hand + self.player2_hand + self.player3_hand + \
                    self.player0_played + self.player1_played + self.player2_played + self.player3_played + \
                    self.out_of_play
        for card in all_cards:
            if not card.verify():
                raise AssertionError(f"{card.rank} of {card.suit}")
        repeated_card = find_repeat(all_cards)
        if repeated_card is not None:
            raise AssertionError(f"{repeated_card.rank} of {repeated_card.suit} was repeated")

    def solve(self, verbose: bool = False) -> dict:
        # determine verbosity
        v = False
        if verbose or self.verbose:
            v = True

        # determine the unknowns
        player0_known = len(self.player0_hand) + len(self.player0_played) # shouldn't be player 0 unknowns?
        player1_known = len(self.player1_hand) + len(self.player1_played)
        player2_known = len(self.player2_hand) + len(self.player2_played)
        player3_known = len(self.player3_hand) + len(self.player3_played)
        out_of_play_known = len(self.out_of_play)
        assert player0_known == 5
        
        player1_unknown = VariableCard(5 - player1_known)
        player2_unknown = VariableCard(5 - player2_known)
        player3_unknown = VariableCard(5 - player3_known)
        out_of_play_unknown = VariableCard(4 - out_of_play_known)
        all_known = self.player0_hand + self.player0_played + self.player1_hand + self.player1_played + \
                    self.player2_hand + self.player2_played + self.player3_hand + self.player3_played + self.out_of_play
        
        possible_cards = remove_known(all_known)

        # stuff previously played
        played_lengths = [len(x) for x in (self.player0_played, self.player1_played, self.player2_played, self.player3_played)]
        if all(map(lambda x: x > 0, played_lengths)):
            # this says each player played at least one card
            tricks_played = min(played_lengths)
            for trick_index in range(tricks_played):
                trick_leader = self.past_leaders[trick_index]
                trick_cards = [self.player0_played[trick_index],
                               self.player1_played[trick_index],
                               self.player2_played[trick_index],
                               self.player3_played[trick_index]]
                # Determine suit necesity
                player_unknowns = [None, player1_unknown, player2_unknown, player3_unknown] # this needs to be like hand based

                lead_suit = determine_suit(trick_cards[trick_leader], self.trump)

                for trick_play_index in range(1, 4):  # see who followed suit
                    player_num = (trick_index + trick_play_index) % 4

                    # We get the unknowns of this player so we can write that a suit is impossible
                    player_n_unknown = player_unknowns[player_num]
                    if player_n_unknown is None:
                        continue  # player 0

                    if not trick_cards[player_num].is_suit(lead_suit, self.trump):
                        player_n_unknown.eliminate_suit(lead_suit)

        # determine unknown card probabilities
        possible_configs = []
        for player1_unknown_val, player2_unknown_val, player3_unknown_val, out_of_play_unknown_val in generate_partitions(
            possible_cards, 5 - player1_known, 5 - player2_known, 5 - player3_known, 4 - out_of_play_known
        ):
            for card in player1_unknown_val:
                if not player1_unknown.is_possible(card, self.trump):
                    print("[warn]skipping", player1_unknown_val, "for player 1")
                    continue

            for card in player2_unknown_val:
                if not player2_unknown.is_possible(card, self.trump):
                    print("[warn]skipping", player2_unknown_val, "for player 2")
                    continue

            for card in player3_unknown_val:
                if not player3_unknown.is_possible(card, self.trump):
                    print("[warn]skipping", player3_unknown_val, "for player 3")
                    continue

            possible_configs.append([player1_unknown_val, player2_unknown_val, player3_unknown_val, out_of_play_unknown_val])

        # stuff being played right now
        lead_suit = None
        player_currently_winning = None
        if max(played_lengths) != min(played_lengths):
            mp = max(played_lengths)
            all_played = [self.player0_played, self.player1_played, self.player2_played, self.player3_played]
            this_trick_played = [l[-1] for l in all_played if len(l) == mp]
            lead_suit = determine_suit(this_trick_played[0], self.trump)
            player_currently_winning = currently_winning(self.trump, this_trick_played, self.lead_player)

        # card consideration
        if lead_suit is not None:
            can_follow_suit = any(map(lambda c: c.is_suit(lead_suit, self.trump), self.player0_hand))
        else:
            can_follow_suit = False

        for card in self.player0_hand:
            pass



    def to_dict(self) -> dict:
        keys = [
            'lead_player',
            'called_player',
            'trump',
            'trick_score',
            'player0_played',
            'player1_played',
            'player2_played',
            'player3_played',
            'player0_hand',
            'player1_hand',
            'player2_hand',
            'player3_hand',
            'past_leaders',
            'out_of_play'
        ]
        
        def _to_dict_helper(value):
            if isinstance(value, Card):
                return value.to_dict()
            elif isinstance(value, int) or isinstance(value, str):
                return value
            elif isinstance(value, list):
                return list(map(_to_dict_helper, value))

        return {k: _to_dict_helper(v) for k,v in self.__dict__.items() if k in keys}

def test():
    ts = TrickStage(lead_player=0, called_player=0, trump='H', trick_score=0,
                    player0_hand=[Card('S', 'K')],
                    player0_played=[Card('H', 'J'), Card('C', 'J'), Card('D', '10'), Card('D', 'A')],
                    player1_played=[Card('H', '10'), Card('H', 'Q'), Card('D', 'Q'), Card('S', '9')],
                    player2_played=[Card('D', 'J'), Card('C', 'Q'), Card('C', 'K'), Card('S', 'J')],
                    player3_played=[Card('H', '9'), Card('C', '9'), Card('D', 'K'), Card('D', '9')],
                    past_leaders=[0, 0, 1, 3],
                    out_of_play=[Card('C', '10')],
                    verbose=True)
    ts.solve()
    #print(ts.to_dict())

    return ts

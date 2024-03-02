from .deck import Card
from .hand import Hand
from .variablecard import VariableCard, create_variables
from typing import List

def find_repeat(oiq: List[Card]) -> Card:
    for i, item in enumerate(oiq):
        if i+1 == len(oiq):
            break
        if item in oiq[i+1:]:
            return item
        
    return None

class TrickStage:
    def __init__(
            self, knowledge: dict = {}, out_of_play: List[Card] = None, trick_score: int = 0, # +- number of tricks won
            lead_player: int = None, called_player: int = None, trump: str = None,
            player0_hand: List[Card] = None, player1_hand: List[Card] = None,
            player2_hand: List[Card] = None, player3_hand: List[Card] = None,
            player0_played: List[Card] = None, player1_played: List[Card] = None,
            player2_played: List[Card] = None, player3_played: List[Card] = None,
            past_leaders: List[int] = None
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

    def solve(self):
        # determine the unknowns
        player0_known = len(self.player0_hand) + len(self.player0_played) # shouldn't be player 0 unknowns?
        player1_known = len(self.player1_hand) + len(self.player1_played)
        player2_known = len(self.player2_hand) + len(self.player2_played)
        player3_known = len(self.player3_hand) + len(self.player3_played)
        out_of_play_known = len(self.out_of_play)
        assert player0_known == 5

        player1_unknown = []
        player2_unknown = []
        player3_unknown = []
        out_of_play_unknown = []

        if player1_known < 5:
            player1_unknown = create_variables(5 - player1_known)
        if player2_known < 5:
            player2_unknown = create_variables(5 - player2_known)
        if player3_known < 5:
            player3_unknown = create_variables(5 - player3_known)
        if out_of_play_known < 4:
            out_of_play_unknown = create_variables(4 - out_of_play_known)
        
        for k in player1_unknown:
            print(k.index, k.total_variables, k)
        for k in out_of_play_unknown:
            print(k.index, k.total_variables, k)

def test():
    ts = TrickStage(lead_player=0, called_player=0, trump='H', trick_score=0,
                    player0_hand=[Card('S', 'K')],
                    player0_played=[Card('H', 'J'), Card('C', 'J'), Card('D', '10'), Card('D', 'A')],
                    player1_played=[Card('H', '10'), Card('H', 'Q'), Card('D', 'Q'), Card('S', '9')],
                    player2_played=[Card('D', 'J'), Card('C', 'Q'), Card('C', 'K'), Card('S', 'J')],
                    player3_played=[Card('H', '9'), Card('C', '9'), Card('D', 'K'), Card('D', '9')],
                    past_leaders=[0, 0, 1, 3],
                    out_of_play=[Card('C', '10')])
    ts.solve()

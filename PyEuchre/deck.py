from dataclasses import dataclass
from typing import List

@dataclass
class Card:
    suit: str
    rank: str

    @classmethod
    def _verify_suit(cls, suit: str) -> bool:
        return suit in ['S', 'C', 'H', 'D']
    
    @classmethod
    def _verify_rank(cls, rank: str) -> bool:
        return rank in ['9', '10', 'J', 'Q', 'K', 'A']
    
    def verify(self) -> bool:
        return Card._verify_rank(self.rank) and Card._verify_suit(self.suit)
    
    def _is_color(self, suit: str) -> bool:
        assert Card._verify_suit(suit)
        red = ['D', 'H']
        black = ['S', 'C']
        if self.suit in red:
            return suit in red
        else:
            return suit in black
        
    def is_suit(self, suit: str, trump: str) -> bool:
        assert Card._verify_suit(suit)
        assert Card._verify_suit(trump)
        if self.rank == 'J':
            if self._is_color(trump):
                return suit == trump
            else:
                return self.suit == suit
        else:
            return self.suit == suit
        
    def display(self) -> None:
        rank_dict = {
            '9': 'Nine',
            '10': 'Ten',
            'J': 'Jack',
            'Q': 'Queen',
            'K': 'King',
            'A': 'Ace'
        }

        suit_dict = {
            'C': 'Clubs',
            'S': 'Spades',
            'D': 'Diamonds',
            'H': 'Hearts'
        }

        print(f"{ rank_dict.get(self.rank) } of { suit_dict.get(self.suit) }")


def generate_deck() -> List[Card]:
    deck = []
    for suit in ['C', 'S', 'H', 'D']:
        for rank in ['9', '10', 'J', 'Q', 'K', 'A']:
            deck.append( Card( suit=suit, rank=rank ) )
    return deck
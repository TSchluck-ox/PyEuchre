from dataclasses import dataclass
from typing import List
from .deck import Card

@dataclass
class Hand:
    cards: List[Card]
    position: int

    @staticmethod
    def compare_cards(card1: Card, card2: Card, trump: str) -> bool:
        assert Card._verify_suit(trump)
        """return true if card1 beats card2"""
        trump_dict = {'9': 0, '10': 1, 'Q': 2, 'K': 3, 'A': 4, 'J': 5}
        off_dict = {'9': 0, '10': 1, 'J': 2, 'Q': 3, 'K': 4, 'A': 5}
        if card1.is_suit(suit=trump, trump=trump):
            rank1int = trump_dict.get(card1.rank)
            if card2.is_suit(suit=trump, trump=trump):
                rank2int = trump_dict.get(card2.rank)
                if rank1int > rank2int:
                    return True
                elif rank2int > rank1int:
                    return False
                else:
                    assert rank1int == rank2int == 5
                    return card1.suit == trump
            else:
                return True
        elif card2.is_suit(suit=trump, trump=trump):
            return False
        elif card2.is_suit(suit=card1.suit, trump=trump):
            rank1int = off_dict.get(card1.rank)
            rank2int = off_dict.get(card2.rank)
            if rank1int > rank2int:
                return True
            elif rank2int > rank1int:
                return False
            else:
                raise Exception('what')
        else:
            return True

    def display(self) -> None:
        print(f"Player Number {self.position}")
        for card in self.cards:
            card.display()
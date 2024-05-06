from typing import List

class VariableCard:

    def __init__(self, size : int = 1) -> None:
        self.suits = ['S', 'H', 'C', 'D']
        self.size = size
    
    def eliminate_suit(self, suit: str):
        self.suits.remove(suit)

    def is_possible(self, card, trump: str):
        for suit in self.suits:
            if card.is_suit(suit, trump):
                return True
        return False
    
    
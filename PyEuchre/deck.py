from dataclasses import dataclass

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
            pass
        else:
            return self.suit == suit
from typing import List

class VariableCard:
    total_variables = 0

    def __init__(self) -> None:
        self.index = VariableCard.total_variables
        VariableCard.total_variables += 1

    def reset(self):
        VariableCard.total_variables = 0
        return None
    
def create_variables(number: int = 1) -> List[VariableCard]:
    out = []
    for _ in range(number):
        out.append(VariableCard())
    return out
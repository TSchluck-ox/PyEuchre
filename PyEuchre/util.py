import json
from .trickstage import TrickStage

# IO
def write_trickstage(trickstage: TrickStage, destination: str) -> None:
    with open(destination, 'w') as destobj:
        json.dump(trickstage.to_dict(), destobj, indent=4)

def read_trickstage(location: str) -> TrickStage:
    with open(location, 'r') as locobj:
        return json.load(locobj)
    
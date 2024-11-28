from enum import Enum

class State(Enum):
    """
    This encapsulates every possible state for fields in the world's grid. Current options:
    - none, pit, small/big wumpus, gold, armor
    """
    NONE = ""
    PIT = "pit"
    SWUMPUS = "swumpus" # small wumpus
    LWUMPUS = "lwumpus" # big wumpus
    GOLD = "gold" # if there's different amounts of gold, add more options
    ARMOR = "armor"
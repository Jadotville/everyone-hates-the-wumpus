from enum import Enum

class State(Enum):
    """
    This provides a fixed selection of possible state for fields in the world's grid. Current options:
    - pit, wumpus, gold, armor
    """
    PIT = "pit"
    WUMPUS = "wumpus" # if there's different-sized wumpi, add more options
    GOLD = "gold" # if there's different amounts of gold, add more options
    ARMOR = "armor"

class Perception(Enum):
    """
    This provides a fixed selection of possible perceptions for agents on a grid's field. Current options:
    - breeze, stench
    """
    BREEZE = "breeze"
    STENCH = "stench"
    
class Gold_found(Enum):
    """
    This provides a fixed selection of possible reactions for agents which found gold. Current options:
    - dig, leava, bidding
    """
    dig = "dig"
    leave = "leave"
    bidding = "bidding"
    
class Status(Enum):
    """
    This provides a fixed selection of possible status for agents. Current options:
    - alive, dead
    """
    alive = "alive"
    dead = "dead"

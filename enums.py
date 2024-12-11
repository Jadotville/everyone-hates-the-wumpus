from enum import Enum

class State(Enum):
    """
    This provides a fixed selection of possible state for fields in the world's grid. Current options:
    - pit, small/big wumpus, gold, armor, sword
    
    For representing an agent's knowledge-base, you can use the following:
    - pit, small/big wumpus, safe
    """
    PIT = "pit"
    S_WUMPUS = "s_wumpus" # small wumpus
    L_WUMPUS = "l_wumpus" # large wumpus
    GOLD = "gold" # if there's different amounts of gold, add more options
    ARMOR = "armor"
    SWORD = 'sword'
    SAFE = 'safe' # only to be used for agents?

class Perception(Enum):
    """
    This provides a fixed selection of possible perceptions for agents on a grid's field. Current options:
    - breeze, (very) smelly
    """
    BREEZE = "breeze"
    SMELLY = "smelly"
    VERY_SMELLY = "very_smelly"
    
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

class Plan(Enum):
    """
    This provides a fixed selection of possible plans for agents. Current options:
    - explore, wait, go_to
    """
    EXPLORE = "explore" # unobligated, go to random/unexplored fields
    WAIT = "wait" # not moving, until plan is changed by environment/other agent (e.g. waiting for another agent to kill wumpus together)
    GO_TO = "go_to" # moving towards a given field (e.g. another agent's position, to kill wumpus together)
from abc import ABC, abstractmethod


class Agent(ABC):
    
    gold = 0
    arrows = 0
    opinions = {}
    
    @abstractmethod
    # possible actions: shoot, move, dig, rob, chat, message    
    # agent moves only if everyone moves
    
    def action(self, meeting=None, percept=None, message=None):
        pass
    
    
class PlayerAgent(Agent):
    
    def action(self):
        pass
    
    

class AIAgent(Agent):
    
    def action(self):
        pass
    
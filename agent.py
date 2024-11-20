from abc import ABC, abstractmethod

import random


class Agent(ABC):
    
    # current position on the grid (determined by the environment)
    position = [0, 0]
    # needs the agent to stay on the grid
    grid_size = 0
    # 0 -> not in a game, ID -> in a game, dead -> dead
    ID = 0
    
    gold = 0
    arrows = 0
    opinions = {}
    
    
    @abstractmethod
    # possible actions: shoot, move, dig, rob, chat, message    
    # agent moves only if everyone moves
    def action(self, meeting=None, percept=None, message=None):
        pass
    
    
class PlayerAgent(Agent):
    
    # TODO: create a playable agent
    
    def action(self, meeting=None, percept=None, message=None):
        pass
    
    

class AIAgent(Agent):

    def select_safe_moves(self):
        is_move_safe = {
            "up": True, 
            "down": True, 
            "left": True, 
            "right": True
        }
    
        safe_moves = []
        
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
        
        return safe_moves
    
    def action(self, meeting=None, percept=None, message=None):
        pass
    
# agent that moves randomly    
class RandomAgent(AIAgent):
    
    def action(self, meeting=None, percept=None, message=None):
        safe_moves = self.select_safe_moves()
        next_move = random.choice(safe_moves)
        return next_move
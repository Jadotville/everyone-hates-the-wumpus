from abc import ABC, abstractmethod

import random


class Agent(ABC):
    
    # current position on the grid (determined by the environment)
    position = [0, 0]
    # needs the agent to stay on the grid
    grid_size = 0
    # unique for every player!
    ID = 'unknown'
    # currently only dead or alive
    state = "alive"

    gold = 0
    arrows = 0
    opinions = {}
    
    
    @abstractmethod
    # possible actions: shoot, move, dig, message    
    # agent moves only if everyone moves
    def action(self, percept=None, message=None):
        pass
    
    # if a meeting is called, the agent shares the same field with other agents and can interact with them
    # possible interactions: chat, rob, nothing
    @abstractmethod
    def meeting(self, agent):
        pass
    
    # the agent receives the result of the meeting
    @abstractmethod
    def meeting_result(self, other_agent, result):
        pass
    
    
    
class PlayerAgent(Agent):
    
    # TODO: create a playable agent
    
    def action(self, meeting=None, percept=None, message=None):
        pass
    
    def meeting(self, agent):
        pass
    
    def meeting_result(self, other_agent, result):
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
        
        # check if the agent is at the edge of the grid
        if self.position[0] == 0:
            is_move_safe["up"] = False
        if self.position[0] == self.grid_size - 1:
            is_move_safe["down"] = False
        if self.position[1] == 0:
            is_move_safe["left"] = False
        if self.position[1] == self.grid_size - 1:
            is_move_safe["right"] = False    
                    
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
        
        return safe_moves
    
    def action(self, meeting=None, percept=None, message=None):
        pass
    
    def meeting(self, agent):
        pass
    
    def meeting_result(self, other_agent, result):
        pass
    
# agent that moves randomly    
class RandomAgent(AIAgent):
    
    def action(self, meeting=None, percept=None, message=None):
        safe_moves = self.select_safe_moves()
        next_move = random.choice(safe_moves)
        return next_move
    
    def meeting(self, agent):
        # TODO: implement the meeting method
        pass
    
    def meeting_result(self, other_agent, result):
        pass
from abc import ABC, abstractmethod
from enums import State, Perception, Gold_found, Status

import random


class Agent(ABC):
    
    # current position on the grid (determined by the environment)
    position = [0, 0]
    # needs the agent to stay on the grid
    grid_size = 0
    # unique for every player!
    ID = 'unknown'
    # currently only dead or alive
    status = Status.alive
    
    # the agent's perception of the environment
    perception = None

    gold = 0
    arrows = 0
    opinions = {}

    messages = {}

    @abstractmethod
    def move(self):
        """
        - the agent moves in a direction
        - possible results: up, down, left, right
        """
        pass   
     
    @abstractmethod
    def action(self):
        """
        - possible actions: shoot, dig
        - agent moves only if everyone moves
        """
        pass
    

    
    @abstractmethod
    def conversation(self):
        """
        - the agent interacts with other agents
        - possible interactions: 
        """
        pass
    
    
    @abstractmethod
    def meeting(self, agent):
        """
        - if a meeting is called, the agent shares the same field with other agents and can interact with them
        - possible interactions: chat, rob, nothing
        """
        pass
    
    
    @abstractmethod
    def meeting_result(self, other_agent, result):
        """
        - the agent receives the result of the meeting
        """
        pass
    
    def found_gold(self):
        """agents found gold on the field

        Returns:
            dig: the agent digs for gold
            leave: the agent leaves the gold
            bidding: the agent starts a bidding for the gold
        """
        pass
    
    def bidding(self, agent, gold):
        pass

    @abstractmethod
    def radio(self):
        '''
        returns 2element array with [performative verb, content]
        if nothing to say empty list
        '''
        pass
    
    
class PlayerAgent(Agent):
    
    # TODO: create a playable agent
    
    def move(self):
        pass
    
    def conversation(self):
        pass
    
    def action(self):
        pass
    
    def meeting(self, agent):
        pass
    
    def meeting_result(self, other_agent, result):
        pass
    
    def found_gold(self):
        pass
    
    def bidding(self, agent, gold):
        pass

    def radio(self):
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
    
    def action(self):
        pass
    
    def move(self):
        pass
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        pass
    
    def meeting_result(self, other_agent, result):
        pass

    def found_gold(self):
        pass
    
    def bidding(self, agent, gold):
        pass

    def radio(self):
        pass

    
# agent that moves randomly    
class RandomAgent(AIAgent):
    
    def move(self):
        safe_moves = self.select_safe_moves()
        next_move = random.choice(safe_moves)
        return next_move
    
    def action(self):
        pass
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        # TODO: implement the meeting method
        pass
    
    def meeting_result(self, other_agent, result):
        pass
    
    def found_gold(self):
        return Gold_found.dig
    
    def bidding(self, agent, gold):
        pass

    def radio(self):
        content = []
        messages = ["","Message1", "Message2", "Message3"]
        message_chosen = random.choice(messages)
        if message_chosen == "":
            return content
        content.append("inform")
        content.append(message_chosen)

        return content

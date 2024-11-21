from abc import ABC, abstractmethod

import random


class Agent(ABC):
    # 0 -> not in a game, ID -> in a game, dead -> dead (determined by the environment)
    ID = 0
    
    
    # current position on the grid (determined by the environment)
    position = [0, 0]
    
    # needs the agent to stay on the grid (determined by the environment)
    grid_size = 0
    
    # amount of gold the agent has (determined by the environment)
    gold = 0
    
    # amount of arrows the agent has (determined by the environment)
    arrows = 0
    
    # perceptions of the agent (determined by the environment)
    perceptions = []

    # opinions of ther agents (determined by the agent)
    opinions = {}
    

    
    
    # message that the agent sends to other agents
    @abstractmethod
    def send_message(self):
        pass

    
    # if there are messages from other agents, the agent receives them
    @abstractmethod
    def receive_message(self, agent, message):
        pass
    
    
    # possible actions: shoot, dig, message 
    @abstractmethod
    def action(self):
        pass
    
    # possible moves: up, down, left, right
    @abstractmethod
    def move(self):
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
    
    def send_message(self):
        pass

    def receive_message(self, agent, message):
        pass
 
    def action(self):
        pass
    
    def move(self):
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
    
    def send_message(self):
        pass

    def receive_message(self, agent, message):
        pass
 
    def action(self):
        pass
        
    def move(self):
        pass
    
    def meeting(self, agent):
        pass
    
    def meeting_result(self, other_agent, result):
        pass
    
# agent that moves randomly    
class RandomAgent(AIAgent):
    
    def send_message(self):
        pass

    def receive_message(self, agent, message):
        pass
 
    def action(self):
        pass
    
    def move(self):
        safe_moves = self.select_safe_moves()
        next_move = random.choice(safe_moves)
        return next_move
    
    def meeting(self, agent):
        pass
    
    def meeting_result(self, other_agent, result):
        pass
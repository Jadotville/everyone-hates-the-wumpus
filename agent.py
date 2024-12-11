from abc import ABC, abstractmethod
from enums import State, Perception, Gold_found, Status, Plan
from utils import get_neighbors, a_star_search

import random


class Agent(ABC):
    grid_size = 0
    def __init__(self, size):
        # needs the agent to stay on the grid
        self.grid_size = size
        
        # no knowledge on pits and wumpi locations, place State.x inside cordinates for assuming "x" is possibly on that field
        self.knowledge = [[[] for _ in range(size)] for _ in range(size)]
    
    # current position on the grid (determined by the environment)
    position = [0, 0]
    # unique for every player!
    ID = 'unknown'
    # currently only dead or alive
    status = Status.alive
    
    # the agent's perception of the environment
    perceptions = None

    gold = 0
    arrows = 0
    opinions = {}

    messages = {}
    
    # start randomly exploring
    plan = {
        "status": Plan.EXPLORE,
        "patience": None, # optional int: agent follows a plan for a set number of actions, before resetting to "status": Plan.EXPLORE
        "target_pos": None # optional [int,int]: when "status": Plan.GO_TO the agent should go to specified position
    }

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
    
    def update_plan(self):
        """
        Resets the agent's plan back to Plan.EXPLORE, when patience hits 0
        """
        if self.plan["target_pos"] == self.position:
            self.plan["patience"] = None
            self.plan["status"] = Plan.EXPLORE
            self.plan["target_pos"] = None
        elif self.plan["patience"] == None:
            return
        elif self.plan["patience"] > 0:
            self.plan["patience"] -= 1
        elif self.plan["patience"] <= 0:
            self.plan["patience"] = None
            self.plan["status"] = Plan.EXPLORE
            self.plan["target_pos"] = None
    
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
        
        # check, if the agent considers the neighboring fields unsafe
        neighbors = get_neighbors(self.knowledge, self.position[0], self.position[1], return_format="full")
        for row, col, dir in neighbors:
            if ( self.knowledge[row][col]
                or self.knowledge[row][col] == State.S_WUMPUS
                or self.knowledge[row][col] == State.L_WUMPUS):
                is_move_safe[dir] = False
        
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
        
        return safe_moves
    
    def update_knowledge(self):
        """UNTESTED: Updates the agent's knowledge base on pit/wumpus locations. Should be called every turn"""
        assumptions = {
            Perception.BREEZE: State.PIT,
            Perception.SMELLY: State.S_WUMPUS,
            Perception.VERY_SMELLY: State.L_WUMPUS
        }
        neighbors = get_neighbors(self.knowledge, self.position[0], self.position[1])
        
        # assume safe fields nearby, when nothing was percepted
        if not perception:
            for row, col in neighbors:
                self.knowledge[row][col] == [State.SAFE]
        
        # assume pits/wumpi nearby, where fields are still not considered safe
        for perception in self.perceptions:
            for row, col in neighbors:
                if self.knowledge[row][col] != [State.SAFE]:
                    self.knowledge[row][col].append(assumptions[perception])
            
    
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
        status = self.plan["status"]
        if status == Plan.EXPLORE:
            safe_moves = self.select_safe_moves()
            next_move = random.choice(safe_moves)
        elif status == Plan.WAIT:
            next_move = None
        elif status == Plan.GO_TO:
            next_move = a_star_search(self.knowledge, (self.position[0], self.position[1]), self.plan["target_pos"])[0]
        
        self.update_plan()
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

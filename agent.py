from abc import ABC, abstractmethod
from enums import State, Perception, Gold_found, Status, Plan
from utils import get_neighbors, a_star_search, convert_to_direction, append_unique, list_difference
from random import random

import random


class Agent(ABC):
    
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
    """WIP: Agent that is controlled by the user."""
    
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
    """Base logic for all AI-controlled Agents."""
    def __init__(self, size=0, init_plan=None, debug=False, risk_aversion=1):
        """
        :param int size: Set this to the size the game's grid uses.
        :param dict init_plan: An optional plan, which the agent has to follow on first initialization. Check the constructor for format reference.
        :param bool debug: Optional toggle for printing debug information
        :param float risk_aversion: optional value between [0,1] to encapsulate general risk aversion, e.g. 0.8 will make the agent step into a possible danger by 20% chance
        """
        if size <= 0:
            print("AIAgent: WARNING - An Agent has been initialized without a proper grid_size. The Agent might not work properly.")
        # needs the agent to stay on the grid
        self.grid_size = size
        
        # set up the plan
        if init_plan:
            self.plan = init_plan
        else:
            # start randomly exploring
            self.plan = {
                "status": Plan.RANDOM,
                "patience": None, # optional int: agent follows a plan for a set number of actions, before resetting to "status": Plan.RANDOM
                "target_pos": [] # optional [[int,int], ...]: when "status": Plan.GO_TO the agent should go to specified position
            }
        
        # OLD-ver (no blocks): no knowledge on pits and wumpi locations, place State.x inside cordinates for assuming "x" is possibly on that field
        # self.knowledge = [[[] for _ in range(size)] for _ in range(size)]
        
        # NEW-ver (with blocks)
        self.knowledge = [[{
                            "state": [], # assumes, that a field could have this state
                            "blocks": [] # assumes, that a field 100% cannot have this state
                            } for _ in range(size)] for _ in range(size)]
        self.debug = debug
        self.risk_aversion = risk_aversion

    def select_safe_moves(self):
        is_move_safe = {
            "up": True, 
            "down": True, 
            "left": True, 
            "right": True
        }
    
        safe_moves = []
        in_bounds_moves = []
        
        # check if the agent is at the edge of the grid
        if self.position[0] == 0:
            is_move_safe["up"] = False
        if self.position[0] == self.grid_size - 1:
            is_move_safe["down"] = False
        if self.position[1] == 0:
            is_move_safe["left"] = False
        if self.position[1] == self.grid_size - 1:
            is_move_safe["right"] = False    
        
        # moves that stay inside the grid
        for move, isSafe in is_move_safe.items():
            if isSafe:
                in_bounds_moves.append(move)
        
        # check, if the agent considers the neighboring fields unsafe
        neighbors = get_neighbors(self.knowledge, self.position[0], self.position[1], return_format="full")
        for row, col, dir in neighbors:
            if (State.PIT in self.knowledge[row][col]["state"]
                or State.S_WUMPUS in self.knowledge[row][col]["state"]
                or State.L_WUMPUS in self.knowledge[row][col]["state"]):
                is_move_safe[dir] = not random.random() <= self.risk_aversion
        
        # moves that stay inside the grid and avoid obstacles
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)
        
        # emergency case: When no move is safe, move randomly inside bounds
        return safe_moves if safe_moves else in_bounds_moves
    
    def update_plan(self):
        """
        Changes the AI-agent's plan based on reaching the goal or missing patience
        """
        # removing target goals
        if self.position in self.plan["target_pos"]:
            if self.debug:
                print("Agent: INFO - Agent " + self.ID + " has reached goal " + str(self.position))
            self.plan["target_pos"].remove(self.position)
        
        # set target to a remaining unexplored field when exploring
        if self.plan["status"] == Plan.EXPLORE:
            self.plan["target_pos"] = [
                [row, col]
                for row in range(len(self.knowledge))
                for col in range(len(self.knowledge[row]))
                if not self.knowledge[row][col]["state"]
            ]
            if self.debug:
                print("Agent: INFO - Agent " + self.ID + " has goals " + str(self.plan["target_pos"]))
            
        if not self.plan["target_pos"]:
            self.reset_plan
        
        # patience management
        if self.plan["patience"] == None:
            return
        elif self.plan["patience"] > 0:
            self.plan["patience"] -= 1
        elif self.plan["patience"] <= 0:
            self.reset_plan()
    
    def reset_plan(self):
        """Sets the AI-agent's plan back to randomly moving"""
        self.plan["patience"] = None
        self.plan["status"] = Plan.RANDOM
        self.plan["target_pos"] = None
    
    def update_knowledge(self):
        """UNTESTED: Updates the agent's knowledge base on pit/wumpus locations. Should be called every turn"""
        assumptions = {
            Perception.BREEZE: State.PIT,
            Perception.SMELLY: State.S_WUMPUS,
            Perception.VERY_SMELLY: State.L_WUMPUS
        }
        neighbors = get_neighbors(self.knowledge, self.position[0], self.position[1])
        missing_perceptions = list_difference(assumptions.keys(), self.perceptions)
        
        # if self.debug:
        #     print("Agent: INFO - The following perceptions were NOT made " + str(missing_perceptions))
        
        # assume safe fields nearby, when nothing was percepted
        # print(self.perceptions)
        if self.perceptions == []:
            self.knowledge[self.position[0]][self.position[1]]["state"] = [State.SAFE]
            for row, col in neighbors:
                self.knowledge[row][col]["state"] = [State.SAFE]
        
        # assume pits/wumpi nearby, where fields are still not considered safe
        for perception in self.perceptions:
            for row, col in neighbors:
                if self.knowledge[row][col]["state"] != [State.SAFE]:
                    append_unique(self.knowledge[row][col], assumptions[perception], safe=True)
        
        # remove and block an assumption, if the corresponding perception is missing
        for perception in missing_perceptions:
            for row, col in neighbors:
                # block an assumption
                append_unique(self.knowledge[row][col]["blocks"], assumptions[perception])
                # remove an existing assumption
                if assumptions[perception] in self.knowledge[row][col]["state"]:
                    if self.debug:
                        print("Agent: INFO - Removing assumption " + str(assumptions[perception]) + " at location " + str((row,col)))
                    self.knowledge[row][col]["state"].remove(assumptions[perception])
        
        
        if self.debug:
            self.print_knowledge()
           
    def print_knowledge(self):
        """Prints the agents knowledge-grid with safe/pit/wumpus assumptions. Can be used for debugging."""
        # set up new grid with shortened State.x 
        k = self.knowledge
        p = [[[] for _ in range(len(k))] for _ in range(len(k))]
        for row in range(len(k)):
            for col in range(len(k)):
                if k[row][col]["state"]:
                    for s in k[row][col]["state"]:
                        p[row][col].append(s.value[0])
        
        # print the results with aliged grid
        print("Knowledge base of Agent " + str(self.ID) + " :")
        max_width = max(len(str(value)) for row in p for value in row)
        for row in p:
            formatted_row = " ".join(f"{''.join(map(str, value)):{max_width}}" for value in row)
            print(formatted_row)
     
    def action(self):
        pass
    
    def move(self):
        """
        Risk-averse AI-move logic for:
        - Random: Moves randomly
        - Waiting: Will not move, until patience runs out or plan is changed by environment
        - Going: Moving towards a specified field via A*-search
        - Exploring: Moving towards an unexplored field via A*-search
        This was tested, so use this as a base for other agents.
        """
        # update first, to prevent errors, e.g. trying to go to a field you already arrived at
        self.update_knowledge()
        self.update_plan()
        status = self.plan["status"]
        if status == Plan.RANDOM:
            # self.print_knowledge() # for debugging, can be commented out
            safe_moves = self.select_safe_moves()
            next_move = random.choice(safe_moves)
        elif status == Plan.WAIT:
            next_move = None
        elif status == Plan.GO_TO or status == Plan.EXPLORE:
            # self.print_knowledge() # for debugging, can be commented out
            path = a_star_search(self.knowledge, (self.position[0], self.position[1]), (self.plan["target_pos"][0][0],self.plan["target_pos"][1][1]))
            
            # go back to exploring, if no path available, otherwise proceed
            if path is None:
                safe_moves = self.select_safe_moves()
                next_move = random.choice(safe_moves)
            else:
                next_move = convert_to_direction(self.position, path[1])
        
        return next_move
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        pass
    
    def meeting_result(self, other_agent, result):
        pass

    def radio(self):
        pass


class RightAgent(AIAgent):
    """Agent that moves only right and ignores all plans."""
    
    def move(self):
        """Moves right only"""
        return "right"
    
    def action(self):
        pass
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        # TODO: implement the meeting method
        pass
    
    def meeting_result(self, other_agent, result):
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
    
       
class RandomAgent(AIAgent):
    """Agent that moves randomly."""
    
    def action(self):
        pass
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        # TODO: implement the meeting method
        pass
    
    def meeting_result(self, other_agent, result):
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
  
class RandomBadAgent(AIAgent):
    """
    Agent that moves randomly.
    - will always rob in meetings
    """
    
    def action(self):
        pass
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        return "rob"
    
    def meeting_result(self, other_agent, result):
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

# Cooperative Agent to get gold efficiently
class CooperativeAgent(AIAgent):
    
    def __init__(self, size):
        super().__init__(size)
        self.gold_positions = []  # List of known gold positions
        self.shared_knowledge = {}  # Stores messages received from other agents
    
    def move(self):
        # Process received messages
        for key, message in self.messages.items():
            if "Gold at" in message:
                gold_pos = eval(message.split("at")[1])  # Extract the position
                if gold_pos not in self.gold_positions:
                    self.gold_positions.append(gold_pos)
        
        # If gold is known, plan to move there
        if self.gold_positions:
            target = self.gold_positions[0]  # Go to the first known gold position
            self.plan = {"status": Plan.GO_TO, "target_pos": target}
            path = a_star_search(self.knowledge, tuple(self.position), target)
            if path:
                return path[0]  # Follow the first step in the path
            else:
                self.gold_positions.pop(0)  # Remove inaccessible gold
        
        # Default behavior: Continue exploring
        self.plan["status"] = Plan.RANDOM
        safe_moves = self.select_safe_moves()
        return random.choice(safe_moves) if safe_moves else None
    
    def update_knowledge(self):
        # Update knowledge based on perceptions
        if not self.perceptions:
            neighbors = get_neighbors(self.knowledge, self.position[0], self.position[1])
            for row, col in neighbors:
                self.knowledge[row][col]["state"].append(State.SAFE)
        for perception in self.perceptions:
            if perception == Perception.BREEZE:
                neighbors = get_neighbors(self.knowledge, self.position[0], self.position[1])
                for row, col in neighbors:
                    if State.SAFE not in self.knowledge[row][col]["state"]:
                        self.knowledge[row][col]["state"].append(State.PIT)
    
    def action(self):
        # Dig if gold is on the current field
        if State.GOLD in self.perceptions:
            if self.position in self.gold_positions:
                self.gold_positions.remove(self.position)
            return "dig"
        return None

    def meeting(self, agent):
        # Do nothing during meetings, could be extended
        return "nothing"

    def meeting_result(self, other_agent, result):
        # No specific reaction required
        pass
    
    def radio(self):
        # Share information about gold
        content = []
        if State.GOLD in self.perceptions:
            content.append("inform")
            content.append(f"Gold at {self.position}")
        return content

# defensive agent who collects gold and ist defensive against robbing
class DefensiveAgent(AIAgent):
    def __init__(self, size):
        super().__init__(size)
        self.armor = 2  # Start with 2 pieces of armor to defend against robbing
        self.survival_mode = False  # Focus on collecting gold rather than evasion

    def move(self):
        # Prioritize gold collection if gold is perceived
        if State.GOLD in self.perceptions:
            return "dig"
        
        # Use A* to navigate to known gold positions if available
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if State.GOLD in self.knowledge[row][col]["state"]:
                    path = a_star_search(self.knowledge, tuple(self.position), (row, col))
                    if path:
                        return path[0]
        
        # Default: Explore safely
        safe_moves = self.select_safe_moves()
        return random.choice(safe_moves) if safe_moves else None

    def update_knowledge(self):
        # Update knowledge based on perceptions
        neighbors = get_neighbors(self.knowledge, self.position[0], self.position[1])
        if not self.perceptions:
            for row, col in neighbors:
                self.knowledge[row][col]["state"] = [State.SAFE]
        for perception in self.perceptions:
            if perception == Perception.BREEZE:
                for row, col in neighbors:
                    if State.SAFE not in self.knowledge[row][col]["state"]:
                        self.knowledge[row][col]["state"].append(State.PIT)

    def meeting(self, agent):
        # Defensive behavior in meetings
        if isinstance(agent, RandomBadAgent):
            if self.armor > 0:
                return "nothing"  # Use armor to block robbing
            else:
                return "rob"  # Attempt to rob back if no armor is left

        # Neutral behavior with cooperative agents
        return "nothing"

    def meeting_result(self, other_agent, result):
        pass

    def radio(self):
        # Share information about gold to cooperative agents
        content = []
        if State.GOLD in self.perceptions:
            content.append("inform")
            content.append(f"Gold at {self.position}")
        return content

    def action(self):
        # Dig gold if present, otherwise no action
        if State.GOLD in self.perceptions:
            return "dig"
        return None


# TODO
# explorative Agent
# aggressive agent

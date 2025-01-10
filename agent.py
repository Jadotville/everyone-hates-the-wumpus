from abc import ABC, abstractmethod
from enums import State, Perception, Gold_found, Status, Plan
from utils import get_neighbors, a_star_search, convert_to_direction, append_unique, list_difference
from random import random
from re import findall

import random

GUESS_PADDING = 10 # used for padding the length of a safe-assumed path to a large wumpus
MAX_ARROWS = 3 # inventory space for arrows
ARROW_PRICE = 2 # from grid_properties in simulation.py

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
    arrows = 2 # normally start with 1 instead
    opinions = {}
    armor = 0
    messages = {}

    @abstractmethod
    def move(self):
        """
        - the agent moves in a direction
        - possible results: up, down, left, right
        """
        pass   
     
    @abstractmethod
    def shoot(self):
        """
        - possible results: up, down, left, right, None
        - shoots an arrow in a direction that flies one filed and kills the wumpus, if its there
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
        content in form of:
        "w(x,y) p(x,y) s(m,x,y)"
        => wumpus at x,y, postition at x,y, shoot in m moves at x,y
        -1 if you dont want to give
        if nothing to say empty list
        '''
        pass
    
    @abstractmethod
    def buy_arrows(self):  
        ''' every new rount the agent can buy arrows for 2 gold per each
        if an agent has not enough gold for the amount of arrows he wants to buy, he buys as many as he can afford
        
        Returns:
            0: the agent does not want to buy arrows
            any positive number: the agent buys the number of arrows
        '''  
        pass
    
class PlayerAgent(Agent):
    """WIP: Agent that is controlled by the user."""
    
    # TODO: create a playable agent
    
    def move(self):
        pass
    
    def conversation(self):
        pass
    
    def shoot(self):
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
                "target_pos": [], # optional [[int,int], ...]: when "status": Plan.GO_TO the agent should go to specified position
                "shoot_pos": [] # optional [[int,int]]: upon reaching a target_pos, shoot these coordinates (requires convertion to direction)
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
        """
        Returns a list of moves, which are within bounds and considered safe regarding the agent's knowledge. 
        - If no move is safe, it chooses a random in-bounds move instead
        - Considers the agent's risk-aversion, to potentially take risks
        """
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
                print("Agent-" + str(self.ID) + ": Reached goal " + str(self.position))
            self.plan["target_pos"].remove(self.position)
            
            if self.plan["status"] == Plan.GO_TO:
                self.plan["status"] = Plan.WAIT
        
        # set target to a remaining unexplored field when exploring
        if self.plan["status"] == Plan.EXPLORE:
            self.plan["target_pos"] = [
                [row, col]
                for row in range(len(self.knowledge))
                for col in range(len(self.knowledge[row]))
                if not self.knowledge[row][col]["state"]
            ]
            if self.debug:
                print("Agent-" + str(self.ID) + ": Has goals " + str(self.plan["target_pos"]))
        
        # ensure the plan is GO_TO, when target_pos is given
        if self.plan["target_pos"] and self.plan["status"] == Plan.RANDOM:
            self.plan["status"] == Plan.GO_TO
        
        # patience management
        if self.plan["patience"] == None:
            
            # ensure, agent cannot wait indefinetly without given patience
            if self.plan["status"] == Plan.WAIT:
                self.reset_plan()
                return
        
        # reduce patience
        elif self.plan["patience"] > 0:
            self.plan["patience"] -= 1
        
        # reset plan, upon not having goals or no patience
        elif self.plan["patience"] <= 0 or not self.plan["target_pos"]:
            self.reset_plan()
    
    def reset_plan(self):
        """Sets the AI-agent's plan back to randomly moving"""
        self.plan["patience"] = None
        self.plan["status"] = Plan.RANDOM
        self.plan["target_pos"] = []
    
    def update_knowledge(self):
        """Updates the agent's knowledge base on pit/wumpus locations. Should be called every turn"""
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
                        print("Agent-" + str(self.ID) + ": Removing assumption " + str(assumptions[perception]) + " at location " + str((row,col)))
                    self.knowledge[row][col]["state"].remove(assumptions[perception])
        
           
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
     
    def guess_wumpus(self) -> list:
        """
        Base logic for guessing large wumpi positions based on the knowledge grid. Returns a list of coordinates e.g. [(3,4), (0,5), ...]
        """
        return [
                (row, col)
                for row in range(len(self.knowledge))
                for col in range(len(self.knowledge))
                if State.L_WUMPUS in self.knowledge[row][col]["state"]
            ]
           
    def accept_message(self):
        """
        Processes a message and updates the agent's plan accordingly. Assumes, that each message is for informing a wumpus location in the following format: 'w(x,y) p(x,y) s(x,y,z)'
        - currently only works with a single message provided by the environment, so it cannot choose a specific message itself
        """
        # choose random message from another agent, if nothing to do and arrows available
        # self.messages.pop(self.ID)
        if (not self.messages
            or not self.plan["status"] == Plan.RANDOM
            or self.arrows <= 0 ): 
            return
        # chosen_message = random.choice([message for message in self.messages.values() if message])
        
        # input string for testing
        # input_string = "w(1,2) p(3,4) s(1,2,3)"
        if self.debug:
            print("Agent-" + str(self.ID) + ": Trying to accept a random message " + str(self.messages))
        
        # parse the message string
        pattern = r"(\w)\(([^)]+)\)"
        matches = findall(pattern, self.messages)
        
        
        # matches = findall(pattern, input_string)
        parsed_data = {key: tuple(map(int, value.split(','))) for key, value in matches}
        
        w = parsed_data['w']
        # p = parsed_data['p']
        s = parsed_data['s']
        
        # set up the next plan
        self.plan["status"] = Plan.GO_TO
        self.plan["patience"] = s[2] # shoot wumpus after informed amount of moves, otherwise cancel plan
        self.plan["target_pos"].append([s[0], s[1]]) # go to the senders shooting position
        self.plan["shoot_pos"].append((w[0], w[1])) # shoot at informed position
        
        if self.debug:
            print("Agent-" + str(self.ID) + ": Successfully acknowledged a message and updated its plan to killing a wumpus at " + str(([w[0], w[1]])))
            
            
     
    def shoot(self):
        if self.debug:
            print(f"Agent-{self.ID}: Has targets {self.plan["shoot_pos"]}")
        # shooting, if locations were calculated or informed via message (small wumpi work aswell) 
        if (self.arrows <= 0
            or self.plan["patience"] and self.plan["patience"] > 0):
            return None
        
        # if self.debug:
        #     print("Agent-" + str(self.ID) + ": Has enough arrows, position at " + str(self.position))
            
        wumpi = get_neighbors(self.knowledge, self.position[0], self.position[1], consider_obstacles=False)
        # if self.debug:
        #     print("Agent-" + str(self.ID) + ": Neighbors at " + str(wumpi))
        wumpi = [
            (wumpus[0], wumpus[1])
            for wumpus in wumpi
            if (wumpus[0], wumpus[1]) in self.plan["shoot_pos"] or self.knowledge[wumpus[0]][wumpus[1]]["state"] == [State.S_WUMPUS]
        ]
        if not wumpi:
            return None
        
        if self.debug:
            print("Agent-" + str(self.ID) + ": Found wumpi to shoot at " + str(wumpi))
        
        # assume, agent may have killed a wumpus and made it safe
        if State.S_WUMPUS in self.knowledge[wumpi[0][0]][wumpi[0][1]]["state"]:
            self.knowledge[wumpi[0][0]][wumpi[0][1]]["state"].remove(State.S_WUMPUS)
            append_unique(self.knowledge[wumpi[0][0]][wumpi[0][1]]["blocks"], State.S_WUMPUS)
        # if there are no assumptions anymore, claim safety
        if not self.knowledge[wumpi[0][0]][wumpi[0][1]]["state"]:
            append_unique(self.knowledge[wumpi[0][0]][wumpi[0][1]]["state"], State.SAFE)
        
        # plan to go to the shot position and collect gold
        # append_unique((self.plan["target_pos"]), wumpi[0])
        
        # update wumpi guesses and return shot direction
        if wumpi[0] in self.plan["shoot_pos"]:
            self.plan["shoot_pos"].remove(wumpi[0])
            self.reset_wumpi_guess()
            if self.debug:
                print(f"Agent-{self.ID}: Updated targets {self.plan["shoot_pos"]}")
                self.print_knowledge()
        direction = convert_to_direction(self.position, wumpi[0])
        if self.debug:
            print("Agent-" + str(self.ID) + ": Shot an arrow in direction " + direction + " at " + str(wumpi[0]))
        return direction
    
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
        self.accept_message() # potentially accept a message to kill wumpi
        self.update_knowledge()
        self.update_plan()
        status = self.plan["status"]
        
        if self.debug:
            self.print_knowledge()
        
        # random exploring
        if status == Plan.RANDOM:
            safe_moves = self.select_safe_moves()
            # if not safe_moves:
            #     return "up" # emergency case, when no move is safe (Note: should already be handled by select_safe_moves())
            next_move = random.choice(safe_moves)
        
        # stand still
        elif status == Plan.WAIT:
            next_move = None
        
        # go to a specific field or unexplored territory
        elif status == Plan.GO_TO or status == Plan.EXPLORE:
            path = a_star_search(self.knowledge, (self.position[0], self.position[1]), (self.plan["target_pos"][0][0],self.plan["target_pos"][0][1]), chance=self.risk_aversion)
            if self.debug:
                print("Agent-" + str(self.ID) + ": Calculated a path to goal " + str(path))
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
        # don't send messages, when you've already planned something
        if (not self.plan["status"] == Plan.RANDOM
            or random.randint(1, 10) >= 9): # regulate amount of messages for less overlapping
            return []
        
        content = []
        three_tuple = []
        position = (self.position[0], self.position[1])
        
        # check out all large wumpi
        wumpi = self.guess_wumpus()
        if self.debug:
            print("Agent-" + str(self.ID) + ": Guessed large wumpi at " + str(wumpi))
        
        if not wumpi:
            return []
        
        shoot_info = [] # used for format (x,y,path_len)
        for i in range(len(wumpi)):
            target = random.choice(get_neighbors(self.knowledge, wumpi[i][0], wumpi[i][1], consider_obstacles=True)) # safe field adjacent to wumpus, the sender aims to go to
            path = a_star_search(self.knowledge, position, (target[0], target[1]), chance=self.risk_aversion)
            shoot_info.append((target[0], target[1], len(path) + GUESS_PADDING if path else GUESS_PADDING))
        
        # create possible messages with wumpus locations and when the sender shoots
        for i in range(len(wumpi)):
            for x,y in wumpi:
                three_tuple.append([(x,y), position, shoot_info[i]])
        
        # choose and send a random message, inform-performative-only
        three_tuple_chosen = random.choice(three_tuple)
        messages = ["",f"w({three_tuple_chosen[0][0]},{three_tuple_chosen[0][1]}) p({three_tuple_chosen[1][0]},{three_tuple_chosen[1][1]}) s({three_tuple_chosen[2][0]},{three_tuple_chosen[2][1]},{three_tuple_chosen[2][2]})"]
        message_chosen = random.choice(messages)
        if message_chosen == "":
            return content
        content.append("inform")
        content.append(message_chosen)

        # assume you can commit to your plan
        self.plan["status"] = Plan.GO_TO
        self.plan["patience"] = three_tuple_chosen[2][2] # shoot wumpus after informed amount of moves, otherwise cancel plan
        self.plan["target_pos"].append([three_tuple_chosen[2][0], three_tuple_chosen[2][1]]) # go to the senders shooting position
        self.plan["shoot_pos"].append((three_tuple_chosen[0][0], three_tuple_chosen[0][1])) # shoot at informed position

        if self.debug:
            print("Agent-" + str(self.ID) + ": Successfully sent a message and commits to killing a wumpus at " + str(([three_tuple_chosen[0][0], three_tuple_chosen[0][1]])))

        return content

    def reset_wumpi_guess(self):
        """
        Removes all large wumpi from the knowledge base. Can be useful to avoid unnecessary alternative guesses after killing a large wumpus.
        """
        if self.debug:
            print(f"Agent-{self.ID}: Removing all large wumpus guesses")
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if State.L_WUMPUS in self.knowledge[row][col]["state"]:
                    self.knowledge[row][col]["state"].remove(State.L_WUMPUS)

    def reset(self):
        """
        Resets the agent's knowledge, plan, perception and life-state. Necessary upon starting the next game. Should be called from the environment.
        """
        # Reset knowledge
        self.knowledge = [[{
                            "state": [], # assumes, that a field could have this state
                            "blocks": [] # assumes, that a field 100% cannot have this state
                            } for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # start randomly exploring
        self.plan = {
            "status": Plan.RANDOM,
            "patience": None, # optional int: agent follows a plan for a set number of actions, before resetting to "status": Plan.RANDOM
            "target_pos": [], # optional [[int,int], ...]: when "status": Plan.GO_TO the agent should go to specified position
            "shoot_pos": [] # optional [[int,int]]: upon reaching a target_pos, shoot these coordinates (requires convertion to direction)
        }
        self.perceptions = None
        self.status = Status.alive

    def buy_arrows(self):
        budget = self.gold
        arrows = 0
        while arrows <= MAX_ARROWS and budget >= ARROW_PRICE:
            arrows += 1
            budget -= ARROW_PRICE
        return arrows

class RightAgent(AIAgent):
    """Agent that moves only right and ignores all plans."""
    
    def move(self):
        """Moves right only"""
        return "right"
    
    def buy_arrows(self):
        return 100
    
    def shoot(self):
        # print(self.perceptions)
        if self.perceptions:
            if Perception.SMELLY in self.perceptions:
                return "up"
        return None
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        # TODO: implement the meeting method
        pass
    
    def meeting_result(self, other_agent, result):
        pass

    def radio(self):
        content = []
        three_tuple = [[(1,2), (2,1), (3,2,9)], [(8,4), (3,1), (3,7,5)], [(3,7), (4,1), (4,7,5)]]
        three_tuple_chosen = random.choice(three_tuple)
        messages = ["",f"w({three_tuple_chosen[0][0]},{three_tuple_chosen[0][1]}) p({three_tuple_chosen[1][0]},{three_tuple_chosen[1][1]}) s({three_tuple_chosen[2][0]},{three_tuple_chosen[2][1]},{three_tuple_chosen[2][2]})"]
        message_chosen = random.choice(messages)
        if message_chosen == "":
            return content
        content.append("inform")
        content.append(message_chosen)

        return content
    
       
class RandomAgent(AIAgent):
    """Agent that moves randomly."""
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        # TODO: implement the meeting method
        pass
    
    def meeting_result(self, other_agent, result):
        pass

    # def radio(self):
    #     content = []
    #     three_tuple = [[(1,2), (2,1), (3,2,9)], [(8,4), (3,1), (3,7,5)], [(3,7), (4,1), (4,7,5)]]
    #     three_tuple_chosen = random.choice(three_tuple)
    #     messages = ["",f"w({three_tuple_chosen[0][0]},{three_tuple_chosen[0][1]}) p({three_tuple_chosen[1][0]},{three_tuple_chosen[1][1]}) s({three_tuple_chosen[2][0]},{three_tuple_chosen[2][1]},{three_tuple_chosen[2][2]})"]
    #     message_chosen = random.choice(messages)
    #     if message_chosen == "":
    #         return content
    #     content.append("inform")
    #     content.append(message_chosen)

    #     return content

class RandomBadAgent(AIAgent):
    """
    Agent that moves randomly.
    - will always rob in meetings
    """
    def buy_arrows(self):
        return 0
    def shoot(self):
        pass
    
    def conversation(self):
        pass
    
    def meeting(self, agent):
        return "rob"
    
    def meeting_result(self, other_agent, result):
        pass

    def radio(self):
        content = []
        three_tuple = [[(1,2), (2,1), (3,2,9)], [(8,4), (3,1), (3,7,5)], [(3,7), (4,1), (4,7,5)]]
        three_tuple_chosen = random.choice(three_tuple)
        messages = ["",f"w({three_tuple_chosen[0][0]},{three_tuple_chosen[0][1]}) p({three_tuple_chosen[1][0]},{three_tuple_chosen[1][1]}) s({three_tuple_chosen[2][0]},{three_tuple_chosen[2][1]},{three_tuple_chosen[2][2]})"]
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
        self.last_meeting_results = {}  # Dictionary to store results
    
    def buy_arrows(self):
        return 0
    def conversation(self):
        pass
        
    def shoot(self):
        pass

    def meeting(self, agent):
        """
        Handles a meeting with another agent using the Tit for Tat strategy.
        If the last interaction with the agent was cooperative, cooperate again.
        If the last interaction was adversarial, retaliate by robbing.
        """
        # Get the last meeting result with the other agent, or default to 'cooperate' if none exists
        result = self.last_meeting_results.get(agent.ID, "cooperate")  # Default to 'cooperate'

        return result

    def meeting_result(self, other_agent, result):
        """
        Store the result of the meeting with another agent.
        This allows the agent to decide the strategy in the next meeting.
        """
        self.last_meeting_results[other_agent.ID] = result

# defensive agent who collects gold and ist defensive against robbing
class DefensiveAgent(AIAgent):

    def meeting(self, agent):
        # Defensive behavior in meetings
        if self.armor > 0:
            return "nothing"  # Use armor to block robbing
        else:
            return "rob"  # Attempt to rob back if no armor is left
        
    def meeting_result(self, other_agent, result):
        pass
    
    def shoot(self):
        return None

    def buy_arrows(self):
        return 0
    def conversation(self):
        pass

class AggressiveAgent:
    def move(self):
        for agent_id, agent_position in self.opinions.items():
            if agent_position not in self.target_positions:
                self.target_positions.append(agent_position)
        
        if self.target_positions:
            closest_target = min(
                self.target_positions,
                key=lambda position: abs(position[0] - self.current_position[0]) + abs(position[1] - self.current_position[1])
            )
            self.plan = {"Status": Plan.GO_TO, "Target Position": closest_target}
            planned_path = a_star_search(self.knowledge, tuple(self.current_position), closest_target)
            if planned_path:
                return convert_to_direction(self.current_position, planned_path[1])
            
        safe_directions = self.select_safe_moves()
        return random.choice(safe_directions) if safe_directions else None

    def meeting(self, agent):
        return "rob"
    
    def meeting_result(self, other_agent, result):
        if result == "failed":
            self.target_agents.remove(other_agent.position)
        pass
    
    def shoot(self):
        return None
    
    def radio(self):
        return []




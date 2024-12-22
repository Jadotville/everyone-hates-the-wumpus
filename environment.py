import copy

import agent
from enums import State, Perception, Status # for storing additional information in a grid's field
from random import randint, shuffle # for randomized world generation
from utils import get_neighbors, append_unique, manhattan
import matplotlib.pyplot as plt
import numpy as np


class Game():
    ''' p1 : [n, message] => in n moves the player can make a radio again, when message != "" -> the player made this radio last move ''' # TODO Maybe saving all radio calls
    radio_possible = {}
    killed_wumpi = 0
    
    def __init__(self, agents, grid_properties, game_properties, prints=True):
        """
        - executes the simulations
        - assigns the agents their IDs and setting their gold to 0
        """
        if not agents:
            raise ValueError("No agents provided")
        else:
            for i in range(len(agents)):
                agents[i].ID = "p" + str(i + 1)
                agents[i].gold = 0
                agents[i].arrows = grid_properties["amount_arrows_start"]
                self.radio_possible["p" + str(i+1)] = [0, ""]

        prints = game_properties["prints"]
        
        gold_progress = []
        
        # executes the simulations
        for _ in range(game_properties["num_games"]):
            gold_progress.append(self.simulate(agents, grid_properties, prints))
        
        if game_properties["plot"]:
            self.plot_gold_evolution(gold_progress, agents)


    def plot_gold_evolution(self, gold_evolution, agents):
        gold_evolution = np.array(gold_evolution)
        gold_evolution = np.transpose(gold_evolution)
        x = list(range(1, gold_evolution.shape[1] + 1))
        for i in range(len(gold_evolution)):
            plt.plot(x, gold_evolution[i], label=type(agents[i]).__name__)

        plt.xlabel('Games')
        plt.ylabel('Gold Amount')
        plt.title('Evolution of Gold Amounts')
        plt.legend()
        plt.show()
            
    def print_grid(self, grid):
        """Display the grid with all agents, pits, wumpi, gold and items"""
        grid_print = []
        i = 0
        for row in grid:
            grid_print.append([])
            for field in row:
                if field["agents"]:
                    string_all_agents = ""
                    for agent in field["agents"]:
                        string_all_agents += agent.ID + " " if len(agent.ID) > 1 else agent.ID
                    string_all_agents =string_all_agents.strip()
                    grid_print[i].append(string_all_agents)
                elif field["state"] is not None:
                    grid_print[i].append(field["state"].value[0])
                else:
                    grid_print[i].append("_")
            i += 1
        for row in grid_print:
            print(row)

    def print_positions(self, agents):
        """prints the positions of the agents # element-format: (int,int)"""
        positions = "" # element-format: dict {"position": (int,int), "size": string}
        for agent in agents:
            positions += agent.ID + ": " + (str(agent.position) if agent.status == Status.alive else "dead") + " " # element-format: dict {"position": (int,int), "amount": int}
        return(positions)
        
    def print_gold(self, agents):
        """prints the gold of the agents"""
        gold = ""
        for agent in agents:
            gold += agent.ID + ": " + str(agent.gold) + " "
        return(gold)


    def is_game_over(self, agents, num_wumpi):	
        """checks if the game is over"""
        living_agents = False
        for agent in agents:
            if agent.status == Status.alive:
                living_agents = True
                break
            
        if num_wumpi != 0 and num_wumpi - self.killed_wumpi <=0:
            return True
        
        return not living_agents
        
    def simulate(self, agents, grid_properties, prints):
        """
        simulates the game given the agents, grid properties
        """

        self.killed_wumpi = 0
        
        # creates the initial grid on which the agents are placed after every move
        grid = self.grid_preperation(agents, grid_properties)
        
        # prints the initial grid
        if prints:
            print(" initial Grid:")
            self.print_grid(grid)


        max_number_of_moves = grid_properties["size"] * grid_properties["size"] * 3

        for agent in agents:
            purchase = agent.buy_arrows()
            if purchase <= 0:
                continue
            
            if agent.gold >= purchase * 2:
                agent.arrows += purchase
                agent.gold -= purchase * 2
            else:
                agent.arrows += agent.gold // grid_properties["arrow_price"]
                agent.gold -= (agent.gold // grid_properties["arrow_price"]) * grid_properties["arrow_price"]
        

        #runs the game loop
        move_counter = 0
        
        num_wumpi = grid_properties["num_s_wumpi"] + grid_properties["num_l_wumpi"]
        
        while not self.is_game_over(agents, num_wumpi) and max_number_of_moves > move_counter:            
            if prints:
                print("\nMove: ", move_counter)
                print(self.radio_possible)
                print("armor")
                for agent in agents:
                    print(agent.ID + " " + str(agent.armor))

            # get all message with player name
            messages = {}
            for key,message in self.radio_possible.items():
                if self.radio_possible[key][1] == '':
                    messages[key] = ''
                else:
                    messages[key] = self.radio_possible[key][1][1]
                    if prints:
                        print(f"{messages[key]} = " + str(messages[key]))

            shots = []    
            
            
            for agent in agents:
                try:
                    grid[agent.position[0]][agent.position[1]]["agents"] = []
                except IndexError:
                    agent.status = Status.dead
                    continue
                
                # agent perceives and then moves
                agent.perceptions = copy.copy(grid[agent.position[0]][agent.position[1]]["perceptions"])
                
                agent.messages = messages         
                    
             
            for agent in agents:
                if agent.status == Status.dead:
                    continue
                shot = agent.shoot()
                if shot and agent.arrows > 0:
                    agent.arrows -= 1
                    if shot == "up":
                        shots.append([agent.position[0]-1, agent.position[1]])
                    elif shot == "down":
                        shots.append([agent.position[0]+1, agent.position[1]])
                    elif shot == "left":
                        shots.append([agent.position[0], agent.position[1]-1])
                    else:
                        shots.append([agent.position[0], agent.position[1]+1])
            if prints:
                print("Shots: ", shots)
          
            for agent in agents:
                
                # print("Game: Agent " + agent.ID + " should perceive " + str(agent.perceptions))
                move=agent.move()
                
                if move== "up":
                    agent.position[0]-=1
                elif move== "down":
                    agent.position[0]+=1
                elif move== "left":
                    agent.position[1]-=1
                elif move== "right":
                    agent.position[1]+=1
                    
            move_counter += 1
            
            
            # updates the agent positions on the grid
            self.update_grid(grid, agents, shots, prints, grid_properties["meeting_rewards"])

            for agent in agents:
                if agent.status == Status.dead:
                    continue
                field = grid[agent.position[0]][agent.position[1]]
                if field["state"] == State.S_GOLD:
                    for every_agent in field["agents"]:
                        every_agent.gold += grid_properties["small_gold"]//len(field["agents"])
                    field["state"] = None
                elif field["state"] == State.L_GOLD:
                    for every_agent in field["agents"]:
                        every_agent.gold += grid_properties["large_gold"]//len(field["agents"])
                    field["state"] = None

            # radio
            for agent in agents:
                self.radio_possible[agent.ID][1] = ""
                if self.radio_possible[agent.ID][0] == 0:
                    radio_call = agent.radio()
                    if radio_call is []:
                        pass
                    elif len(radio_call) == 2:
                        if radio_call[0] == "inform":
                            self.radio_possible[agent.ID][1] = radio_call
                            self.radio_possible[agent.ID][0] = 5
                    else:
                        # TODO: errorhandling
                        pass
                else:
                    self.radio_possible[agent.ID][0] -= 1

            # prints the grid
            if prints:
                self.print_grid(grid)
                print("Gold: ", self.print_gold(agents))
                print("Positions: ", self.print_positions(agents))

        # final gold distribution
        gold = []
        for agent in agents:
            gold.append(agent.gold)

        return gold


    def grid_preperation(self, agents, grid_properties):
        """
        - creates a grid given the grid properties
        - places the agents in the grid by giving them their positions
        """

        # creates a grid of size n x n
        size = grid_properties["size"]

        # initializes the grid with empty fields
        grid = [[{"agents": [], 
                  "state": None, # plz use State.x: none | pit | wumpus | gold | armor
                  "perceptions": [] # plz use Perception.x: breeze | smelly
                  } for _ in range(size)] for _ in range(size)]
        

        # initializes the agents
        # gives agents their positions and grid size
        # stores agents in the grid
        if agents:
            agents[0].position = [0, 0]
            agents[0].grid_size = size
            grid[0][0]["agents"].append(agents[0])
        if len(agents) > 1:
            agents[1].position = [0, size - 1]
            agents[1].grid_size = size
            grid[0][size - 1]["agents"].append(agents[1])
        if len(agents) > 2:
            agents[2].position = [size - 1, 0]
            agents[2].grid_size = size
            grid[size - 1][0]["agents"].append(agents[2])
        if len(agents) > 3:
            agents[3].position = [size - 1, size - 1]
            agents[3].grid_size = size
            grid[size - 1][ size - 1]["agents"].append(agents[3])
            

        # Order matters (probably): place pits -> wumpi -> objects
        grid = self.spawn_pits(agents, grid, grid_properties)
        grid = self.spawn_wumpi(agents, grid, grid_properties)
        grid = self.spawn_objects(agents, grid, grid_properties)
        self.spawn_perceptions(grid) # untested, comment this line out, if something breaks

        return grid
    
    
    def spawn_pits(self, agents, grid, grid_properties, spawn_dist=2):
        """
        New implementation for spawning State.PITs specifically. Randomly fills fields, while skipping agents' positions. 
        - Plz spawn in the following order: spawn_pits() -> spawn_wumpi() -> spawn_objects()
        - keep the amount of pits lower than a third of the field
        
        :param int spawn_dist: generates wumpi atleast x fields away from Agents' spawn
        """
        # Extract properties for easier access
        size = grid_properties["size"]
        num_pits = grid_properties["num_pits"]
        agent_positions = []
        for agent in agents:
            agent_positions.append((agent.position[0], agent.position[1]))
        
        # Create a flat list of grid positions, exclude positions near agents
        all_positions = [(row, col) for row in range(size) for col in range(size)]
        filtered_positions = [
            pos_a for pos_a in all_positions
            if all(manhattan(pos_a, pos_b) >= spawn_dist for pos_b in agent_positions)
        ]
        
        attempts = 0
        all_accessible = False # grid hasn't been checked for full acessibility
        while not all_accessible:
            attempts += 1
            # Shuffle positions and select a subset for object placement
            shuffle(filtered_positions)
            selected_positions = filtered_positions[:num_pits]

            grid_copy = copy.deepcopy(grid)
            
            # Create a list of objects to place
            objects = ([State.PIT] * num_pits)

            # Place objects in the selected grid positions
            for pos, obj in zip(selected_positions, objects):
                row, col = pos
                grid_copy[row][col]["state"] = obj
            
            # Validate pit placement, otherwise reset grid's copy for reshuffling
            # print(f"Grid-Generation: flood-fill found {self.flood_fill(grid_copy, 0, 0)} fields") # for debugging purposes
            accessible_fields = self.flood_fill(grid_copy, 0, 0)
            target_number = size * size - num_pits
            if accessible_fields >= target_number:
                all_accessible = True
                grid = grid_copy
            else:
                print(f"Attempt {attempts}: Grid not fully accessible, only {accessible_fields} out of {target_number}. Reshuffling.") # for debugging only
        
        return grid
    
    def spawn_objects(self, agents, grid, grid_properties):
        """
        New Implementation: Places gold, armor and optionally more in the grid. 
        - Plz spawn in the following order: spawn_pits() -> spawn_wumpi() -> spawn_objects()
        """
        # Extract properties for easier access
        size = grid_properties["size"]
        num_armor = grid_properties["num_armor"]
        num_swords = grid_properties['num_swords']
        num_small_gold = grid_properties["num_small_gold"]
        num_large_gold = grid_properties["num_large_gold"]
        agent_positions = []
        for agent in agents:
            agent_positions.append((agent.position[0], agent.position[1]))
        
        # Create a flat list of grid positions
        all_positions = [(row, col) for row in range(size) for col in range(size)]

        # remove fields with and pits and wumpi
        for row, col in all_positions:
            if grid[row][col]["state"] != None:
                all_positions.remove((row,col))
                
        # Total number of objects to place
        total_objects = num_small_gold + num_large_gold + num_armor + num_swords # + num_s_wumpi + num_l_wumpi
        
        # Shuffle positions and select a subset for object placement
        shuffle(all_positions)
        selected_positions = all_positions[:total_objects]

        # Create a list of objects to place
        objects = ([State.S_GOLD] * num_small_gold + 
                   [State.L_GOLD] * num_large_gold +
                   [State.ARMOR] * num_armor +
                   [State.SWORD] * num_swords)
        
        # Shuffle the objects
        shuffle(objects)

        # Place objects in the selected grid positions
        for pos, obj in zip(selected_positions, objects):
            row, col = pos
            grid[row][col]["state"] = obj
        
        return grid
    
    def spawn_wumpi(self, agents, grid, grid_properties, spawn_dist=2):
        """
        New Implementation: Places just wumpi in the grid. 
        - Plz spawn in the following order: spawn_pits() -> spawn_wumpi() -> spawn_objects()
        
        :param int spawn_dist: generates wumpi atleast x fields away from Agents' spawn
        """
        # Extract properties for easier access
        size = grid_properties["size"]
        num_s_wumpi = grid_properties["num_s_wumpi"]
        num_l_wumpi = grid_properties["num_l_wumpi"]
        agent_positions = []
        for agent in agents:
            agent_positions.append((agent.position[0], agent.position[1]))
        
        # Create a flat list of grid positions, remove agent positions (no spawn-camping wumpi allowed lol)
        all_positions = [(row, col) for row in range(size) for col in range(size)]
        filtered_positions = [
            pos_a for pos_a in all_positions
            if all(manhattan(pos_a, pos_b) >= spawn_dist for pos_b in agent_positions)
        ]

        # remove fields with and pits
        for row, col in filtered_positions:
            if grid[row][col]["state"] != None:
                filtered_positions.remove((row,col))
                
        # Total number of objects to place
        total_objects = num_s_wumpi + num_l_wumpi
        
        # Shuffle positions and select a subset for object placement
        shuffle(filtered_positions)
        selected_positions = filtered_positions[:total_objects]

        # Create a list of objects to place
        objects = ([State.S_WUMPUS] * num_s_wumpi + 
                   [State.L_WUMPUS] * num_l_wumpi)
        
        # Shuffle the objects
        shuffle(objects)

        # Place objects in the selected grid positions
        for pos, obj in zip(selected_positions, objects):
            row, col = pos
            grid[row][col]["state"] = obj
        
        return grid
    
    def flood_fill(self, grid, start_row, start_col):
        """
        Calculate the number of accessible fields in the world's grid from a starting position.
        
        :param 2D-list grid: The world's grid, there have to be State.PITs
        :param int start_row: Starting row index
        :param int start_col: Starting column index
        
        """
        rows = len(grid)
        cols = len(grid[0])
        
        # Check if the starting position is valid
        if grid[start_row][start_col]["state"] == State.PIT:
            return 0 
        
        # Directions for moving in 4 cardinal directions (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # Stack for iterative flood-fill
        stack = [(start_row, start_col)]
        visited = set()  # To track visited cells
        accessible_count = 0
        
        while stack:
            row, col = stack.pop()
            
            # Skip if already visited or pit
            if (row, col) in visited:
                continue
            
            # Mark the field as visited
            visited.add((row, col))
            accessible_count += 1
            
            # Explore neighbors
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                # Check if the neighbor is within bounds and accessible
                if (0 <= new_row < rows and 
                    0 <= new_col < cols and 
                    grid[new_row][new_col]["state"] != State.PIT and 
                    (new_row, new_col) not in visited):
                    stack.append((new_row, new_col))
        
        return accessible_count
  
    def spawn_perceptions(self, grid):
        """UNTESTED: Places perceptions for pits, small/large wumpi in neighboring fields in the grid"""
        # associate Items with Perceptions to be placed
        perceptions = {
            State.PIT: Perception.BREEZE,
            State.S_WUMPUS: Perception.SMELLY,
            State.L_WUMPUS: Perception.VERY_SMELLY
        }
        size = len(grid)
        
        for row in range(size):
            for col in range(size):
                state = grid[row][col]['state']
                
                if state not in perceptions.keys():
                    continue
                
                # place perceptions in adjacent fields
                perception = perceptions[state]
                for n_row, n_col in get_neighbors(grid, row, col, consider_obstacles=False):
                    append_unique(grid[n_row][n_col]['perceptions'], perception)
        
    def update_grid(self, grid, agents, shots, prints, meeting_rewards):
        
        for pos in shots:
            if grid[pos[0]][pos[1]]["state"] == State.S_WUMPUS:
                grid[pos[0]][pos[1]]["state"] = State.S_GOLD
                self.killed_wumpi += 1
                
            if grid[pos[0]][pos[1]]["state"] == State.L_WUMPUS and shots.count(pos) > 1:
                grid[pos[0]][pos[1]]["state"] = State.L_GOLD
                self.killed_wumpi += 1
            
        
        for agent in agents:
            
            if agent.status == Status.dead:
                continue
            
            if agent.position[0] < 0 or agent.position[0] >= len(grid):
                agent.status = Status.dead
                continue
            
            if agent.position[1] < 0 or agent.position[1] >= len(grid):
                agent.status = Status.dead
                continue
            
            if grid[agent.position[0]][agent.position[1]]["state"] == State.PIT:
                agent.status = Status.dead
                continue    
                    
            if grid[agent.position[0]][agent.position[1]]["state"] == State.S_WUMPUS:
                agent.status = Status.dead
                continue
            
            if grid[agent.position[0]][agent.position[1]]["state"] == State.L_WUMPUS:
                agent.status = Status.dead
                continue
            if grid[agent.position[0]][agent.position[1]]["state"] == State.ARMOR:
                agent.armor += 1
                grid[agent.position[0]][agent.position[1]]["state"] = None
            
            # agent.perceptions = copy.deepcopy(grid[agent.position[0]][agent.position[1]]["perceptions"])
            # print("Game: Agent " + agent.ID + " should perceive " + agent.perceptions)
            for other_agent in grid[agent.position[0]][agent.position[1]]["agents"]:
                self.meeting(agent, other_agent, prints, meeting_rewards)

            grid[agent.position[0]][agent.position[1]]["agents"].append(agent)
            self.spawn_perceptions(grid) # in case any wumpi got killed, removes their perceptions (alternatively do this specifically after killing a wumpus)
        

             
    def meeting(self, agent1, agent2, prints, rm):
        """
        - defines the result of a meeting between two agents
        """
        if prints:
            print("meeting: " + agent1.ID + " und " +agent2.ID)
        action_agent1 = agent1.meeting(agent2)
        action_agent2 = agent2.meeting(agent1)

        # function for returning list with indices for the reward matrix as specified in the simulation.py
        def get_meeting_reward_pos(action_agent1, action_agent2, agent1, agent2):
            meeting_reward_pos = []
            if action_agent1 == "rob":
                if action_agent2 == "rob":
                    meeting_reward_pos.append(0)
                else:
                    meeting_reward_pos.append(1)
            else:
                if action_agent2 == "rob":
                    meeting_reward_pos.append(2)
                else:
                    meeting_reward_pos.append(3)

            if agent1.armor > 0:
                meeting_reward_pos.append(0)
                if agent2.armor > 0:
                    meeting_reward_pos.append(0)
                else:
                    meeting_reward_pos.append(1)
            else:
                meeting_reward_pos.append(1)
                if agent2.armor > 0:
                    meeting_reward_pos.append(0)
                else:
                    meeting_reward_pos.append(1)
            return meeting_reward_pos


        meeting_reward_pos_1 = get_meeting_reward_pos(action_agent1, action_agent2, agent1, agent2)
        meeting_reward_pos_2 = get_meeting_reward_pos(action_agent2, action_agent1, agent2, agent1)

        # decreasing or increasing the gold of the agents
        agent1.gold += rm[meeting_reward_pos_1[0]][meeting_reward_pos_1[1]][meeting_reward_pos_1[2]]
        agent2.gold += rm[meeting_reward_pos_2[0]][meeting_reward_pos_2[1]][meeting_reward_pos_2[2]]

        # decreasing the armor of the agents
        if (meeting_reward_pos_1[0] == 0 or meeting_reward_pos_1[0] == 2) and agent1.armor > 0:
            if prints:
                print("looses armor " + agent1.ID)
            agent1.armor -= 1
        if (meeting_reward_pos_2[0] == 0 or meeting_reward_pos_2[0] == 2) and agent2.armor > 0:
            if prints:
                print("looses armor " + agent2.ID)
            agent2.armor -= 1
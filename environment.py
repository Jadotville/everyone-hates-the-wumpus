import copy
from enums import State, Perception # for storing additional information in a grid's field
from random import randint, shuffle # for randomized world generation
from utils import near_objects

class Game():
    def __init__(self, agents, grid_properties, game_properties, prints=True):
        """
        - executes the simulations
        - assigns the agents their IDs and setting their gold to 0
        """
        if not agents:
            # TODO: errorhandling
            pass
        else:
            for i in range(len(agents)):
                agents[i].ID = "p" + str(i + 1)
                agents[i].gold = 0
        
        # executes the simulations
        for _ in range(game_properties["num_games"]):
            self.simulate(agents, grid_properties, prints)

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
                    grid_print[i].append("0")
            i += 1
        for row in grid_print:
            print(row)

    def print_positions(self, agents):
        """prints the positions of the agents # element-format: (int,int)"""
        positions = "" # element-format: dict {"position": (int,int), "size": string}
        for agent in agents:
            positions += agent.ID + ": " + str(agent.position) + " " # element-format: dict {"position": (int,int), "amount": int}
        print(positions)
         # element-format: dict {"position": (int,int), "name": string}
        
    def print_gold(self, agents):
        """prints the gold of the agents"""
        gold = ""
        for agent in agents:
            gold += agent.ID + ": " + str(agent.gold) + " "
        print(gold)


    def simulate(self, agents, grid_properties, prints):
        """
        simulates the game given the agents, grid properties
        """

        # creates the initial grid on which the agents are placed after every move
        grid = self.grid_preperation(agents, grid_properties)
        
        # prints the initial grid without agents
        if prints:
            print(" initial Grid without agents:")
            self.print_grid(grid)
            
        # places the agents on the grid
        self.update_grid(grid, agents)

        # prints the initial grid with agents
        if prints:
            print(" initial Grid with agents:")
            self.print_grid(grid)

        #runs the game loop
        # TODO: add break criteria
        for _ in range(1):              
            
            
            # every agent makes a move
            for agent in agents:
                grid[agent.position[0]][agent.position[1]]["agents"] = []
                action=agent.action()
                if action== "up":
                    agent.position[0]-=1
                elif action== "down":
                    agent.position[0]+=1
                elif action== "left":
                    agent.position[1]-=1
                elif action== "right":
                    agent.position[1]+=1
                agent.perceptions = copy.deepcopy(grid[agent.position[0]][agent.position[1]]["perceptions"])

            # updates the agent positions on the grid
            self.update_grid(grid, agents)

            # prints the grid
            if prints:
                print("Grid:")
                self.print_grid(grid)
                print("Gold:")
                self.print_gold(agents)
                print("Positions:")
                self.print_positions(agents)


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
                  "perceptions": [] # plz use Perception.x: breeze | stench
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
            

        # Order matters: place pits, then objects
        grid = self.spawn_pits(agents, grid, grid_properties)
        grid = self.spawn_objects(grid, grid_properties)

        return grid


    def generate_world(self, agents, grid, grid_properties):
        """
        !!!DISCLAIMER: This wasn't tested yet and the algorithm is stupid!!! \\
        Places in order: pits, wumpi, gold, armor
        """
        # extract properties for easier access
        size = grid_properties["size"]
        num_pits = grid_properties["num_pits"]
        num_wumpi = grid_properties["num_wumpi"]
        num_gold = grid_properties["num_gold"]
        num_armor = grid_properties["num_armor"]
        
        # check, if world is too small for specified spawns
        num_total = num_pits + num_wumpi + num_gold + num_armor
        if num_total > size*size:
            print("Game-Error: Too many objects specified for the grid generation!")
        
        objects = [
            (State.PIT, num_pits), # spawn pits first, because it has the most spawn-restrictions (reachability to every non-pit field)
            (State.WUMPUS, num_wumpi),
            (State.GOLD, num_gold),
            (State.ARMOR, num_armor),
        ]
        # spawn objects in order of list
        for object, num_objects in range(objects):
            grid = self.spawn_object(agents, grid, object, num_objects)
        
        return grid
        
    
    def spawn_object(self, agents, grid, object, num_object):
        """
        !!!DISCLAIMER: This wasn't tested yet and the algorithm is stupid!!! \\
        Places specified object into a grid, avoiding agent fields
        
        :param list agents: non-empty list of all agents
        :param 2D-list grid: the world's grid
        :param enums.State object: objects to be placed into the grid
        :param int num_object: number of specified object to be placed, >=1
        """
        size = len(grid)
        
        # settings for ignoring fields
        if object == State.PIT:
            dist = 1
            excluded_fields = 12 # exclude agents' positions and adjacent fields
        else:
            dist = 0
            excluded_fields = 4 # exclude agents' positions
        
        # iterate over every field, while not enough objects placed
        while num_object > 0:
            for row in range(size):
                for col in range(size):
                    remaining_fields = size*size - excluded_fields
                    
                    # skip fields near agents
                    if near_objects((row, col), agents, dist):
                        continue
                    
                    # calculate probability
                    rng = randint(1, remaining_fields)
                    if num_object > 0 and rng == 1:
                        grid[row][col] = object
                        num_object -= 1
                        excluded_fields += 1 # ignore this field next
        
        return grid
    
    
    def spawn_pits(self, agents, grid, grid_properties):
        """
        New implementation for spawning State.PITs specifically. Randomly fills fields skipping agents' positions.
        - keep the amount of pits lower than a third of the field
        """
        # Extract properties for easier access
        size = grid_properties["size"]
        num_pits = grid_properties["num_pits"]
        agent_positions = []
        for agent in agents:
            agent_positions.append((agent.position[0], agent.position[1]))
        
        # Create a flat list of grid positions, exclude agent positions
        all_positions = [(row, col) for row in range(size) for col in range(size)]
        for pos in agent_positions:
            all_positions.remove(pos)
        
        attempts = 0
        all_accessible = False # grid hasn't been checked for full acessibility
        while not all_accessible:
            attempts += 1
            # Shuffle positions and select a subset for object placement
            shuffle(all_positions)
            selected_positions = all_positions[:num_pits]

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
    
    def spawn_objects(self, grid, grid_properties):
        """New Implementation: Places wumpi, gold, armor and optionally more in the grid."""
        # Extract properties for easier access
        size = grid_properties["size"]
        num_wumpi = grid_properties["num_wumpi"]
        num_gold = grid_properties["num_gold"]
        num_armor = grid_properties["num_armor"]

        # Total number of objects to place
        total_objects =  num_wumpi + num_gold + num_armor

        # Create a flat list of grid positions, remove fields with agents and pits
        all_positions = [(row, col) for row in range(size) for col in range(size)]
        for row, col in all_positions:
            if grid[row][col]["state"] != None:
                all_positions.remove((row,col))
        
        # Shuffle positions and select a subset for object placement
        shuffle(all_positions)
        selected_positions = all_positions[:total_objects]

        # Create a list of objects to place
        objects = ([State.WUMPUS] * num_wumpi + 
                [State.GOLD] * num_gold + 
                [State.ARMOR] * num_armor)
        
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
    
    
    def update_grid(self, grid, agents):
        """
        - copy the grid so no pointers are left: "grid_copy"
        """
        grid_copy = copy.deepcopy(grid)
        i = 0
        for agent in agents:
            
            if agent.state == 'dead':
                continue
            if agent.position[0] < 0 or agent.position[0] >= len(grid):
                agent.state = 'dead'
            elif agent.position[1] < 0 or agent.position[1] >= len(grid):
                agent.state = 'dead'
            else:
                if grid[agent.position[0]][agent.position[1]]["state"] == State.PIT:
                    agent.state = 'dead'
                    
                elif grid[agent.position[0]][agent.position[1]]["state"] == State.WUMPUS:
                    agent.state = 'dead'
                
                elif grid[agent.position[0]][agent.position[1]]["state"] == State.GOLD:
                    print(agent.gold)
                    agent.gold += 5
                    print(agent.gold)
                    print("Gold gefunden")
                    grid[agent.position[0]][agent.position[1]]["state"] = None

                
                for other_agent in grid[agent.position[0]][agent.position[1]]["agents"]:
                    self.meeting(agent, other_agent)
                grid[agent.position[0]][agent.position[1]]["agents"].append(agent)


    def meeting(self, agent1, agent2):
        """
        - defines the result of a meeting between two agents
        """
        print("meeting: " + agent1.ID + " und " +agent2.ID)
        action_agent1 = agent1.meeting(agent2)
        action_agent2 = agent2.meeting(agent1)
        if action_agent1 == "rob":
            if action_agent2 == "rob":
                # TODO: result?
                pass
            elif action_agent2 == "chat":
                # TODO: result?
                pass
            elif action_agent2 == "nothing":
                # TODO: result?
                pass
            else:
                # TODO: errorhandling
                pass
        elif action_agent1 == "chat":
            if action_agent2 == "rob":
                # TODO: result?
                pass
            elif action_agent2 == "chat":
                # TODO: result?
                pass
            elif action_agent2 == "nothing":
                # TODO: result?
                pass
            else:
                # TODO: errorhandling
                pass
        elif action_agent1 == "nothing":
            if action_agent2 == "rob":
                # TODO: result?
                pass
            elif action_agent2 == "chat":
                # TODO: result?
                pass
            elif action_agent2 == "nothing":
                # TODO: result?
                pass
            else:
                # TODO: errorhandling
                pass
        else:
            #TODO: errorhandling
            pass
            
            
            
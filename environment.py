import copy
from enums import State, Perception # for storing additional information in a grid's field
from random import randint # for randomized world generation
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
        for _ in range(10):              
            
            
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
            
            
        # TODO: place wumpi
        # example for placing wumpi
        grid[3][4]["state"] = State.WUMPUS
        
        # TODO: place pits
        # example for placing pits
        grid[3][2]["state"] = State.PIT

        # TODO: place gold
        # example for placing gold
        grid[2][3]["state"] = State.GOLD

        # TODO: place special items
        # example for placing special items
        grid[4][2]["state"] = State.ARMOR

        # place all objects
        self.generate_world(grid, grid_properties)

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
            
            
            
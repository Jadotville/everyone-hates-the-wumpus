import copy
from enums import State, Perception # for storing additional information in a grid's field

class Game():

    # prints the grid
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

    # prints the positions of the agents # element-format: (int,int)
    def print_positions(self, agents):
        positions = "" # element-format: dict {"position": (int,int), "size": string}
        for agent in agents:
            positions += agent.ID + ": " + str(agent.position) + " " # element-format: dict {"position": (int,int), "amount": int}
        print(positions)
         # element-format: dict {"position": (int,int), "name": string}
        
    # prints the gold of the agents
    def print_gold(self, agents):
        gold = ""
        for agent in agents:
            gold += agent.ID + ": " + str(agent.gold) + " "
        print(gold)
    
    
    # executes the simulations
    def __init__(self, agents, grid_properties, game_properties, prints=True):
        # assigns the agents their IDs and setting their gold to 0
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
        grid[3][4]["state"] = "wumpus"
        
        # TODO: place pits
        # example for placing pits
        grid[3][2]["state"] = "pit"

        # TODO: place gold
        # example for placing gold
        grid[2][3]["state"] = "gold"

        # TODO: place special items
        # example for placing special items
        grid[4][2]["state"] = "arrow"

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
            
            
            
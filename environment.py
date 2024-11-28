import copy
from enums import State # for storing additional information in a grid's field

class Game():

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
                        string_all_agents += agent + " " if len(agent) > 1 else agent
                    string_all_agents =string_all_agents.strip()
                    grid_print[i].append(string_all_agents)
                elif field["state"] is not None:
                    grid_print[i].append(field["state"].value[0])
                else:
                    grid_print[i].append("0")
            i += 1
        for row in grid_print:
            print(row)

    # primitive lists for iterating over specific objects faster
    pits = [] # element-format: (int,int)
    wumpi = [] # element-format: dict {"position": (int,int), "size": string}
    gold_position = [] # element-format: dict {"position": (int,int), "amount": int}
    items = [] # element-format: dict {"position": (int,int), "name": string}
    gold_amount_player = {}

    # executes the simulations
    def __init__(self, agents, grid_properties, game_properties, prints=True):
        if agents:
            agents[0].ID = 'p1'
        if len(agents) > 1:
            agents[1].ID = 'p2'
        if len(agents) > 2:
            agents[2].ID = 'p3'
        if len(agents) > 3:
            agents[3].ID = 'p4'
        # beginning: set every player.gold = 0
        for agent in agents:
            self.gold_amount_player[agent.ID] = 0
        for _ in range(game_properties["num_games"]):
            self.simulate(agents, grid_properties, prints)


    def simulate(self, agents, grid_properties, prints):
        """
        simulates the game given the agents, grid properties
        """

        # creates the initial grid on which the agents are placed after every move
        initial_grid = self.grid_preperation(agents, grid_properties)
        if prints:
            print(" initial Grid without agents:")
            self.print_grid(initial_grid)
        # places the agents on the grid
        grid = self.update_grid(initial_grid, agents)


        # prints the initial grid
        if prints:
            print(" initial Grid with agents:")
            self.print_grid(grid)


        #runs the game loop
        # TODO: add break criteria
        for _ in range(10):

            # every agent makes a move
            for agent in agents:
                action=agent.action()
                if action== "up":
                    agent.position[0]-=1
                elif action== "down":
                    agent.position[0]+=1
                elif action== "left":
                    agent.position[1]-=1
                elif action== "right":
                    agent.position[1]+=1

            # updates the agent positions on the grid
            grid = self.update_grid(initial_grid, agents)

            # prints the initial grid
            if prints:
                print("Grid:")
                self.print_grid(grid)
                print("Gold:", self.gold_amount_player)


    def grid_preperation(self, agents, grid_properties):
        """
        - creates a grid given the grid properties
        - places the agents in the grid by giving them their positions
        """

        # creates a grid of size n x n
        size = grid_properties["size"]

        grid = [[{"agents": [], "state": State.NONE} for _ in range(size)] for _ in range(size)]
        # "state"-values: "pit" | 
        

        # initializes the agents
        # gives agents their positions, grid size and ID
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
            
        self.wumpi = []
        # TODO: place wumpi

        self.pits = []
        # TODO: place pits

        self.gold_position = []

        self.items = []
        # TODO: place special items

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

                for wumpus in self.wumpi:
                    if wumpus.position == agent.position:
                        agent.state = 'dead'
                        break

                for pit in self.pits:
                    if pit.position == agent.position:
                        agent.state = 'dead'
                        break
                for gold in self.gold_position:
                    if gold == agent.position:
                        self.gold_amount_player[agent.ID] += 5
                        self.gold_position.remove(gold)
                        break



                for other_agent in agents:
                    if other_agent.ID == agent.ID:
                        continue
                    if other_agent.position == agent.position:
                        self.meeting(agent, other_agent)

                if grid_copy[agent.position[0]][agent.position[1]]["state"] == State.NONE:
                    grid_copy[agent.position[0]][agent.position[1]]["agents"].append(agent.ID)
                    # serach in the old grid 'grid' for the agent and remove this position in the copied grid: "copy_grid"
                    for row in grid:
                        for field in row:
                            if agent.ID in field["agents"]:
                                field["agents"].remove(agent.ID)
                                break
            i+=1
        return grid_copy


    def meeting(self, agent1, agent2):
        """
        - defines the result of a meeting between two agents
        """
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
            
            
            
class Game():   
    
    # primitive lists for iterating over specific objects faster
    pits = []   # element-format: dict {"x": int, "y": int}
    wumpi = []  # element-format: dict {"x": int, "y": int, "size": string}
    gold = []   # element-format: dict {"x": int, "y": int, "amount": int}
    items = []  # element-format: dict {"x": int, "y": int, "item": string}
    
    def __init__(self, agents, grid_properties, game_properties):
        """executes the simulations"""
        prints = game_properties["prints"]
        for _ in range(game_properties["num_games"]):
            self.simulate(agents, grid_properties, prints)


    def simulate(self, agents, grid_properties, prints):
        """simulates the game given the agents, grid properties"""
        
        # creates the initial grid on which the agents are placed after every move 
        initial_grid = self.grid_preperation(agents, grid_properties)
        
        # places the agents on the grid
        grid = self.update_grid(initial_grid, agents)
        
        # prints the initial grid
        if prints:
            print(" initial Grid with agents:")   
            for row in grid:
                print(row)               
        
        
        #runs the game loop
        # TODO: add break criteria
        for _ in range(10):
            
            # TODO: messages
            
            # TODO: actions
            
            # every agent makes a move
            for agent in agents:
                move = agent.move()
                if move == "up":
                    agent.position[0]-=1
                elif move == "down":
                    agent.position[0]+=1
                elif move == "left":
                    agent.position[1]-=1
                elif move == "right":
                    agent.position[1]+=1
            
            # updates the agent positions on the grid
            grid = self.update_grid(initial_grid, agents)
                    
            # prints the initial grid
            if prints:
                print("Grid:")   
                for row in grid:
                    print(row)   
   
   
    def grid_preperation(self, agents, grid_properties):
        """
        - creates a grid given the grid properties
        - places the agents in the grid by giving them their positions
        """
        
        # empty object for saving the state of a field
        empty_field = {
            "agents": [],   # list with agent objects
            "pit": False,   # if it's a pit, then True, else False
            "wumpus": None, # if no Wumpus, then None, else "small" or "big"
            "gold": None,   # if no Gold, then None, else int-value
            "item": None,   # if no Item, then None, else "armor" or ...
        }
        
        # creates a grid of size n x n
        size = grid_properties["size"]
        grid = [[empty_field for _ in range(size)] for _ in range(size)]

        # initializes the agents
        # gives agents their positions, grid size and ID
        # stores agent inside the grid
        if agents:
            agents[0].ID = 'p1'
            agents[0].position = [0, 0]
            agents[0].grid_size = size
            grid[0][0]["agents"] = list.append(agents[0])
        if len(agents) > 1:
            agents[1].ID = 'p2'
            agents[1].position = [0, size - 1]
            agents[1].grid_size = size
            grid[0][size - 1]["agents"].append(agents[1])
        if len(agents) > 2:
            agents[2].ID = 'p3'
            agents[2].position = [size - 1, 0]
            agents[2].grid_size = size
            grid[size - 1][0]["agents"].append(agents[2])
        if len(agents) > 3:
            agents[3].ID = 'p4'
            agents[3].position = [size - 1, size - 1]
            agents[3].grid_size = size
            grid[size - 1][size - 1]["agents"].append(agents[3])
        
        self.generate_objects(grid, grid_properties)
        
        return grid     
        

    def update_grid(self, grid, agents):
        grid_copy = [row[:] for row in grid]        
        for agent in agents:
            # simplify agent's position
            x = agent.position[0]
            y = agent.position[1]
            
            if agent.ID == 'dead':
                continue
            if x < 0 or x >= len(grid):
                agent.ID = 'dead'
            elif y < 0 or y >= len(grid):
                agent.ID = 'dead'
            else:
                
                for wumpus in self.wumpi:
                    if wumpus.position == agent.position:
                        agent.ID = 'dead'
                        break
                    
                for pit in self.pits:
                    if pit.position == agent.position:
                        agent.ID = 'dead'
                        break
                
                for other_agent in agents:
                    if other_agent.ID == agent.ID:
                        continue
                    if other_agent.position == agent.position:
                        self.meeting(agent, other_agent)
                    
                grid_copy[x][y]["agents"].append(agent)           
                
        return grid_copy
    
    
    def meeting(self, agent1, agent2):
        """defines the result of a meeting between two agents"""
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
            
            
    def spawn_objects(self, grid, grid_properties):
        """
        Spawns pits, wumpi, gold and items into a grid. Every object should be saved inside the grid's coordinates and the object's own list.
        
        :param grid: initial grid of the game
        :param grid_properties: should contain information about each spawnable object's amount
        """
        self.pits = []        
        # TODO: place pits
        
        self.wumpi = []
        # TODO: place wumpi
        
        self.gold = []
        # TODO: place gold
        
        self.items = []
        # TODO: place special items
        pass
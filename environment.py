class Game():   
    
    def __init__(self):
        pass
    
    
    # creates a grid given the grid properties
    # places the agents in the grid by giving them their positions
    def grid_preperation(self, agents, grid_properties):
        
        # creates a grid of size n x n
        size = grid_properties["size"]
        grid = [[0 for _ in range(size)] for _ in range(size)]

        # initializes the agents
        # gives agents their positions
        # gives agents the grid size
        # gives agents their ID
        if agents:
            agents[0].ID = 'p1'
            agents[0].position = [0, 0]
            agents[0].grid_size = size
        if len(agents) > 1:
            agents[1].ID = 'p2'
            agents[1].position = [0, size - 1]
            agents[1].grid_size = size
        if len(agents) > 2:
            agents[2].ID = 'p3'
            agents[2].position = [size - 1, 0]
            agents[2].grid_size = size
        if len(agents) > 3:
            agents[3].ID = 'p4'
            agents[3].position = [size - 1, size - 1]
            agents[3].grid_size = size
        
        
        # TODO: place pits
        # TODO: place wumpi
        # TODO: place gold
        # TODO: place special items
        
        return grid
    

    # simulates the game given the agents and grid properties
    def simulate(self, agents, grid_properties):
        initial_grid = self.grid_preperation(agents, grid_properties)
            
        grid = self.update_grid(initial_grid, agents)

        # prints the initial grid with agents (TODO: remove this)
        print(" initial Grid with agents:")
        for row in grid:
            print(row)

        
        # TODO: run the game loop
        
        for _ in range(10):
        
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
            
            grid = self.update_grid(initial_grid, agents)
                    
            # prints the grid (TODO: remove this)
            print("Grid:")
            for row in grid:
                print(row)
            
        

    def update_grid(self, grid, agents):
        grid_copy = [row[:] for row in grid]        
        for agent in agents:
            if agent.ID == 'dead':
                continue
            if agent.position[0] < 0 or agent.position[0] >= len(grid):
                agent.ID = 'dead'
            elif agent.position[1] < 0 or agent.position[1] >= len(grid):
                agent.ID = 'dead'
            else:
                grid_copy[agent.position[0]][agent.position[1]] = agent.ID             
        
            # TODO: what happens, if two agents are on the same position?
            # TODO: what happens, if an agent is on a pit?
            # TODO: what happens, if an agent is on a wumpus?
        
        return grid_copy     
        
            
            
        
            
        
        
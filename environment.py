class Game():   
    
    def __init__(self):
        pass
    
    
    # creates a grid given the grid properties and places the agents in the corners
    def grid_preperation(self, agents, grid_properties):
        
        # creates a grid of size n x n
        size = grid_properties["size"]
        grid = [[0 for _ in range(size)] for _ in range(size)]

        
        # places agents in the grid corners and gives them their positions and the grid size
        if agents:
            grid[0][0] = agents[0]  # Top-left corner
            agents[0].position = (0, 0)
            agents[0].grid_size = size
        if len(agents) > 1:
            grid[0][size - 1] = agents[1]  # Top-right corner
            agents[1].position = (0, size - 1)
            agents[1].grid_size = size
        if len(agents) > 2:
            grid[size - 1][0] = agents[2]  # Bottom-left corner
            agents[2].position = (size - 1, 0)
            agents[2].grid_size = size
        if len(agents) > 3:
            grid[size - 1][size - 1] = agents[3]  # Bottom-right corner
            agents[3].position = (size - 1, size - 1)
            agents[3].grid_size = size
        
        
        # TODO: place pits
        # TODO: place wumpi
        # TODO: place gold
        # TODO: place special items
        
        return grid
    

    # simulates the game given the agents and grid properties
    def simulate(self, agents, grid_properties):
        grid = self.grid_preperation(agents, grid_properties)
        
        # TODO: run the game loop
        
        
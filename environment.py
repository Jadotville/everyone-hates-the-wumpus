class Game():   
    
    pits = []
    wumpi = []
    gold_position = []
    items = []
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
        print("gold_amount_player", self.gold_amount_player)
        for _ in range(game_properties["num_games"]):
            self.simulate(agents, grid_properties, prints)


    # simulates the game given the agents, grid properties
    def simulate(self, agents, grid_properties, prints):
        
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
                for row in grid:
                    print(row)
                print("Gold:", self.gold_amount_player)
   
   
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
            agents[0].position = [0, 0]
            agents[0].grid_size = size
        if len(agents) > 1:
            agents[1].position = [0, size - 1]
            agents[1].grid_size = size
        if len(agents) > 2:
            agents[2].position = [size - 1, 0]
            agents[2].grid_size = size
        if len(agents) > 3:
            agents[3].position = [size - 1, size - 1]
            agents[3].grid_size = size
        
        self.wumpi = []
        # TODO: place wumpi
        
        self.pits = []        
        # TODO: place pits
        
        self.gold_position = []
        
        self.items = []
        # TODO: place special items
        
        return grid     
        

    def update_grid(self, grid, agents):
        grid_copy = [row[:] for row in grid]
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
                    
                if grid_copy[agent.position[0]][agent.position[1]] == 0:
                    grid_copy[agent.position[0]][agent.position[1]] = agent.ID             
                else:
                    grid_copy[agent.position[0]][agent.position[1]] = grid_copy[agent.position[0]][agent.position[1]] + ' | ' + agent.ID
            i+=1
        return grid_copy
    
    
    # defines the result of a meeting between two agents
    def meeting(self, agent1, agent2):
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
            
            
            
from environment import Game
from agent import RandomAgent


if __name__ == '__main__':
    game = Game()
    
    agents = []
    
    agents.append(RandomAgent())
    agents.append(RandomAgent())
    agents.append(RandomAgent())
    agents.append(RandomAgent())
    
    
    grid_properties = {
        "size": 5,
        "num_pits": 0,
        "num_wumpi": 0
    }
    
    
    
    game.simulate(agents, grid_properties)
from environment import Game
from agent import RandomAgent


if __name__ == '__main__':
    
    agents = []
    
    agents.append(RandomAgent())
    agents.append(RandomAgent())
    agents.append(RandomAgent())
    agents.append(RandomAgent())
    
    
    grid_properties = {
        "size": 5,
        "num_pits": 0,
        "num_small_wumpi": 0,
        "num_big_wumpi": 0,
        "num_gold": 0,
        "num_armor": 0,
    }
    
    game_properties = {
        "num_games": 1,
        "prints": True,
    }
    
    
    game = Game(agents, grid_properties, game_properties)
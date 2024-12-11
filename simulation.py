from environment import Game
from agent import RandomAgent


if __name__ == '__main__':
    
    agents = [RandomAgent(), RandomAgent(), RandomAgent(), RandomAgent()]       
    
    grid_properties = {
        "size": 4, # must be odd
        "num_pits": 0, # this should be lower than size*size/3
        "num_s_wumpi": 0,
        "num_l_wumpi": 0,
        "num_gold": 2,
        "num_armor": 2,
        "num_swords": 2,
    }
    
    game_properties = {
        "num_games": 1000,
        "prints": False,
        "plot": True,
    }
    
    
    game = Game(agents, grid_properties, game_properties)
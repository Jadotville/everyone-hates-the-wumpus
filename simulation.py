from environment import Game
from agent import RandomAgent


if __name__ == '__main__':
    
    agents = [RandomAgent(), RandomAgent(), RandomAgent(), RandomAgent()]       
    
    grid_properties = {
        "size": 9, # must be odd
        "num_pits": 15, # this should be lower than size*size/3
        "num_wumpi": 3,
        "num_gold": 3,
        "num_armor": 2,
        "num_swords": 2,
    }
    
    game_properties = {
        "num_games": 1,
        "prints": True,
    }
    
    
    game = Game(agents, grid_properties, game_properties)
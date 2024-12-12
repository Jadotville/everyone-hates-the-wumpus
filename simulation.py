from environment import Game
from agent import RandomAgent, RightAgent, RandomBadAgent


if __name__ == '__main__':
    
    grid_properties = {
        "size": 5, # must be odd
        "num_pits": 0, # this should be lower than size*size/3
        "num_s_wumpi": 0,
        "num_l_wumpi": 0,
        "num_gold": 2,
        "num_armor": 2,
        "num_swords": 2,
    }
    
    game_properties = {
        "num_games": 100,
        "prints": False,
        "plot": True,
    }
    
    agents = [RightAgent(grid_properties["size"]), RandomBadAgent(grid_properties["size"]), RandomAgent(grid_properties["size"]), RandomAgent(grid_properties["size"])]       
    
    game = Game(agents, grid_properties, game_properties)
    

# TODO: implement armor and swords
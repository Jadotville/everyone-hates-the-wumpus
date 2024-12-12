from environment import Game
from agent import RandomAgent, RightAgent, RandomBadAgent
from enums import Plan

if __name__ == '__main__':
    
    # ------ GAME SETTINGS ------
    
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
    
    
    # ------ AGENT PARAMETERS ------
    
    size = grid_properties["size"]
    # change this dictionary and pass it to AI-Agents to test out a plan on first initialization
    example_plan = {
                "status": Plan.GO_TO,
                "patience": None, # optional int: agent follows a plan for a set number of actions, before resetting to "status": Plan.EXPLORE
                "target_pos": [4,2] # optional [int,int]: when "status": Plan.GO_TO the agent should go to specified position
            }
    
    
    # ------ START SIMULATION ------
    
    agents = [RightAgent(size=size), RandomBadAgent(size=size), RandomAgent(size=size), RandomAgent(size=size)]       
    
    game = Game(agents, grid_properties, game_properties)
    

# TODO: implement armor and swords
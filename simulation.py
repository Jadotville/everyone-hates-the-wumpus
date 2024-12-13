from environment import Game
from agent import RandomAgent, RightAgent, RandomBadAgent, CooperativeAgent, DefensiveAgent
from enums import Plan

if __name__ == '__main__':
    
    # ------ GAME SETTINGS ------
    
    grid_properties = {
        "size": 7, # Grid size: must be odd
        "num_pits": 0, # Pits: this should be pretty low
        "num_s_wumpi": 0, # Smol wumpi: this should be pretty low
        "num_l_wumpi": 0, # Large wumpi: this should be pretty low
        "num_gold": 2, # Gold spawns
        "num_armor": 2, # Armor spawns
        "num_swords": 2, # Sword spawns
    }
    
    game_properties = {
        "num_games": 100,
        "prints": False, # display the game's state in the console
        "plot": True, # plot the total amount of gold
    }
    
    
    # ------ AGENT PARAMETERS ------
    
    size = grid_properties["size"]
    # change this dictionary and pass it to AI-Agents to test out a plan on first initialization
    testing_plan = {
                "status": Plan.EXPLORE,
                "patience": None, # optional int: agent follows a plan for a set number of actions, before resetting to "status": Plan.EXPLORE
                "target_pos": [] # optional [[int,int], ...]: when "status": Plan.GO_TO the agent should go to first specified position, then the next
            }
    
    
    # ------ START SIMULATION ------
    
    # pass the following setup for a standart game
    standart_agents = [
        CooperativeAgent(size=size), 
        RandomAgent(size=size), 
        #RightAgent(size=size), 
        DefensiveAgent(size = size),
        RandomBadAgent(size=size)
    ]  
    
    # pass the following setup for experimenting
    testing_agents = [
        RandomAgent(size=size, init_plan=testing_plan, debug=True, risk_aversion=0.95)
    ]
    
    # pass the following setup for random agents, they will always try to not step into pits/wumpi like an idiot
    random_agents = [
        RandomAgent(size=size), 
        RandomAgent(size=size), 
        RandomAgent(size=size), 
        RandomAgent(size=size)
    ] 
    
    game = Game(standart_agents, grid_properties, game_properties)
    

# TODO: implement armor and swords
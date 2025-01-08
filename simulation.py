from environment import Game
from agent import RandomAgent, RightAgent, RandomBadAgent, CooperativeAgent, DefensiveAgent
from enums import Plan

if __name__ == '__main__':
    
    # ------ GAME SETTINGS ------
    
    grid_properties = {
        "size": 7,          # Grid size: must be odd
        "num_pits": 1,      # Pits: this should be pretty low
        "num_s_wumpi": 2,   # Smol wumpi: this should be pretty low
        "num_l_wumpi": 1,   # Large wumpi: this should be pretty low
        "num_small_gold": 2,# Gold spawns
        "num_large_gold": 1,# Gold spawns
        "num_armor": 2,     # Armor spawns
        "num_swords": 2,    # Sword spawns
        "small_gold": 5,    # Amount of gold for small gold
        "large_gold": 10,   # Amount of gold for large gold
        "arrow_price": 2,   # Price for arrows
        "amount_arrows_start": 2, # Amount of arrows at the start
        "meeting_rewards" : [[[0,    5 ],       [0,     -5]],       [[0,        5],     [0,     5]],
                             [[0,    0],        [-5,       -5]],    [[5,        5],     [5,     5]]], # Rewards for meeting another agent
                                                #                     |  other player robs      other player does nothing
                                                #         player robs |       [0]                     [1]
                                                # player does nothing |       [2]                     [3]
                                                # for each cell in upper grid:
                                                #                     |  player has armor       player has no armor
                                                #    player has armor |      [0][0]                  [0][1]
                                                # player has no armor |      [1][0]                  [1][1]

        }
    
    game_properties = {
        "num_games": 1,   # number of games to simulate
        "prints": True,    # display the game's state in the console
        "plot": True,       # plot the evolution of total amount of gold per agent
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
    # standart_agents = [
    #     CooperativeAgent(size=size), 
    #     RandomAgent(size=size), 
    #     #RightAgent(size=size), 
    #     DefensiveAgent(size = size),
    #     RandomBadAgent(size=size)
    # ]  
    
    # pass the following setup for experimenting
    testing_agents = [
        RandomAgent(size=size, debug=True),
        RandomAgent(size=size, risk_aversion=0.95), 
        RandomAgent(size=size, risk_aversion=0.95), 
        RandomAgent(size=size, risk_aversion=0.95)
    ]
    
    # pass the following setup for random agents, they will always try to not step into pits/wumpi like an idiot
    random_agents = [
        RandomAgent(size=size), 
        RandomAgent(size=size), 
        RandomAgent(size=size), 
        RandomAgent(size=size)
    ] 
    
    game = Game(testing_agents, grid_properties, game_properties)
    

# TODO: implement armor and swords
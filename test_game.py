import unittest
from environment import Game

class TestEnvironment(unittest.TestCase):

    def test_grid_generation(self):
        
        game = Game()
        grid = game.create_grid(game.grid_properties)
    
        # full display of all, unfiltered information
        print("Generated Grid:")
        for row in grid:
            print(row)
        
        # separate display for all generated items
        items = ["agents", "pit", "wumpus", "gold", "item"]
        for item in items:
            game.print_objects(grid, item)

if __name__ == '__main__':
    unittest.main()
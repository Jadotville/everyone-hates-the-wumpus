import unittest
from environment import Game

class TestEnvironment(unittest.TestCase):

    def test_grid_generation(self):
        
        game = Game()
        grid = game.create_grid(game.grid_properties)
    
        print("Generated Grid:")
        for row in grid:
            print(row)

if __name__ == '__main__':
    unittest.main()
import unittest

from agent import RandomAgent

class TestRandomAgent(unittest.TestCase):

    def test_action(self):
        agent = RandomAgent()
        for i in range(10):
            print(agent.action())

if __name__ == '__main__':
    unittest.main()
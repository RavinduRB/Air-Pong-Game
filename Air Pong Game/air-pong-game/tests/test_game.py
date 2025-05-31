import unittest
from src.game.game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_initialization(self):
        self.assertIsNotNone(self.game)

    def test_game_start(self):
        self.game.start()
        self.assertTrue(self.game.is_running)

    def test_game_update(self):
        initial_score = self.game.score
        self.game.update()
        self.assertNotEqual(initial_score, self.game.score)

    def test_game_render(self):
        self.game.render()
        # Assuming render method updates some internal state
        self.assertTrue(self.game.rendered)

if __name__ == '__main__':
    unittest.main()
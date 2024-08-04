import unittest
from unittest.mock import MagicMock, patch
from scripts.tools.hook import Hook
from scripts.player import Player
import os
import pygame


class TestHook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((32, 32))
        self.game = MagicMock()
        self.player = Player(self.game, [0, 0], [16, 16])
        self.hook = Hook(self.game, self.player)

    def test_init(self):
        self.assertEqual(self.hook.is_hooked, False)
        self.assertEqual(self.hook.max_length, 200)
        self.assertEqual(self.hook.is_rope_torn, True)

    @patch('pygame.mouse.get_pressed')
    def test_shoot(self, mock_pressed):
        mock_pressed.return_value = (0, 0, 1, 0)
        self.hook.shoot((5, 5))
        self.assertNotEqual(self.hook.velocity, [0, 0])
        self.assertEqual(self.hook.is_rope_torn, False)
        with patch.object(self.hook, 'pos', [100, 200]):
            self.hook.update(MagicMock())

    def test_pull_player(self):
        with patch.object(self.hook, 'pos', [5, 5]):
            self.hook.pull_player()
        self.assertNotEqual(self.player.velocity, [0, 0])

if __name__ == '__main__':
    unittest.main()
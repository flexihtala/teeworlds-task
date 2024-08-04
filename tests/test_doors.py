import unittest
from unittest.mock import MagicMock, patch
from scripts.tools.door import Door
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
        self.door = Door((19, 0), self.game)

    def test_init(self):
        self.assertEqual(self.door.center_coordinates, [27, 16])
        self.assertEqual(self.door.is_open, False)
        self.assertEqual(self.door.can_be_closed, True)

    def test_distance(self):
        self.assertNotEqual(self.door.distance_to_player(self.player), 0)

    def test_update(self):
        with patch.object(self.door.game.player, 'is_e_active', True), patch.object(self.door, 'door_kd', 0):
            self.door.update()

if __name__ == '__main__':
    unittest.main()
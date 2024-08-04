import unittest
from scripts.player import Player
from unittest.mock import MagicMock, patch, PropertyMock
import os
import pygame


class PlayerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((800, 600))
        self.game = MagicMock()
        self.player = Player(self.game, [0, 0], [16, 16])

    def test_init(self):
        self.assertIsInstance(self.player, Player)
        self.assertEqual(self.player.is_immortal, False)
        self.assertIsNotNone(self.player.hook)
        self.assertIsNotNone(self.player.minigun)
        self.assertIsNotNone(self.player.rpg)
        self.assertEqual(len(self.player.weapons), 2)

    def test_jump(self):
        with patch.object(self.player, 'jumps', 2):
            self.player.jump()
        self.assertNotEqual(self.player.velocity[1], 0)

    def test_die(self):
        with patch.object(self.player.game.tilemap, 'spawnpoint_positions', [[1, 1], [2, 2]]):
            self.player.die()
        self.assertGreater(self.player.immortality_time, 0)
        self.assertEqual(self.player.hp, self.player.max_hp)
        self.assertEqual(self.player.velocity, [0, 0])

    def test_update(self):
        self.player.update(MagicMock())

    def test_take_damage(self):
        self.player.take_damage(50)
        self.assertEqual(self.player.hp, self.player.max_hp)
        with patch.object(self.player, 'immortality_time', 0):
            self.player.take_damage(50)
        self.assertNotEqual(self.player.hp, self.player.max_hp)


if __name__ == '__main__':
    unittest.main()
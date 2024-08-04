import unittest
from unittest.mock import MagicMock, patch
import os
from scripts.tools.rpg.rpg_bullet import Bullet
import pygame
from scripts.player import Player


class TestRpgBullet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((32, 32))
        self.game = MagicMock()
        self.player = Player(self.game, [1, 0], [16, 16])
        self.player.immortality_time = 0
        self.bullet = Bullet(self.game, [0, 0], [5, 5], True, 45, 10)

    def test_explode(self):
        self.bullet.explode()
        self.assertNotEqual(len(self.bullet.explosion_group), 0)

    def test_apply_explosion_force(self):
        self.bullet.apply_explosion_force(self.player)
        self.assertNotEqual(self.player.velocity, [0, 0])

    def test_update(self):
        self.bullet.update(MagicMock(), (0, 0), False)
        self.assertNotEqual(self.bullet.velocity, [0, 0])

    def test_serialize(self):
        self.bullet.serialize()
        self.assertEqual(self.bullet.serialize(), {'angle': 45, 'bullet_type': 'rpg', 'damage': 10, 'damaged_players': [], 'direction': [5, 5], 'is_bullet_flipped': True, 'is_damaged': False, 'is_exploded': False, 'pos': [0, 0]})


if __name__ == '__main__':
    unittest.main()


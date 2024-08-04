import pygame

from scripts.tools.minigun.minigun import Minigun
from scripts.tools.rpg.rpg import Rpg
import unittest
from unittest.mock import MagicMock, patch
from scripts.player import Player
import os


class TestWeapon(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((32, 32))
        self.game = MagicMock()
        self.player = Player(self.game, [0, 0], [16, 16])
        self.minigun = Minigun(self.game, self.player)
        self.rpg = Rpg(self.game, self.player)

    def test_init(self):
        self.assertEqual(self.minigun.is_shooting, False)
        self.assertEqual(self.minigun.damage, 5)
        self.assertEqual(self.minigun.angle, 0)
        self.assertEqual(self.rpg.is_bullet_flipped, False)
        self.assertEqual(self.rpg.damage, 30)
        self.assertEqual(self.rpg.angle, 0)

    def test_shoot(self):
        with patch.object(self.minigun, 'ticks', 10):
            self.minigun.shoot((1, 1))
        with patch.object(self.rpg, 'ticks', 100):
            self.rpg.shoot((1, 1))
        self.assertEqual(len(self.player.bullets), 2)
        self.player.bullets[0].update(MagicMock(), 0)
        self.assertEqual(self.player.bullets[0].pos[0], 18)
        self.assertEqual(self.player.bullets[0].serialize(), {'bullet_type': 'minigun', 'damage': 5, 'damaged_player': -1,'direction': (1, 1),'is_exist': True,'pos': [18, 18]})

    @patch('pygame.mouse.get_pos')
    def test_get_shooting_direction(self, mock_mouse_pos):
        mock_mouse_pos.return_value = (5, 5)
        with patch.object(self.minigun, 'is_shooting', True):
            self.minigun.update(MagicMock(), 0)
        self.assertEqual(self.minigun.get_shooting_direction(), (-0.8012153902822761, -0.5983760509703074))

    def test_give_player_impulse(self):
        with patch.object(self.minigun, 'angle', 45):
            self.minigun.give_player_impulse()
        self.assertNotEqual(self.player.velocity[0], 0)
        self.assertNotEqual(self.player.velocity[1], 0)


if __name__ == '__main__':
    unittest.main()

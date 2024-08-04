import os
import unittest
import pygame
from scripts.utils import load_sprite


class TestLoadSprite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def test_load_sprite_colorkey(self):
        test_sprite_path = 'player.png'
        test_sprite = pygame.image.load('assets/sprites/' + test_sprite_path).convert()
        test_sprite.set_colorkey((0, 0, 0))

        loaded_sprite = load_sprite(test_sprite_path)

        self.assertEqual(pygame.image.tostring(loaded_sprite, "RGB"), pygame.image.tostring(test_sprite, "RGB"),
                         "Метод load_sprite неправильно устанавливает цвет прозрачности")

    def test_load_sprite_type(self):
        test_sprite_path = 'player.png'
        loaded_sprite = load_sprite(test_sprite_path)

        self.assertIsInstance(loaded_sprite, pygame.Surface,
                              "Метод load_sprite должен возвращать объект pygame.Surface")


if __name__ == '__main__':
    unittest.main()

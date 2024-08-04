import os
import unittest
from unittest.mock import patch, MagicMock
import pygame
from main_menu.menu import MainMenu


class TestMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def setUp(self):
        pygame.init()
        self.menu = MainMenu(pygame.display.set_mode((32, 32)))

    @patch("game.pygame.event.get")
    def test_main_loop_quit_event(self, mock_event_get):
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]
        with self.assertRaises(SystemExit):
            self.menu.main_menu()


if __name__ == "__main__":
    unittest.main()

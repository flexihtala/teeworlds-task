import unittest
from unittest.mock import patch, MagicMock
import pygame
import os
from main_menu.input_box import InputBox
from main_menu.input_name_menu import InputNameMenu


class TestMainMenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.input_name_menu = InputNameMenu(self.screen)
        self.input_name_menu.start_button = MagicMock()
        self.input_name_menu.input_box = InputBox(5, 5, 300, 48, pygame.Color('black'), pygame.Color('darkslategrey'),
                                                  self.screen)

    @patch('main_menu.input_name_menu.pygame.event.get')
    def test_run_quit_event(self, mock_event_get):
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]
        result = self.input_name_menu.run()
        self.assertEqual(result, "ENDofTHEprogramGG")

    @patch('main_menu.input_name_menu.pygame.event.get')
    def test_run_start_button_event(self, mock_event_get):
        mock_event = pygame.event.Event(pygame.USEREVENT, button=self.input_name_menu.start_button)
        self.input_name_menu.start_button.handle_event = MagicMock()
        self.input_name_menu.start_button.handle_event.return_value = None
        mock_event_get.return_value = [mock_event]

        with patch.object(self.input_name_menu.input_box, 'is_enter_pressed', False):
            self.input_name_menu.input_box.text = 'test'
            result = self.input_name_menu.run()
            self.assertEqual(result, 'test')

    @patch('main_menu.input_name_menu.pygame.event.get')
    def test_run_empty_name_event(self, mock_event_get):
        mock_event_key_pressed = pygame.event.Event(pygame.KEYDOWN, key=119, unicode='w')
        mock_event_start = pygame.event.Event(pygame.USEREVENT, button=self.input_name_menu.start_button)
        self.input_name_menu.start_button.handle_event = MagicMock()
        self.input_name_menu.start_button.handle_event.return_value = None
        mock_event_get.return_value = [mock_event_start, mock_event_key_pressed, mock_event_start]

        with patch.object(self.input_name_menu.input_box, 'is_enter_pressed', False):
            self.input_name_menu.input_box.text = ''
            result = self.input_name_menu.run()
            self.assertEqual(self.input_name_menu.is_warning_active, True)
            self.assertEqual(result, 'w')


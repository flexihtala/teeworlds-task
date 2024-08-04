import unittest
import pygame
from main_menu.input_box import InputBox


class TestInputBox(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.input_box = InputBox(5, 5, 300, 48, pygame.Color('black'), pygame.Color('darkslategrey'), self.screen)

    def test_initialization(self):
        self.assertEqual(self.input_box.rect.x, 5)
        self.assertEqual(self.input_box.rect.y, 5)
        self.assertEqual(self.input_box.rect.w, 300)
        self.assertEqual(self.input_box.rect.h, 48)

    def test_handle_event(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=97, unicode='a')
        self.input_box.handle_event(event)
        self.assertEqual(self.input_box.text, 'a')

        event = pygame.event.Event(pygame.KEYDOWN, key=96)
        self.input_box.handle_event(event)
        self.assertEqual(self.input_box.text, 'a')

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_BACKSPACE)
        self.input_box.handle_event(event)
        self.assertEqual(self.input_box.text, '')

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        self.input_box.handle_event(event)
        self.assertEqual(self.input_box.is_enter_pressed, True)

    def test_update(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=119, unicode='w')
        self.input_box.handle_event(event)
        self.input_box.update()
        self.assertEqual(self.input_box.rect.w, 300)

        for _ in range(20):
            self.input_box.handle_event(event)
            self.input_box.update()
        self.assertEqual(self.input_box.text, 'wwwwwwwwww')
        self.assertEqual(self.input_box.rect.w, 350)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
import pygame
from scripts.tilemap import Tilemap
from editor import Editor


class TestEditor(unittest.TestCase):

    @patch('editor.load_sprite')
    def setUp(self, mock_load_sprite):
        # Замена загрузки спрайтов на создание пустого Surface
        mock_load_sprite.return_value = pygame.Surface((32, 32))
        self.editor = Editor()

    def test_init(self):
        self.assertIsInstance(self.editor, Editor)
        self.assertEqual(self.editor.scroll, [False, False])
        self.assertEqual(self.editor.offset, 0)
        self.assertEqual(self.editor.rows, 20)
        self.assertEqual(self.editor.cols, 50)
        self.assertEqual(self.editor.tile_size, 16)
        self.assertIsInstance(self.editor.assets, dict)
        self.assertIsInstance(self.editor.buttons, dict)
        self.assertIsNone(self.editor.current_tile)
        self.assertIsInstance(self.editor.tilemap, Tilemap)
        self.assertFalse(self.editor.is_left_hold)
        self.assertFalse(self.editor.is_right_hold)

    def test_fill_buttons_list(self):
        self.editor.fill_buttons_list()
        self.assertEqual(len(self.editor.buttons), len(self.editor.assets))

    @patch('pygame.mouse.get_pos')
    def test_place_tile(self, mock_get_pos):
        self.editor.current_tile = 'grass'
        mock_get_pos.return_value = (100, 100)
        self.editor.place_tile()
        tile_pos = ((100 + 2 * self.editor.offset) // 32, 100 // 32)
        tilemap_key = str(tile_pos[0]) + ';' + str(tile_pos[1])
        self.assertIn(tilemap_key, self.editor.tilemap.tilemap)
        self.assertEqual(self.editor.tilemap.tilemap[tilemap_key]['type'], 'grass')

        self.editor.place_tile(remove_tile=True)
        self.assertNotIn(tilemap_key, self.editor.tilemap.tilemap)

    @patch('pygame.transform.scale')
    @patch('pygame.mouse.get_pressed')
    @patch('pygame.mouse.get_pos')
    @patch('pygame.event.get')
    @patch('builtins.open')
    @patch('json.dump')
    @patch('pygame.quit')
    def test_run(self, mock_pygame_quit, mock_json_dump, mock_open, mock_event_get, mock_mouse_get_pos,
                 mock_mouse_get_pressed, mock_transform_scale):
        mock_transform_scale.return_value = pygame.Surface((32, 32))
        mock_mouse_get_pressed.return_value = [0, 1]
        mock_mouse_get_pos.return_value = (100, 100)
        mock_event_get.side_effect = [
            [pygame.event.Event(pygame.QUIT)],
            []
        ]

        with self.assertRaises(SystemExit):
            self.editor.run()

        mock_open.assert_not_called()
        mock_json_dump.assert_not_called()

        mock_event_get.side_effect = [
            [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_s})],
            [pygame.event.Event(pygame.KEYUP, {'key': pygame.K_s})],
            [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1})],
            [pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1})],
            [pygame.event.Event(pygame.QUIT)]
        ]

        with patch('pygame.display.update'), patch('pygame.draw.line'), patch(
                'pygame.draw.rect'):
            with self.assertRaises(SystemExit):
                self.editor.run()

        mock_open.assert_called_once_with('save.json', 'w', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()

import os
import unittest
from unittest.mock import patch, MagicMock
import pygame
from game import Game


class TestGame(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @patch('game.json.load')
    @patch('socket.socket')
    def setUp(self, mock_socket, mock_load):
        mock = MagicMock()
        mock_socket.return_value = mock
        mock.connect.return_value = None
        mock_socket.sendall.return_value = MagicMock()
        mock_load.return_value = {'4;10': {'type': 'grass', 'pos': [4, 10]}, '5;10': {'type': 'grass', 'pos': [5, 10]}, '6;10': {'type': 'grass', 'pos': [6, 10]}, '7;10': {'type': 'grass', 'pos': [7, 10]}, '8;10': {'type': 'grass', 'pos': [8, 10]}, '9;10': {'type': 'grass', 'pos': [9, 10]}, '10;10': {'type': 'grass', 'pos': [10, 10]}, '11;10': {'type': 'grass', 'pos': [11, 10]}, '12;10': {'type': 'grass', 'pos': [12, 10]}, '13;10': {'type': 'grass', 'pos': [13, 10]}, '14;10': {'type': 'grass', 'pos': [14, 10]}, '15;10': {'type': 'grass', 'pos': [15, 10]}, '16;10': {'type': 'grass', 'pos': [16, 10]}, '17;10': {'type': 'grass', 'pos': [17, 10]}, '18;10': {'type': 'grass', 'pos': [18, 10]}, '19;10': {'type': 'grass', 'pos': [19, 10]}, '20;10': {'type': 'grass', 'pos': [20, 10]}, '21;10': {'type': 'grass', 'pos': [21, 10]}, '22;10': {'type': 'grass', 'pos': [22, 10]}, '10;9': {'type': 'heal', 'pos': [10, 9]}, '14;9': {'type': 'random_potion', 'pos': [14, 9]}, '12;8': {'type': 'spawnpoint', 'pos': [12, 8]}, '4;11': {'type': 'left_bottom_ground', 'pos': [4, 11]}, '5;11': {'type': 'bottom_ground', 'pos': [5, 11]}, '6;11': {'type': 'bottom_ground', 'pos': [6, 11]}, '7;11': {'type': 'bottom_ground', 'pos': [7, 11]}, '8;11': {'type': 'bottom_ground', 'pos': [8, 11]}, '9;11': {'type': 'bottom_ground', 'pos': [9, 11]}, '10;11': {'type': 'bottom_ground', 'pos': [10, 11]}, '11;11': {'type': 'bottom_ground', 'pos': [11, 11]}, '12;11': {'type': 'bottom_ground', 'pos': [12, 11]}, '13;11': {'type': 'bottom_ground', 'pos': [13, 11]}, '14;11': {'type': 'bottom_ground', 'pos': [14, 11]}, '15;11': {'type': 'bottom_ground', 'pos': [15, 11]}, '16;11': {'type': 'bottom_ground', 'pos': [16, 11]}, '17;11': {'type': 'bottom_ground', 'pos': [17, 11]}, '18;11': {'type': 'bottom_ground', 'pos': [18, 11]}, '19;11': {'type': 'bottom_ground', 'pos': [19, 11]}, '20;11': {'type': 'bottom_ground', 'pos': [20, 11]}, '21;11': {'type': 'bottom_ground', 'pos': [21, 11]}, '22;11': {'type': 'right_bottom_ground', 'pos': [22, 11]}, '12;6': {'type': 'spawnpoint', 'pos': [12, 6]}, '12;4': {'type': 'spawnpoint', 'pos': [12, 4]}, '12;2': {'type': 'spawnpoint', 'pos': [12, 2]}, '11;9': {'type': 'heal', 'pos': [11, 9]}, '13;9': {'type': 'random_potion', 'pos': [13, 9]}, '15;9': {'type': 'random_potion', 'pos': [15, 9]}}
        self.game = Game()

    def test_init(self):
        self.assertEqual(len(self.game.heals), 2)
        self.assertEqual(len(self.game.random_potions), 3)
        self.assertEqual(len(self.game.tilemap.spawnpoint_positions), 4)

    @patch('game.MainMenu.main_menu')
    @patch('game.pygame.event.get')
    def test_main_loop_quit_event(self, mock_event_get, mock_main_menu):
        mock_main_menu.return_value = None
        mock_event_get.return_value = [pygame.event.Event(pygame.QUIT)]

        with self.assertRaises(SystemExit):
            self.game.run()

    @patch('game.MainMenu.main_menu')
    @patch('game.pygame.event.get')
    def test_activate_cheat_menu(self, mock_event_get, mock_main_menu):
        mock_main_menu.return_value = None
        event_activate_cheat_menu = pygame.event.Event(pygame.KEYDOWN, key=96)
        event_a = pygame.event.Event(pygame.KEYDOWN, key=97, unicode='a')
        self.game.input_box.is_enter_pressed = True
        return_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        mock_event_get.return_value = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1),
            pygame.event.Event(pygame.MOUSEWHEEL, y=-1),
            event_activate_cheat_menu,
            event_a,
            return_event,
            pygame.event.Event(pygame.MOUSEWHEEL, y=-1),
            pygame.event.Event(pygame.QUIT)]
        with patch.object(self.game.input_box, 'is_enter_pressed', True):
            with self.assertRaises(SystemExit):
                self.game.run()
        self.assertEqual(self.game.is_cheat_menu_active, True)

    def test_deserialize_bullet(self):
        bullet = self.game.deserialize_bullet({'pos': [487.23352125624103, 40.94680598649589], 'direction': [0.8487310536011489, -0.5288247333976389], 'bullet_type': 'minigun', 'is_exist': False, 'damage': 5, 'damaged_player': -1})
        self.assertEqual(bullet.pos, [487.23352125624103, 40.94680598649589])
        self.assertEqual(bullet.damage, 5)
        self.assertEqual(bullet.direction, [0.8487310536011489, -0.5288247333976389])
        self.assertEqual(bullet.damaged_player, -1)

        another_bullet = self.game.deserialize_bullet({'pos': [295.74588690388646, 163.912253949587], 'direction': [0.04682358629858615, 0.9989031743698379], 'is_bullet_flipped': False, 'angle': 87.31622484053102, 'is_exploded': True, 'bullet_type': 'rpg', 'damage': 30, 'damaged_players': [], 'is_damaged': True})
        self.assertEqual(another_bullet.pos, [295.74588690388646, 163.912253949587])
        self.assertEqual(another_bullet.damage, 30)
        self.assertEqual(another_bullet.direction, [0.04682358629858615, 0.9989031743698379])
        self.assertEqual(another_bullet.is_bullet_flipped, False)

    @patch('socket.socket')
    def test_send_player_info(self, mock_socket):

        mock_socket_obj = MagicMock()
        mock_socket.return_value = mock_socket_obj
        mock_socket_obj.sendall = MagicMock()

        with patch('json.dumps', return_value='{"mocked": "data"}') as mock_json_dumps:
            game = Game()
            game.send_player_info()
            player_info_data = {
                'x': game.player.pos[0],
                'y': game.player.pos[1],
                'is_rope_torn': True,
                'hook_x': 0,
                'hook_y': 0,
                'direction': 'right',
                'mouse_pos': [0, 0],
                'weapon_index': 0,
                'bullets': [],
                'hp': 100,
                'nickname': '',
                'id': game.player.id,
            }

            mock_socket_obj.sendall.assert_called_once_with('{"mocked": "data"}'.encode())
            mock_json_dumps.assert_called_with(player_info_data)


if __name__ == '__main__':
    unittest.main()

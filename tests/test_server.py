import unittest
from unittest.mock import patch, MagicMock
import socket
import json
import threading
from server import GameServer


class TestGameServer(unittest.TestCase):
    @patch('socket.socket')
    def setUp(self, mock_socket):
        mock = MagicMock()
        mock_socket.return_value = mock
        mock.bind.return_value = '127.0.0.1'
        self.server = GameServer()

    @patch('server.socket.socket')
    def test_init(self, mock_socket):
        mock_socket_instance = mock_socket.return_value
        self.server.__init__()
        mock_socket_instance.bind.assert_called_with(('localhost', 5555))
        mock_socket_instance.listen.assert_called_once()

    def test_start(self):
        with self.assertRaises(ValueError):
            self.server.start()

    @patch('server.socket.socket')
    def test_handle_client(self, mock_socket):
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = [
            json.dumps({'x': 10, 'y': 20}).encode('utf-8'),
            b''
        ]
        addr = ('127.0.0.1', 12345)
        self.server.clients.append(mock_conn)
        with self.assertRaises(Exception):
            self.server.handle_client(mock_conn, addr)


if __name__ == "__main__":
    unittest.main()

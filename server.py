import socket
import threading
import json


class GameServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.players = {}
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        self.map = {}
        print('Сервер запущен, ожидание подключения')

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(262144).decode()
                if not data:
                    break
                loaded_data = json.loads(data)
                if 'map' in loaded_data:
                    self.map = loaded_data['map']
                    continue
                player_data = loaded_data
                self.players[addr] = player_data
                for client in self.clients:
                    client.sendall(json.dumps(self.players).encode('utf-8'))
        except Exception as e:
            raise e
        finally:
            conn.close()
            self.clients.remove(conn)
            self.players.pop(addr)
            print(f'Соединение с {addr} разорвано')

    def start(self):
        try:
            while True:
                conn, addr = self.server_socket.accept()
                address = str(addr[0]) + ":" + str(addr[1])
                print(f'Подключен к адресу {addr}')
                self.clients.append(conn)
                if not self.map:
                    conn.sendall(json.dumps({'map': None}).encode())
                else:
                    conn.sendall(json.dumps({'map': self.map}).encode())
                threading.Thread(target=self.handle_client,
                                 args=(conn, address)).start()
        except Exception:
            raise


if __name__ == "__main__":
    GameServer().start()

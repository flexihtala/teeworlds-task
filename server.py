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
        print('Сервер запущен, ожидание подключения')

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(4096).decode()
                if not data:
                    break
                player_data = json.loads(data)
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
                threading.Thread(target=self.handle_client,
                                 args=(conn, address)).start()
        except Exception:
            raise


if __name__ == "__main__":
    GameServer().start()

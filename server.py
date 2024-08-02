import socket
import threading
import pickle


class GameServer:
    def __init__(self):
        self.host = 'localhost'
        self.port = 5555
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.players = {}
        self.map = {}
        self.spawnpoints = []
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print('Сервер запущен, ожидание подключения')

    def handle_client(self, conn, addr):
        try:
            while True:
                data = pickle.loads(conn.recv(1024))
                if not data:
                    break
                if 'map' in data:
                    print('загрузил карту')
                    if not self.map:
                        self.map = data['map']
                        self.spawnpoints = data['spawnpoints']
                    continue
                player_data = data
                self.players[addr] = player_data
                self.players[addr]['map'] = self.map
                self.players[addr]['spawnpoints'] = self.spawnpoints
                for client in self.clients:
                    client.sendall(pickle.dumps(self.players))
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
                if self.map:
                    conn.sendall(pickle.dumps({'map': self.map,
                                               'spawnpoints': self.spawnpoints}))
                else:
                    conn.sendall(pickle.dumps({'map': None}))
                threading.Thread(target=self.handle_client,
                                 args=(conn, address)).start()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    GameServer().start()


import pygame
import sys
import socket
import json
import threading
import math
from scripts.settings import *
from scripts.utils import load_sprite
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.tools.hook import Hook


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Teeworlds Task')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.display = pygame.Surface((WIDTH / 2, HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.player = PhysicsEntity(self, (50, 50), (10, 16))

        self.movement = [False, False]

        self.assets = {
            'grass': load_sprite('tiles/grass.png'),
            'player': load_sprite('player.png')
        }

        self.tilemap = Tilemap(self, 16)

        self.scroll = [0, 0]
        self.camera_speed = 30
        self.hook = Hook(self, self.player)

        self.host = '192.168.1.125'
        self.port = 5555
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.socket_name = self.client_socket.getsockname()
        self.address = str(self.socket_name[0]) + ":" + str(
            self.socket_name[1])

        self.player_info = {}
        self.players_data = {}
        self.players = {}
        self.hooks = {}

        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def run(self):
        while True:
            self.display.fill(BACKGROUND_COLOR)
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, render_scroll)
            self.player.update(self.tilemap,
                               ((self.movement[1] - self.movement[0]) * 2, 0))
            self.player.render(self.display, render_scroll)
            self.render_players(render_scroll)

            self.hook.update(self.tilemap)
            self.hook.render(self.display, render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        mouse_pos = pygame.mouse.get_pos()
                        world_mouse_pos = (mouse_pos[0], mouse_pos[1])
                        direction = (world_mouse_pos[0] - WIDTH / 2, world_mouse_pos[1] - HEIGHT / 2)
                        length = math.sqrt(direction[0] * direction[0] + direction[1] * direction[1])
                        direction = (direction[0] / length, direction[1] / length)
                        self.hook.shoot(direction)

            self.send_player_info()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

    def send_player_info(self):
        self.player_info['x'] = self.player.pos[0]
        self.player_info['y'] = self.player.pos[1]
        self.player_info['is_rope_torn'] = self.hook.is_rope_torn
        self.player_info['hook_x'] = self.hook.pos[0]
        self.player_info['hook_y'] = self.hook.pos[1]
        try:
            self.client_socket.sendall(json.dumps(self.player_info).encode())
        except Exception as e:
            print(f"Ошибка при отправлении информации: {e}")

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if data:
                    self.players_data = json.loads(data)
                    self.players_data.pop(self.address)
                    for addr, pdata in self.players_data.items():
                        if addr not in self.players:
                            self.players[addr] = PhysicsEntity(self, (pdata['x'], pdata['y']), (10, 16))
                            self.hooks[addr] = Hook(self, self.players[addr])
                        else:
                            self.players[addr].pos = (pdata['x'], pdata['y'])
                            self.hooks[addr].pos = (pdata['hook_x'], pdata['hook_y'])
                            self.hooks[addr].is_rope_torn = (pdata['is_rope_torn'])
                    print(self.players_data)
            except:
                print("Я сдох")

    def render_players(self, render_scroll):
        for player in self.players.values():
            player.render(self.display, render_scroll)
        for hook in self.hooks.values():
            hook.render(self.display, render_scroll)


if __name__ == "__main__":
    Game().run()

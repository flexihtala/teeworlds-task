import pygame
import sys
import socket
import json
import threading
import math
from scripts.settings import *
from scripts.utils import load_sprite
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.tools.rpg import rpg_bullet
from scripts.tools.minigun import minigun_bullet
from main_menu.menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Teeworlds Task')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.display = pygame.Surface((WIDTH / 2, HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.player = Player(self, (50, 50), (10, 16))

        self.movement = [False, False]

        self.assets = {
            'grass': load_sprite('tiles/grass.png'),
            'player': load_sprite('player.png'),
        }

        self.tilemap = Tilemap(self, 16)

        self.scroll = [0, 0]
        self.render_scroll = (0, 0)
        self.camera_speed = 30

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
        self.receive_thread = threading.Thread(target=self.receive_data)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def run(self):
        self.player.name = MainMenu(self.screen).main_menu()
        while True:
            self.display.fill(BACKGROUND_COLOR)
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])
            self.render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, self.render_scroll)
            self.player.update(self.tilemap,
                               ((self.movement[1] - self.movement[0]) * 2, 0))
            self.player.render(self.display, self.render_scroll)
            self.render_players(self.render_scroll)

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
                        self.player.velocity[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                        self.player.velocity[0] = 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    world_mouse_pos = (mouse_pos[0], mouse_pos[1])
                    direction = (world_mouse_pos[0] - WIDTH / 2, world_mouse_pos[1] - HEIGHT / 2)
                    length = math.sqrt(direction[0] * direction[0] + direction[1] * direction[1])
                    direction = (direction[0] / length, direction[1] / length)
                    if event.button == 3:
                        self.player.hook.shoot(direction)
                    if event.button == 1:
                        self.player.current_weapon.shoot(direction)
                        self.player.minigun.is_shooting = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.player.minigun.is_shooting = False
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:
                        self.player.switch_weapon(1)
                    elif event.y < 0:
                        self.player.switch_weapon(-1)

            self.send_player_info()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

    def send_player_info(self):
        self.player_info['x'] = self.player.pos[0]
        self.player_info['y'] = self.player.pos[1]
        self.player_info['is_rope_torn'] = self.player.hook.is_rope_torn
        self.player_info['hook_x'] = self.player.hook.pos[0]
        self.player_info['hook_y'] = self.player.hook.pos[1]
        self.player_info['direction'] = self.player.direction
        self.player_info['mouse_pos'] = self.player.mouse_pos
        self.player_info['weapon_index'] = self.player.weapons.index(self.player.current_weapon)
        self.player_info['bullets'] = [bullet.serialize() for bullet in self.player.bullets]
        self.player_info['hp'] = self.player.hp
        self.player_info['nickname'] = self.player.name
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
                    current_addresses = set(self.players_data.keys())
                    for addr in self.players.keys():
                        if addr not in current_addresses:
                            self.players.pop(addr)
                    for addr, pdata in self.players_data.items():
                        if addr not in self.players:
                            self.players[addr] = Player(self, (pdata['x'], pdata['y']), (10, 16))
                        else:
                            self.players[addr].pos = (pdata['x'], pdata['y'])
                            self.players[addr].direction = pdata['direction']
                            self.players[addr].hook.is_rope_torn = pdata['is_rope_torn']
                            self.players[addr].hook.pos = (pdata['hook_x'], pdata['hook_y'])
                            self.players[addr].mouse_pos = pdata['mouse_pos']
                            self.players[addr].current_weapon = self.players[addr].weapons[pdata['weapon_index']]
                            bullets = [self.deserialize_bullet(bullet) for bullet in pdata['bullets']]
                            self.players[addr].bullets = bullets
                            self.players[addr].hp = pdata['hp']
                            self.players[addr].name = pdata['nickname']
                            self.player.other_bullets = bullets
            except:
                pass

    def deserialize_bullet(self, bullet_info):
        pos = bullet_info['pos']
        direction = bullet_info['direction']
        if bullet_info['bullet_type'] == 'rpg':
            is_bullet_flipped = bullet_info['is_bullet_flipped']
            angle = bullet_info['angle']
            bullet = rpg_bullet.Bullet(self, pos, direction, is_bullet_flipped, angle)
            bullet.exploded = bullet_info['is_exploded']
            return bullet
        elif bullet_info['bullet_type'] == 'minigun':
            return minigun_bullet.Bullet(self, pos, direction)

    def render_players(self, render_scroll):
        for player in self.players.values():
            player.render(self.display, render_scroll)


if __name__ == "__main__":
    Game().run()


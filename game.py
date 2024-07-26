import pygame
import sys
import socket
import json
import threading
import math
import random

from main_menu.input_box import InputBox
from scripts.settings import *
from scripts.utils import load_sprite
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.tools.rpg import rpg_bullet
from scripts.tools.minigun import minigun_bullet
from main_menu.menu import MainMenu
from scripts.cheat_codes import cheat_cods


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Teeworlds Task')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.display = pygame.Surface((WIDTH / 2, HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'grass': load_sprite('tiles/grass.png'),
            'left_grass': load_sprite('tiles/left_grass.png'),
            'right_grass': load_sprite('tiles/right_grass.png'),
            'player': load_sprite('player.png'),
            'left_ground_wall': load_sprite('tiles/left_ground_wall.png'),
            'right_ground_wall': load_sprite('tiles/right_ground_wall.png'),
            'ground': load_sprite('tiles/ground.png'),
            'left_bottom_ground': load_sprite('tiles/left_bottom_ground.png'),
            'bottom_ground': load_sprite('tiles/bottom_ground.png'),
            'right_bottom_ground': load_sprite('tiles/right_bottom_ground.png'),
            'spawnpoint': None,
            'heal': load_sprite('tiles/heal.png')
        }

        self.tilemap = Tilemap(self, 16)
        with open('save.json', 'r', encoding='utf-8') as file:
            self.tilemap.tilemap = json.load(file)
        self.tilemap.find_spawnpoints()

        self.spawnpoint_pos = self.tilemap.spawnpoint_positions[random.randint(0, len(self.tilemap.spawnpoint_positions)) - 1]
        start_pos = [self.spawnpoint_pos[0] * 16, self.spawnpoint_pos[1] * 16]
        self.player = Player(self, start_pos, (10, 16))

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

        self.is_cheat_menu_active = False
        self.input_box = InputBox(5, 5, 300, 48, pygame.Color('black'),
                                  pygame.Color('darkslategrey'), self.screen)
        self.text_surface = (pygame.font.Font(None, 48).
                             render("Код неверный",
                                    True, (0, 0, 0)))
        self.text_rect = self.text_surface.get_rect(center=(WIDTH / 2, 100))
        self.is_warning_active = False

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
                if not self.is_cheat_menu_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == 96:
                            self.is_cheat_menu_active = True
                            self.input_box.text = ""
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

                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == 96:
                            self.is_cheat_menu_active = False
                            self.is_warning_active = False
                            self.input_box.text = ''
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN or self.input_box.is_enter_pressed:
                        input_text = self.input_box.text
                        if input_text not in cheat_cods:
                            self.is_warning_active = True
                        else:
                            self.is_cheat_menu_active = False
                            code = cheat_cods[input_text]
                            self.is_warning_active = False
                            if code == "immortality":
                                self.player.is_immortal = True
                            elif code == "full_hp":
                                self.player.hp = 100
                            elif code == "damage_up":
                                self.player.current_weapon.damage *= 2
                        self.input_box.is_enter_pressed = False
                        self.input_box.text = ""
                self.input_box.handle_event(event)
            self.input_box.update()

            self.send_player_info()
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            if self.is_cheat_menu_active:
                self.input_box.draw()
            if self.is_warning_active:
                self.screen.blit(self.text_surface, self.text_rect)
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
        self.player_info['id'] = self.player.id
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
                            self.players[addr].id = pdata['id']
                            self.player.other_bullets = bullets
            except:
                pass

    def deserialize_bullet(self, bullet_info):
        pos = bullet_info['pos']
        direction = bullet_info['direction']
        damage = bullet_info['damage']
        if bullet_info['bullet_type'] == 'rpg':
            is_bullet_flipped = bullet_info['is_bullet_flipped']
            angle = bullet_info['angle']
            bullet = rpg_bullet.Bullet(self, pos, direction, is_bullet_flipped, angle, damage)
            bullet.exploded = bullet_info['is_exploded']
            bullet.damaged_players = bullet_info['damaged_players']
            return bullet
        elif bullet_info['bullet_type'] == 'minigun':
            bullet = minigun_bullet.Bullet(self, pos, direction, damage)
            bullet.is_exist = bullet_info['is_exist']
            bullet.damaged_player = bullet_info['damaged_player']
            return bullet

    def render_players(self, render_scroll):
        for player in self.players.values():
            player.render(self.display, render_scroll)


if __name__ == "__main__":
    Game().run()


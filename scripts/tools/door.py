import math

import pygame
from scripts.utils import load_sprite


class Door:
    def __init__(self, pos, game):
        self.closed_image = load_sprite('tiles/closed_door.png')
        self.opened_image = load_sprite('tiles/opened_door.png')
        self.is_open = False
        self.pos = pos
        self.game = game
        self.center_coordinates = [pos[0] + 8, pos[1] + 16]
        self.can_be_closed = True
        self.door_kd = 60
        self.current_tick = 0

    def update(self):
        self.current_tick += 1
        self.can_be_closed = True
        if self.game.player.rect().colliderect(self.rect()):
            self.can_be_closed = False

        for player in self.game.players.values():
            if player.rect().colliderect(self.rect()):
                self.can_be_closed = False
        if self.distance_to_player(self.game.player) < 30 and self.game.player.is_e_active and self.current_tick > self.door_kd:
            self.current_tick = 0
            if not self.is_open:
                self.is_open = True
                self.game.tilemap.tilemap[f"{self.pos[0] // 16};{self.pos[1] // 16}"]["type"] = "opened_door"
            elif self.can_be_closed:
                self.is_open = False
                self.game.tilemap.tilemap[f"{self.pos[0] // 16};{self.pos[1] // 16}"]["type"] = "closed_door"
        else:
            for player in self.game.players.values():
                if self.distance_to_player(player) < 30 and player.is_e_active and self.current_tick > self.door_kd:
                    self.current_tick = 0
                    if not self.is_open:
                        self.is_open = True
                        self.game.tilemap.tilemap[f"{self.pos[0] // 16};{self.pos[1] // 16}"]["type"] = "opened_door"
                    elif self.can_be_closed:
                        self.is_open = False
                        self.game.tilemap.tilemap[f"{self.pos[0] // 16};{self.pos[1] // 16}"]["type"] = "closed_door"

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], *self.closed_image.get_rect().size)

    def distance_to_player(self, player):
        return math.sqrt((self.pos[0] - player.pos[0]) ** 2 + (self.pos[1] - player.pos[1]) ** 2)

    def render(self, surface, offset=(0, 0)):
        if self.is_open:
            surface.blit(self.opened_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        else:
            surface.blit(self.closed_image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))



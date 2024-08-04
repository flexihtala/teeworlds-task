import pygame
import math
from scripts.utils import load_sprite


class Bullet:
    def __init__(self, game, pos, direction, damage, range1=200, speed=10):
        self.game = game
        self.direction = direction
        self.image = load_sprite('tools/minigun/minigun_bullet.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_rect().width // 10,
                                             self.image.get_rect().height // 10))
        self.start_pos = list(pos)
        self.pos = self.start_pos[:]
        self.range = range1
        self.velocity = [direction[0] * speed, direction[1] * speed]
        self.size = (10, 10)
        self.is_exist = True
        self.damage = damage
        self.is_damaged = False
        self.damaged_player = -1

    def update(self, tilemap, _, is_enemy=False):
        # Move bullet
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        length = math.sqrt((self.pos[0] - self.start_pos[0]) ** 2 + (self.pos[1] - self.start_pos[1]) ** 2)
        if length > self.range:
            self.is_exist = False

        bullet_rect = pygame.Rect(self.pos[0], self.pos[1], *self.image.get_rect().size)
        # получение урона
        if is_enemy:
            if self.game.player.id == self.damaged_player:
                self.game.player.take_damage(self.damage)

        else:
            if self.is_damaged:
                self.damaged_player = -1
                self.is_exist = False
                return

            for player in self.game.players.values():
                if bullet_rect.colliderect(player.rect()):
                    self.damaged_player = player.id
                    self.is_damaged = True

        bullet_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if bullet_rect.colliderect(rect):
                self.is_exist = False
                return

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], *self.image.get_rect().size)

    def render(self, surface, offset=(0, 0)):
        if self.is_exist:
            surface.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def serialize(self):
        return {
            'pos': self.pos,
            'direction': self.direction,
            'bullet_type': 'minigun',
            'is_exist': self.is_exist,
            'damage': self.damage,
            'damaged_player': self.damaged_player,
        }

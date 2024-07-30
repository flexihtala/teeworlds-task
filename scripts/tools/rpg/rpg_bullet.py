import pygame
import math

from scripts.tools.rpg.bullet_explosion import Explosion
from scripts.utils import load_sprite


class Bullet:
    def __init__(self, game, pos, direction, is_bullet_flipped, angle, damage, range1=200, speed=5):
        self.game = game
        self.direction = direction
        self.image = load_sprite('tools/rpg/bullet_rpg.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_rect().width // 10,
                                             self.image.get_rect().height // 10))
        self.start_pos = list(pos)
        self.pos = self.start_pos[:]
        self.range = range1
        self.velocity = [direction[0] * speed, direction[1] * speed]
        self.size = (10, 10)
        self.exploding_radius = 50
        self.exploded = False
        self.is_exist = True
        self.angle = angle
        self.is_bullet_flipped = is_bullet_flipped
        self.explosion_group = pygame.sprite.Group()
        self.offset = (0, 0)
        self.damage = damage
        self.is_damaged = False
        self.damaged_players = []

    def update(self, tilemap, offset=(0, 0), is_enemy=False):
        if self.exploded:
            return
        bullet_rect = self.rect()
        if is_enemy and not self.is_damaged:
            if self.game.player.id in self.damaged_players:
                self.game.player.take_damage(self.damage)
                self.apply_explosion_force(self.game.player)
                self.is_damaged = True
                self.explode()

        else:
            if self.is_damaged:
                self.damaged_players = []
                self.explode()
                return

            for player in self.game.players.values():
                if bullet_rect.colliderect(player.rect()):
                    self.damaged_players.append(player.id)
                    self.is_damaged = True

        self.offset = offset

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        length = math.sqrt((self.pos[0] - self.start_pos[0]) ** 2 + (self.pos[1] - self.start_pos[1]) ** 2)
        if length > self.range:
            self.is_exist = False
        # Check for collisions with tiles
        if not self.is_damaged:
            for rect in tilemap.physics_rects_around(self.pos):
                if bullet_rect.colliderect(rect):
                    if is_enemy:
                        self.explode()
                        return
                    for player in self.game.players.values():
                        if self.distance_to(player.rect().center) <= self.exploding_radius:
                            self.damaged_players.append(player.id)
                    if self.distance_to(self.game.player.rect().center) <= self.exploding_radius:
                        self.apply_explosion_force(self.game.player)
                    self.is_damaged = True
                    return

    def explode(self):
        self.exploded = True
        explosion = Explosion(self.pos[0] - self.offset[0], self.pos[1] - self.offset[1], self)
        self.explosion_group.add(explosion)

    def apply_explosion_force(self, player):
        if player.immortality_time > 0:
            return
        dx = player.rect().center[0] - self.pos[0]
        dy = player.rect().center[1] - self.pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 1:
            distance = 2

        force = 10 / distance
        if force < 2:
            force = 2
        angle = math.atan2(dy, -dx)

        player.velocity[0] -= force * math.cos(angle)
        player.velocity[1] += force * math.sin(angle)

    def distance_to(self, point):
        return math.sqrt((self.pos[0] - point[0]) ** 2 + (self.pos[1] - point[1]) ** 2)

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], *self.image.get_rect().size)

    def render(self, surface, offset=(0, 0)):
        self.offset = offset
        if self.is_exist:
            if not self.exploded:
                if self.is_bullet_flipped:
                    image = pygame.transform.flip(self.image, True, False)
                else:
                    image = self.image

                surface.blit(pygame.transform.rotate(image, -self.angle),
                             (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            else:
                self.explosion_group.draw(surface)
                self.explosion_group.update()

    def serialize(self):
        return {
            'pos': self.pos,
            'direction': self.direction,
            'is_bullet_flipped': self.is_bullet_flipped,
            'angle': self.angle,
            'is_exploded': self.exploded,
            'bullet_type': 'rpg',
            'damage': self.damage,
            'damaged_players': self.damaged_players,
        }

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

    def update(self, tilemap, offset=(0, 0), is_enemy=False):
        if self.exploded:
            return
        bullet_rect = self.rect()
        if is_enemy:
            if bullet_rect.colliderect(self.game.player.rect()):
                self.explode(True)
                return
        self.offset = offset

        # Move bullet
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        length = math.sqrt((self.pos[0] - self.start_pos[0]) ** 2 + (self.pos[1] - self.start_pos[1]) ** 2)
        if length > self.range:
            self.is_exist = False
        for player in self.game.players.values():
            if bullet_rect.colliderect(player.rect()):
                self.explode(False)
                return
        # Check for collisions with tiles
        for rect in tilemap.physics_rects_around(self.pos):
            if bullet_rect.colliderect(rect):
                self.explode(is_enemy)
                return

    def explode(self, is_enemy):
        self.exploded = True
        explosion = Explosion(self.pos[0] - self.offset[0], self.pos[1] - self.offset[1], self)
        self.explosion_group.add(explosion)
        # Check for players within the explosion radius
        for player in self.game.players.values():
            if self.distance_to(player.rect().center) <= self.exploding_radius:
                self.apply_explosion_force(player)
        if self.distance_to((self.game.player_info['x'], self.game.player_info['y'])) <= self.exploding_radius:
            if self.game.player.immortality_time > 0:
                pass
            self.apply_explosion_force(self.game.player)
            if is_enemy:
                self.game.player.take_damage(self.damage)

    def apply_explosion_force(self, player):
        dx = player.rect().center[0] - self.pos[0]
        dy = player.rect().center[1] - self.pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 1:
            distance = 2

        force = 10 / distance  # Explosion force decreases with distance
        if force < 2:
            force = 2
        angle = math.atan2(dy, dx)

        player.velocity[0] += force * math.cos(angle)
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
        }

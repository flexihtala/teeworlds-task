import random

import pygame
from scripts.settings import WIDTH
from scripts.tools.rpg.rpg import Rpg
from scripts.tools.minigun.minigun import Minigun
from scripts.tools.hook import Hook


class Player:
    def __init__(self, game, pos, size):
        self.game = game
        self.name = ''
        self.pos = list(pos)
        self.mouse_pos = [0, 0]
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False,
                           'right': False, 'left': False}
        self.g = 0.03
        self.jumps = 0
        self.direction = 'right'
        self.max_hp = 100
        self.hp = self.max_hp

        self.rpg = Rpg(self.game, self)
        self.minigun = Minigun(self.game, self)
        self.weapons = [self.rpg, self.minigun]
        self.current_weapon = self.weapons[0]

        self.hook = Hook(self.game, self)
        self.bullets = []
        self.other_bullets = []
        self.immortality_time = 120
        self.is_immortal = False
        # todo норм айди
        self.id = random.randint(1, 10000)
        self.max_velocity = 2
        self.is_hiding = False
        self.is_e_active = False

    def update(self, tilemap, movement=(0, 0)):
        self.is_hiding = False
        self.immortality_time -= 1
        self.mouse_pos = pygame.mouse.get_pos()
        self.bullets = [bullet for bullet in self.bullets if bullet.is_exist]
        self.current_weapon.update(self.game.tilemap, self.game.render_scroll)
        for bullet in self.bullets:
            bullet.update(tilemap, self.game.render_scroll)
        for bullet in self.other_bullets:
            bullet.update(tilemap, self.game.render_scroll, True)

        self.hook.update(self.game.tilemap)

        self.collisions = {'up': False, 'down': False,
                           'right': False, 'left': False}
        if movement[0] < 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, -self.max_velocity)
        if movement[0] > 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, self.max_velocity)

        self.pos[0] += self.velocity[0]
        entity_rect = self.rect()
        for rect in tilemap.hiding_tiles_positions:
            if entity_rect.colliderect(rect):
                self.is_hiding = True
            else:
                self.is_hiding = False
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if self.velocity[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += self.velocity[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.jumps = 2
                if self.velocity[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        self.velocity[1] = min(5, self.velocity[1] + self.g)
        if self.collisions['down']:
            if abs(self.velocity[0]) < 0.2:
                self.velocity[0] = 0
            elif self.velocity[0] > 0:
                self.velocity[0] -= 0.2
            else:
                self.velocity[0] += 0.2
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        if pygame.mouse.get_pos()[0] > WIDTH // 2:
            self.direction = 'right'
        else:
            self.direction = 'left'

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1],
                           self.size[0], self.size[1])

    def render(self, surface, offset=(0, 0)):
        if self.hp < 1:
            return
        image = self.game.assets['player']
        if self.direction == 'right':
            image = pygame.transform.flip(image, True, False)
        if not self.is_hiding:
            surface.blit(image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            self.current_weapon.render(self.game.display, self.mouse_pos,
                                       self.game.render_scroll)
        self.hook.render(self.game.display, self.game.render_scroll)

        for bullet in self.bullets:
            bullet.render(surface, offset)
        for bullet in self.other_bullets:
            bullet.render(surface, offset)
        if not self.is_hiding:
            self.render_health_bar(surface, offset)
            self.render_name(surface, offset)

    def render_health_bar(self, surface, offset=(0, 0)):
        bar_width = 20
        bar_height = 5
        health_ratio = self.hp / self.max_hp
        health_bar_width = int(bar_width * health_ratio)

        health_bar_rect = pygame.Rect(self.pos[0] - offset[0] - (bar_width - self.size[0]) / 2,
                                      self.pos[1] - offset[1] - 10 + 3, bar_width, bar_height)
        current_health_rect = pygame.Rect(self.pos[0] - offset[0] - (bar_width - self.size[0]) / 2,
                                          self.pos[1] - offset[1] - 10 + 3, health_bar_width, bar_height)

        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(surface, (0, 255, 0), current_health_rect)

    def render_name(self, surface, offset=(0, 0)):
        render_name = pygame.font.Font(None, 16).render(self.name, True, (0, 0, 0))
        text_rect = render_name.get_rect(center=(self.pos[0] + 5, int(self.pos[1]) - 15))
        text_rect.x = int(text_rect.x - offset[0])
        text_rect.y = int(text_rect.y - offset[1])
        surface.blit(render_name, text_rect)

    def jump(self):
        if self.jumps:
            self.velocity[1] = -2
            self.jumps -= 1

    def take_damage(self, amount):
        print(self.immortality_time, self.is_immortal)
        if self.immortality_time > 0 or self.is_immortal:
            return
        self.hp -= amount
        print(self.hp)
        if self.hp < 1:
            self.hp = 0
            self.die()

    def switch_weapon(self, direction):
        current_index = self.weapons.index(self.current_weapon)
        new_index = (current_index + direction) % len(self.weapons)
        self.current_weapon = self.weapons[new_index]

    def die(self):
        spawn_point = self.game.tilemap.spawnpoint_positions[random.randint(0, len(self.game.tilemap.spawnpoint_positions)) - 1]
        self.pos = [spawn_point[0] * 16, spawn_point[1] * 16]
        self.hp = self.max_hp
        self.velocity = [0, 0]
        self.immortality_time = 120

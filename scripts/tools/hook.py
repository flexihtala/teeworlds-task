import pygame
import math


class Hook:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.pos = (0, 0)
        self.velocity = [0, 0]
        self.speed = 10
        self.length = 0
        self.is_hooked = False
        self.max_length = 200
        self.is_rope_torn = True
        self.tension_coefficient = 0.1  # коэффициент натяжения (увеличен для большей силы притяжения)

    def shoot(self, direction):
        if self.is_rope_torn:
            self.is_rope_torn = False
            self.pos = self.player.rect().center
            self.velocity = [direction[0] * self.speed, direction[1] * self.speed]
            self.length = 0

    def update(self, tilemap):
        if not pygame.mouse.get_pressed()[2]:
            self.is_rope_torn = True
            self.is_hooked = False

        if self.is_hooked and not self.is_rope_torn:
            self.pull_player()

        if not self.is_rope_torn and not self.is_hooked:
            self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
            self.length = math.sqrt((self.player.rect().center[0] - self.pos[0])**2 +
                                    (self.player.rect().center[1] - self.pos[1])**2)
            if self.length > self.max_length:
                self.is_rope_torn = True
                self.is_hooked = False

            for rect in tilemap.physics_rects_around(self.pos):
                if pygame.Rect(rect).collidepoint(self.pos):
                    self.is_hooked = True
                    break

    def pull_player(self):
        player_pos = self.player.rect().center
        hook_pos = self.pos

        dx = hook_pos[0] - player_pos[0]
        dy = hook_pos[1] - player_pos[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.max_length:
            self.is_rope_torn = True
            self.is_hooked = False
            return

        if distance > self.length:
            force = (distance - self.length) * self.tension_coefficient  # изменен коэффициент натяжения
            force_x = force * (dx / distance)
            force_y = force * (dy / distance)

            # Применяем силу натяжения
            self.player.velocity[0] += force_x
            self.player.velocity[1] += force_y
        else:
            # Обновление длины крюка
            self.length = distance

    def render(self, surface, scroll):
        if not self.is_rope_torn:
            pygame.draw.line(surface,
                             (255, 255, 255),
                             (self.player.rect().centerx - scroll[0], self.player.rect().centery - scroll[1]),
                             (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), 2)
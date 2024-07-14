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
        self.max_length = 100
        self.is_rope_torn = True
        self.ticks_count = 0

    def shoot(self, direction):
        if self.is_rope_torn:
            self.is_rope_torn = False
            self.pos = self.player.rect().center
            self.velocity = [direction[0] * self.speed, direction[1] * self.speed]
            self.length = 0

    def update(self, tilemap):
        self.ticks_count += 1
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
                self.is_hooked = False
                self.is_rope_torn = True

            for rect in tilemap.physics_rects_around(self.pos):
                if pygame.Rect(rect).collidepoint(self.pos):
                    self.is_hooked = True
                    self.player.velocity[1] = 0
                    self.ticks_count = 0
                    break

        else:
            self.length = math.sqrt((self.player.rect().center[0] - self.pos[0]) ** 2 +
                                    (self.player.rect().center[1] - self.pos[1]) ** 2)
            if self.length > self.max_length:
                self.is_rope_torn = True


    def pull_player(self):
        player_pos = self.player.rect().center
        alpha = math.degrees(math.atan2(player_pos[1] - self.pos[1],
                                        self.pos[0] - player_pos[0]))
        self.player.velocity[0] += (abs(
                self.player.g * math.cos(alpha)) if self.player.rect().center[0] < self.pos[0]
                else -abs(self.player.g * math.cos(alpha)))
        self.player.velocity[1] += (abs(
            self.player.g * math.sin(alpha)) if self.player.rect().center[0] < self.pos[0]
                                    else -abs(self.player.g * math.sin(alpha))) - self.player.g

        #self.player.pos[1] = math.sqrt(self.length ** 2 - self.player.pos[0] ** 2)

        """ Я уже не можу эту залупу писать
        player_pos = self.player.rect().center

        dx = self.pos[0] - player_pos[0]
        dy = self.pos[1] - player_pos[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        angle = math.atan2(dy, dx)



        tension = (self.length - distance) * 0.1  # 0.1 - коэффициент натяжения


        force_x = tension * math.cos(angle)
        force_y = tension * math.sin(angle)


        force_gravity = self.player.g


        total_force_x = force_x
        total_force_y = force_y + force_gravity


        acceleration_x = total_force_x
        acceleration_y = total_force_y


        self.player.velocity[0] -= acceleration_x
        self.player.velocity[1] -= acceleration_y"""

    def render(self, surface, scroll):
        if not self.is_rope_torn:
            pygame.draw.line(surface,
                             (255, 255, 255),
                             (self.player.rect().centerx - scroll[0], self.player.rect().centery - scroll[1]),
                             (self.pos[0] - scroll[0], self.pos[1] - scroll[1]), 2)

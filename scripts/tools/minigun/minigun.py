import math

import pygame
from scripts.utils import load_sprite
from scripts.settings import WIDTH, HEIGHT
from scripts.tools.weapon_rotate import get_rotated_parameters
from scripts.tools.minigun.minigun_bullet import Bullet


class Minigun:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.bullets = []
        # todo добавить удаление пуль, которые уже взорвались/исчезли
        self.image = load_sprite('tools/minigun/minigun.png')
        self.scale_mult = 10
        # координаты ключевой точки относительно левого верхнего угла картинки
        self.key_point = (30, 30)
        self.ticks = 0
        self.is_shooting = False
        self.angle = 0
        # Сила отталкивания
        self.force = 0.1

    def shoot(self, direction):
        if self.ticks > 5:
            self.ticks = 0
            bullet = Bullet(self.game, self.player.rect().center, direction)
            self.give_player_impulse()
            # todo сделать вылет пули из дула, а не из центра игрока(не обязательно, но желательно)
            self.bullets.append(bullet)

    def get_shooting_direction(self):
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - WIDTH / 2
        dy = mouse_pos[1] - HEIGHT / 2
        length = math.sqrt(dx * dx + dy * dy)
        direction = (dx / length, dy / length)
        return direction

    def update(self, tilemap, _):
        self.ticks += 1
        for bullet in self.bullets:
            bullet.update(tilemap)

        if self.is_shooting:
            direction = self.get_shooting_direction()
            self.shoot(direction)

    def give_player_impulse(self):
        self.player.velocity[0] -= self.force * math.cos(math.radians(self.angle))
        self.player.velocity[1] -= self.force * math.sin(math.radians(self.angle))

    def render(self, surface, mouse_coord, offset=(0, 0)):
        for bullet in self.bullets:
            bullet.render(surface, offset)

        center_x, center_y = self.player.rect().center
        scaled_image = pygame.transform.scale(self.image,
                                              (self.image.get_rect().width / self.scale_mult,
                                               self.image.get_rect().height / self.scale_mult))
        # угол поворота
        dx = mouse_coord[0] - WIDTH / 2
        dy = mouse_coord[1] - HEIGHT / 2
        angle = math.degrees(math.atan2(dy, dx))
        self.angle = angle

        # Отражаем картинку относительно оси Oy, меняем координаты "рычага поворота"
        if mouse_coord[0] < WIDTH / 2:
            flipped_image = pygame.transform.flip(scaled_image, True, False)
            angle -= 180
            origin_pos = ((223 - self.key_point[0]) / self.scale_mult,
                          (59 - self.key_point[1]) / self.scale_mult)
        else:
            flipped_image = scaled_image
            origin_pos = (self.key_point[0] / self.scale_mult,
                          self.key_point[1] / self.scale_mult)

        surface.blit(*get_rotated_parameters(flipped_image, (center_x - offset[0], center_y - offset[1] + 4),
                                             origin_pos, -angle))
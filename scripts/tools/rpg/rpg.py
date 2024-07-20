import pygame
import math
from scripts.utils import load_sprite
from scripts.settings import WIDTH, HEIGHT
from scripts.tools.weapon_rotate import get_rotated_parameters
from scripts.tools.rpg.rpg_bullet import Bullet


class Rpg:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        # todo добавить удаление пуль, которые уже взорвались/исчезли
        self.image = load_sprite('tools/rpg/rpg.png')
        self.scale_mult = 10
        # координаты ключевой точки относительно левого верхнего угла картинки
        self.key_point = (30, 30)
        self.ticks = 0
        # угол нужен для поворота изображения пули
        self.angle = 0
        # отражена ли пуля по оси Ох
        self.is_bullet_flipped = False

    def shoot(self, direction):
        if self.ticks > 60:
            self.ticks = 0
            bullet = Bullet(self.game, self.player.rect().center, direction, self.is_bullet_flipped, self.angle)
            # todo сделать вылет пули из дула, а не из центра игрока(не обязательно, но желательно)
            self.player.bullets.append(bullet)

    def update(self, tilemap, offset=(0, 0)):
        self.ticks += 1

    def render(self, surface, mouse_coord, offset=(0, 0)):
        center_x, center_y = self.player.rect().center
        scaled_image = pygame.transform.scale(self.image,
                                              (self.image.get_rect().width / self.scale_mult,
                                               self.image.get_rect().height / self.scale_mult))
        # угол поворота
        dx = mouse_coord[0] - WIDTH / 2
        dy = mouse_coord[1] - HEIGHT / 2
        angle = math.degrees(math.atan2(dy, dx))

        # Отражаем картинку относительно оси Oy, меняем координаты "рычага поворота"
        if mouse_coord[0] < WIDTH / 2:
            flipped_image = pygame.transform.flip(scaled_image, True, False)
            angle -= 180
            origin_pos = ((223 - self.key_point[0]) / self.scale_mult,
                          (59 - self.key_point[1]) / self.scale_mult)
            self.is_bullet_flipped = True
        else:
            flipped_image = scaled_image
            origin_pos = (self.key_point[0] / self.scale_mult,
                          self.key_point[1] / self.scale_mult)
            self.is_bullet_flipped = False
        self.angle = angle

        surface.blit(*get_rotated_parameters(flipped_image, (center_x - offset[0], center_y - offset[1] + 4),
                                             origin_pos, -angle))

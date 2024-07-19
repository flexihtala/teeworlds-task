import pygame
import math
from scripts.utils import load_sprite
from scripts.settings import WIDTH, HEIGHT
from scripts.tools.weapon_rotate import get_rotated_parameters


class Rpg:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.bullets = []
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
            self.bullets.append(bullet)

    def update(self, tilemap):
        self.ticks += 1
        for bullet in self.bullets:
            bullet.update(tilemap)

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


class Bullet:
    def __init__(self, game, pos, direction, is_bullet_flipped, angle, range1=200, speed=5):
        self.game = game
        self.image = load_sprite('tools/rpg/bullet_rpg.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.image.get_rect().width // 10,
                                             self.image.get_rect().height // 10))
        self.start_pos = list(pos)
        self.pos = self.start_pos[:]
        self.range = range1
        self.velocity = [direction[0] * speed, direction[1] * speed]
        self.size = (10, 10)
        self.exploding_radius = 30
        self.exploded = False
        self.is_exist = True
        self.angle = angle
        self.is_bullet_flipped = is_bullet_flipped
        self.explosion_group = pygame.sprite.Group()
        self.offset = (0, 0)

    def update(self, tilemap):
        if self.exploded:
            return

        # Move bullet
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        length = math.sqrt((self.pos[0] - self.start_pos[0]) ** 2 + (self.pos[1] - self.start_pos[1]) ** 2)
        if length > self.range:
            self.is_exist = False

        # Check for collisions with tiles
        bullet_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if bullet_rect.colliderect(rect):
                self.explode()
                return

    def explode(self):
        self.exploded = True
        explosion = Explosion(self.pos[0] - self.offset[0], self.pos[1] - self.offset[1])
        self.explosion_group.add(explosion)
        # Check for players within the explosion radius
        for player in self.game.players.values():
            print(f'player{player.rect().center}')
            if self.distance_to(player.rect().center) <= self.exploding_radius:
                print('go')
                self.apply_explosion_force(player)
        if self.distance_to((self.game.player_info['x'], self.game.player_info['y'])) <= self.exploding_radius:
            self.apply_explosion_force(self.game.player)

    def apply_explosion_force(self, player):
        dx = player.rect().center[0] - self.pos[0]
        dy = player.rect().center[1] - self.pos[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            distance = 10

        force = 10 / distance  # Explosion force decreases with distance
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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"assets/sprites/tools/rpg/exploding/exp{num}.png")
            img = pygame.transform.scale(img, (40, 40))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

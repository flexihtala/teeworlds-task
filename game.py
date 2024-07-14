import pygame
import sys
import math
from scripts.settings import *
from scripts.utils import load_sprite
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.tools.hook import Hook


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Teeworlds Task')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.display = pygame.Surface((WIDTH / 2, HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.player = PhysicsEntity(self, (50, 50), (10, 16))

        self.movement = [False, False]

        self.assets = {
            'grass': load_sprite('tiles/grass.png'),
            'player': load_sprite('player.png')
        }

        self.tilemap = Tilemap(self, 16)

        self.scroll = [0, 0]
        self.camera_speed = 30
        self.hook = Hook(self, self.player)

    def run(self):
        while True:
            self.display.fill(BACKGROUND_COLOR)
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1])
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, render_scroll)
            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * 2, 0))
            self.player.render(self.display, render_scroll)

            self.hook.update(self.tilemap)
            self.hook.render(self.display, render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        mouse_pos = pygame.mouse.get_pos()
                        world_mouse_pos = (mouse_pos[0], mouse_pos[1])
                        direction = (world_mouse_pos[0] - WIDTH / 2, world_mouse_pos[1] - HEIGHT / 2)
                        length = math.sqrt(direction[0] * direction[0] + direction[1] * direction[1])
                        direction = (direction[0] / length, direction[1] / length)
                        self.hook.shoot(direction)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()

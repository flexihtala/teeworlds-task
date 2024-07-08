import pygame
import sys
from scripts.settings import *
from scripts.utils import load_sprite
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Teeworlds Task')

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT))

        self.display = pygame.Surface(
            (WIDTH / 2, HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.player = PhysicsEntity(self, (50, 50), (10, 16))

        self.movement = [False, False]

        self.assets = {
            'grass': load_sprite('tiles/grass.png'),
            'player': load_sprite('player.png')
        }

        self.tilemap = Tilemap(self, 16)

    def run(self):
        while True:
            self.display.fill(BACKGROUND_COLOR)
            self.tilemap.render(self.display)
            self.player.update(self.tilemap, ((self.movement[1] - self.movement[0]) * 2, 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()

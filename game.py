import pygame
import sys
import settings
import utils
from entities import PhysicsEntity


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Teeworlds Task')

        self.screen = pygame.display.set_mode(
            (settings.WIDTH, settings.HEIGHT))

        self.display = pygame.Surface(
            (settings.WIDTH / 2, settings.HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.player = PhysicsEntity(self, (50, 50), (15, 32))

        self.movement = [False, False]

        self.assets = {
            'player': utils.load_sprite('player.png')
        }

    def run(self):
        while True:
            self.display.fill(settings.BACKGROUND_COLOR)
            self.player.update(((self.movement[1] - self.movement[0]) * 2, 0))
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
            self.clock.tick(settings.FPS)


if __name__ == "__main__":
    Game().run()

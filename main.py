import pygame
import sys
from player import Player
import settings


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.update()
            self.screen.fill(settings.BACKGROUND_COLOR)
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(settings.FPS)



if __name__ == "__main__":
    Game().run()

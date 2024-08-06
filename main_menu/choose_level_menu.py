import sys

import pygame
from main_menu.buttons import ImageButton
from scripts.settings import WIDTH, HEIGHT


class LevelMenu:
    def __init__(self, screen):
        self.screen = screen
        self.first_button = ImageButton(WIDTH // 2 - 126, 200, 252, 74, '', "assets/main_menu/level_buttons/World.png")
        self.second_button = ImageButton(WIDTH // 2 - 126, 300, 252, 74, '', "assets/main_menu/level_buttons/gray.png")
        self.third_button = ImageButton(WIDTH // 2 - 126, 400, 252, 74, '', "assets/main_menu/level_buttons/Your.png")
        self.main_background = [pygame.transform.scale(pygame.image.load(f"assets/main_menu/background/{i + 1}.png"),
                                                       (WIDTH, HEIGHT)) for i in range(4)]
        self.text_surface = (pygame.font.Font(None, 64).
                             render("Выберите уровень.",
                                    True, (0, 0, 0)))
        self.text_rect = self.text_surface.get_rect(center=(WIDTH / 2 + 20, 120))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.USEREVENT and event.button == self.first_button:
                    return 'map1'
                if event.type == pygame.USEREVENT and event.button == self.second_button:
                    return 'map2'
                if event.type == pygame.USEREVENT and event.button == self.third_button:
                    return 'save'
                self.first_button.handle_event(event)
                self.second_button.handle_event(event)
                self.third_button.handle_event(event)

            self.screen.fill((0, 0, 0))
            for i in self.main_background:
                self.screen.blit(i, (0, 0))
            for btn in [self.first_button, self.second_button, self.third_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen)
            self.screen.blit(self.text_surface, self.text_rect)
            pygame.display.flip()


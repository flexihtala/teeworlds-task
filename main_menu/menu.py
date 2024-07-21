import pygame
import sys
from scripts.settings import WIDTH, HEIGHT
from main_menu.buttons import ImageButton
from main_menu.input_name_menu import InputNameMenu


class MainMenu:
    def __init__(self, screen):
        # задний фон
        self.main_background = [pygame.transform.scale(pygame.image.load(f"assets/main_menu/background/{i + 1}.png"),
                                                       (WIDTH, HEIGHT)) for i in range(4)]
        self.screen = screen

    def main_menu(self):
        start_button = ImageButton(WIDTH/2-(252/2), 250, 252, 74, "", "assets/main_menu/start_button.png")
        exit_button = ImageButton(WIDTH / 2 - (252 / 2), 350, 252, 74, "", "assets/main_menu/exit_button.png")

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for i in self.main_background:
                self.screen.blit(i, (0, 0))

            font = pygame.font.Font(None, 72)
            text_surface = font.render("TEEWORLDS", True, (0, 0, 255))
            text_rect = text_surface.get_rect(center=(WIDTH/2, 100))
            self.screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == exit_button:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT and event.button == start_button:
                    name = InputNameMenu(self.screen).run()
                    if name == "ENDofTHEprogramGG":
                        pygame.quit()
                        sys.exit()
                    running = False
                    return name

                for btn in [start_button, exit_button]:
                    btn.handle_event(event)

            for btn in [start_button, exit_button]:
                btn.check_hover(pygame.mouse.get_pos())
                btn.draw(self.screen)

            pygame.display.flip()

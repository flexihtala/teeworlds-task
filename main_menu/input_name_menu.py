import pygame
from main_menu.buttons import ImageButton
from scripts.settings import WIDTH, HEIGHT
from main_menu.input_box import InputBox


class InputNameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.input_box = InputBox(WIDTH / 3 - 20, 200, 300, 64, pygame.Color('black'),
                                  pygame.Color('darkslategrey'), self.screen)
        self.main_background = [pygame.transform.scale(pygame.image.load(f"assets/main_menu/background/{i + 1}.png"),
                                                       (WIDTH, HEIGHT)) for i in range(4)]
        self.input_text = ""
        self.start_button = ImageButton(WIDTH / 2 - (252 / 2), 300, 252, 74, "", "assets/main_menu/start_button.png")
        self.is_warning_active = False
        self.text_surface = (pygame.font.Font(None, 32).
                             render("Имя не может быть пустым.",
                                    True, (255, 255, 255)))
        self.text_rect = self.text_surface.get_rect(center=(WIDTH / 2, 100))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "ENDofTHEprogramGG"
                if (event.type == pygame.USEREVENT and event.button == self.start_button or
                        self.input_box.is_enter_pressed):
                    self.input_text = self.input_box.text
                    if len(self.input_text) == 0 or len(self.input_text) > 10:
                        self.is_warning_active = True
                    else:
                        running = False

                self.start_button.handle_event(event)
                self.input_box.handle_event(event)

            self.input_box.update()

            self.screen.fill((0, 0, 0))
            for i in self.main_background:
                self.screen.blit(i, (0, 0))
            self.input_box.draw()
            self.start_button.check_hover(pygame.mouse.get_pos())
            self.start_button.draw(self.screen)
            if self.is_warning_active:
                self.screen.blit(self.text_surface, self.text_rect)
            pygame.display.flip()
        return self.input_text

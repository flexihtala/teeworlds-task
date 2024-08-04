import pygame


class InputBox:

    def __init__(self, x, y, w, h, active_color, inactive_color, screen, text=''):
        self.width = w
        self.rect = pygame.Rect(x, y, w, h)
        self.current_color = active_color
        self.active_color = active_color
        self.text = text
        self.screen = screen
        self.font = pygame.font.Font(None, 64)
        self.txt_surface = self.font.render(text, True, self.current_color)
        self.is_enter_pressed = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.is_enter_pressed = True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == 96:
                return
            elif len(self.text) < 10:
                self.text += event.unicode

            self.txt_surface = self.font.render(self.text, True, self.current_color)

    def update(self):
        width = max(self.width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        self.txt_surface = self.font.render(self.text, True, self.current_color)
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(self.screen, self.current_color, self.rect, 2)

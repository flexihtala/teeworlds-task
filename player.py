import pygame
import settings


class Player:
    def __init__(self):
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (settings.WIDTH // 2, settings.HEIGHT // 2)
        self.vel_y = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= settings.PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += settings.PLAYER_SPEED
        if keys[pygame.K_SPACE] and self.rect.bottom >= settings.HEIGHT:
            self.vel_y = -settings.JUMP_HEIGHT
        self.vel_y += settings.GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom > settings.HEIGHT:
            self.rect.bottom = settings.HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.rect)

import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet):
        pygame.sprite.Sprite.__init__(self)
        self.bullet = bullet
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
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
            self.bullet.is_exist = False
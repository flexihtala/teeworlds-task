import pygame

from scripts.utils import load_sprite


class HealPotion:
    def __init__(self, pos, game):
        self.pos = pos
        self.game = game
        self.is_active = True
        self.timer = 0
        self.active_timer = 300
        self.image = load_sprite('tiles/heal.png')
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.heal_power = 40

    def update(self):
        self.timer += 1
        if self.timer >= self.active_timer:
            self.is_active = True
        if self.is_active:
            heal_rect = self.rect()
            for player in self.game.players.values():
                if heal_rect.colliderect(player.rect()):
                    if player.hp < player.max_hp:
                        self.is_active = False
                        self.timer = 0
            if self.game.player.rect().colliderect(heal_rect):
                print(1)
                if self.game.player.hp < self.game.player.max_hp:
                    self.game.player.hp = min(self.game.player.max_hp, self.game.player.hp + self.heal_power)
                    self.is_active = False
                    self.timer = 0

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], *self.image.get_rect().size)

    def render(self, surface, offset=(0, 0)):
        if self.is_active:
            surface.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

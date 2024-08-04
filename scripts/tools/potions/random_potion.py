import pygame
from random import choice
from scripts.utils import load_sprite


class RandomPotion:
    def __init__(self, pos, game):
        self.pos = pos
        self.game = game
        self.is_active = True
        self.timer = 0
        self.active_timer = 600
        self.image = load_sprite('tiles/random_potion.png')
        self.image = pygame.transform.scale(self.image, (16, 16))
        self.all_buffs = {
            "speed_up": "Скорость увеличена",
            "immortality": "Временная неуязвимость",
            "damage_up": "Урон увеличен"}
        self.current_buff = choice(list(self.all_buffs.keys()))
        self.buff_timer = 0
        self.buff_timer_max = 300  # время баффа
        self.is_buff_active = False
        self.is_text_active = False
        self.text = ""
        self.text_color = tuple(choice(range(255)) for _ in range(3))

    def update(self):
        self.timer += 1
        if self.is_buff_active:
            self.buff_timer += 1
            if self.buff_timer >= self.buff_timer_max // 2:
                self.is_text_active = False
            if self.buff_timer >= self.buff_timer_max:
                self.is_buff_active = False
                self.apply_debuff()
        if self.timer >= self.active_timer:
            self.is_active = True
            self.current_buff = choice(list(self.all_buffs.keys()))
        if self.is_active:
            random_potion_rect = self.rect()
            for player in self.game.players.values():
                if random_potion_rect.colliderect(player.rect()):
                    self.is_active = False
                    self.timer = 0
            if self.game.player.rect().colliderect(random_potion_rect):
                self.is_active = False
                self.timer = 0
                self.buff_timer = 0
                self.apply_buff()

    def apply_buff(self):
        self.is_buff_active = True
        print("buff" + self.current_buff)
        if self.current_buff == "speed_up":
            self.game.player.max_velocity = 4
        elif self.current_buff == "immortality":
            self.game.player.immortality_time = 10 ** 5
        elif self.current_buff == "damage_up":
            self.game.player.rpg.damage *= 2
            self.game.player.minigun.damage *= 2
        self.is_text_active = True
        self.text = self.all_buffs[self.current_buff]

    def apply_debuff(self):
        print("debuff" + self.current_buff)
        if self.current_buff == "speed_up":
            self.game.player.max_velocity = 2
        elif self.current_buff == "immortality":
            self.game.player.immortality_time = 0
        elif self.current_buff == "damage_up":
            self.game.player.rpg.damage //= 2
            self.game.player.minigun.damage //= 2

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], *self.image.get_rect().size)

    def render(self, surface, offset=(0, 0)):
        if self.is_active:
            surface.blit(self.image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        if self.is_text_active:
            print(self.text)
            render_text = pygame.font.Font(None, 28).render(self.text, True, self.text_color)
            text_rect = render_text.get_rect(center=(self.pos[0] + 5, int(self.pos[1]) - 40))
            text_rect.x = int(text_rect.x - offset[0])
            text_rect.y = int(text_rect.y - offset[1])
            surface.blit(render_text, text_rect)

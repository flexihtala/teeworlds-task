import pygame
from scripts.settings import WIDTH


class PhysicsEntity:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False,
                           'right': False, 'left': False}
        self.g = 0.03
        self.jumps = 0
        self.direction = 'right'

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False,
                           'right': False, 'left': False}
        if movement[0] < 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, -2)
        if movement[0] > 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, 2)

        self.pos[0] += self.velocity[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if self.velocity[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += self.velocity[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                    self.jumps = 2
                if self.velocity[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        self.velocity[1] = min(5, self.velocity[1] + self.g)
        if self.collisions['down']:
            if abs(self.velocity[0]) < 0.2:
                self.velocity[0] = 0
            elif self.velocity[0] > 0:
                self.velocity[0] -= 0.2
            else:
                self.velocity[0] += 0.2
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        if pygame.mouse.get_pos()[0] > WIDTH // 2:
            self.direction = 'right'
        else:
            self.direction = 'left'

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1],
                           self.size[0], self.size[1])

    def render(self, surface, offset=(0, 0)):
        image = self.game.assets['player']
        if self.direction == 'right':
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def jump(self):
        if self.jumps:
            self.velocity[1] = -2
            self.jumps -= 1

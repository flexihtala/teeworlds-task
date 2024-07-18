import pygame
import sys
import math

G = 1  # гравитация


class Ball:
    def __init__(self, pos, rect_center, radius=50):
        self.pos = pos
        self.radius = radius
        self.mass = 10
        self.start_pos = self.pos.copy()
        self.rect_center = rect_center
        self.rope_length = self.calculate_distance(self.pos, self.rect_center)

        # Углы и угловая скорость для маятника
        self.angle = math.pi / 4  # начальный угол (в радианах)
        self.angular_velocity = 0
        self.angular_acceleration = 0
        self.damping = 0.995  # коэффициент трения для замедления
        self.attraction_rate = 0.5  # скорость уменьшения длины нити

    def calculate_distance(self, pos1, pos2):
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    def update(self):
        # Угловое ускорение (влияние гравитации)
        self.angular_acceleration = (-G / self.rope_length) * math.sin(
            self.angle)
        # Обновление угловой скорости с учетом трения
        self.angular_velocity += self.angular_acceleration
        self.angular_velocity *= self.damping
        # Обновление угла
        self.angle += self.angular_velocity

        # Уменьшение длины нити
        self.rope_length -= self.attraction_rate
        if self.rope_length < 50:  # минимальная длина нити
            self.rope_length = 50

        # Обновление позиции шара
        self.pos[0] = self.rect_center[0] + self.rope_length * math.sin(
            self.angle)
        self.pos[1] = self.rect_center[1] + self.rope_length * math.cos(
            self.angle)

    def render(self, surface):
        pygame.draw.circle(surface, 'red', self.pos, self.radius)


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
rect = pygame.Rect(375, 75, 50, 50)
ball = Ball([200, 200], rect.center)

while True:
    screen.fill('black')
    pygame.draw.line(screen, 'white', ball.pos, rect.center)
    pygame.draw.rect(screen, 'blue', rect)
    ball.render(screen)
    ball.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                ball.angular_velocity -= 0.1  # толчок влево
            if event.key == pygame.K_d:
                ball.angular_velocity += 0.1  # толчок вправо

    pygame.display.update()
    clock.tick(60)

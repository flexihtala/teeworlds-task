import pygame
import math

# Инициализация Pygame
pygame.init()


def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Загружаем изображение оружия
weapon_image = pygame.transform.scale(pygame.image.load('rpg/rpg.png'), (24, 6))
weapon_width, weapon_height = weapon_image.get_size()

# Координаты рукоятки относительно изображения
origin_pos = (3, 3)

# Координаты центра экрана
center_x, center_y = screen_width // 2, screen_height // 2

# Основная игровая петля
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получаем положение курсора
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Вычисляем угол поворота
    dx = mouse_x - center_x
    dy = mouse_y - center_y
    angle = math.degrees(math.atan2(dy, dx))
    if pygame.mouse.get_pos()[0] < screen.get_width() / 2:
        image1 = pygame.transform.flip(weapon_image, True, False)
        angle -= 180
        origin_pos = (20, 3)
    else:
        image1 = weapon_image
        origin_pos = (3, 3)
    screen.fill((0,0,0))
    blitRotate(screen, image1, (center_x, center_y), origin_pos, -angle)
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()

import pygame


def get_rotated_parameters(image, pos, origin_pos, angle):
    """Сложный страшный метод, писал 2 часа, добивал при помощи китайца со стаковерфлоу,
         высчитывает координаты повернутой фигуры image на угол angle
         pos - финальная позиция на экране,
         origin_pos - позиция точки поворота относительно верхнего левого угла исходной картинки"""
    image_rect = image.get_rect(topleft=(pos[0] - origin_pos[0], pos[1] - origin_pos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    return rotated_image, rotated_image_rect
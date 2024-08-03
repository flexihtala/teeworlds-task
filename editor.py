import pygame
import sys
import json
from scripts.utils import load_sprite
from scripts.tile_button import TileButton
from scripts.tilemap import Tilemap


class Editor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800 + 300, 600 + 200))
        self.display = pygame.Surface((400 + 150, 300 + 100))
        pygame.display.set_caption('Level Editor')

        self.scroll_horizontal = [False, False]
        self.scroll_vertical = [False, False]
        self.offset = [0, 0]

        self.rows = 50
        self.cols = 50
        self.tile_size = 16

        self.assets = {
            'grass': load_sprite('tiles/grass.png'),
            'left_grass': load_sprite('tiles/left_grass.png'),
            'right_grass': load_sprite('tiles/right_grass.png'),
            'left_ground_wall': load_sprite('tiles/left_ground_wall.png'),
            'right_ground_wall': load_sprite('tiles/right_ground_wall.png'),
            'ground': load_sprite('tiles/ground.png'),
            'left_bottom_ground': load_sprite('tiles/left_bottom_ground.png'),
            'bottom_ground': load_sprite('tiles/bottom_ground.png'),
            'right_bottom_ground': load_sprite('tiles/right_bottom_ground.png'),
            'top_brick': load_sprite('tiles/top_brick.png'),
            'top_left_brick': load_sprite('tiles/top_left_brick.png'),
            'top_right_brick': load_sprite('tiles/top_right_brick.png'),
            'left_brick': load_sprite('tiles/left_brick.png'),
            'mid_brick': load_sprite('tiles/mid_brick.png'),
            'right_brick': load_sprite('tiles/right_brick.png'),
            'bottom_brick': load_sprite('tiles/bottom_brick.png'),
            'bottom_left_brick': load_sprite('tiles/bottom_left_brick.png'),
            'bottom_right_brick': load_sprite('tiles/bottom_right_brick.png'),
            'spawnpoint': load_sprite('tiles/spawnpoint.png'),
            'heal': load_sprite('tiles/heal.png'),
            'random_potion': load_sprite('tiles/random_potion.png')
        }

        self.buttons = {}
        self.fill_buttons_list()
        self.current_tile = None

        self.tilemap = Tilemap(self)

        self.is_left_hold = False
        self.is_right_hold = False
        self.spawnpoints = set()

    def fill_buttons_list(self):
        i = 0
        j = 0
        for asset in self.assets.items():
            self.buttons[asset[0]] = TileButton(425 + j, (i // 2) * 32 + 16, asset[1], 1.5)
            i += 1
            j = 32 * (i % 2)

    def draw_grid(self):
        for col in range(self.cols + 1):
            pygame.draw.line(self.display, 'white',
                             (col * self.tile_size - self.offset[0], 0),
                             (col * self.tile_size - self.offset[0], 600))
        for row in range(self.rows):
            pygame.draw.line(self.display, 'white',
                             (0, row * self.tile_size - self.offset[1]),
                             (400, row * self.tile_size - self.offset[1]))

    def place_tile(self, remove_tile=False):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > 800 or mouse_pos[1] > 600 or self.current_tile is None:
            return
        tile_pos = ((mouse_pos[0] + 2 * self.offset[0]) // 32,
                    (mouse_pos[1] + 2 * self.offset[1]) // 32)
        tilemap_key = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if not remove_tile:
            self.tilemap.tilemap[tilemap_key] = {'type': self.current_tile,
                                                 'pos': tile_pos}
            if self.current_tile == 'spawnpoint':
                self.spawnpoints.add(tilemap_key)
        else:
            self.tilemap.tilemap.pop(tilemap_key, None)
            if self.current_tile == 'spawnpoint' and tilemap_key in self.spawnpoints:
                self.spawnpoints.remove(tilemap_key)

    def run(self):
        while True:
            print(self.offset)
            self.display.fill((14, 219, 248))
            self.draw_grid()
            self.tilemap.render(self.display, True, self.offset)
            pygame.draw.rect(self.display, 'gray',
                             pygame.Rect(0, 304, 400, 100))
            pygame.draw.rect(self.display, 'gray',
                             pygame.Rect(400, 0, 150, 450))
            for button in self.buttons:
                self.buttons[button].draw(self.display)
                if self.buttons[button].clicked:
                    self.current_tile = button

            if self.current_tile is not None:
                pygame.draw.rect(self.display, 'red', self.buttons[self.current_tile].rect, 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.scroll_horizontal[0] = True
                    if event.key == pygame.K_d:
                        self.scroll_horizontal[1] = True
                    if event.key == pygame.K_w:
                        self.scroll_vertical[0] = True
                    if event.key == pygame.K_s:
                        self.scroll_vertical[1] = True
                    if event.key == pygame.K_c:
                        if not self.spawnpoints:
                            print('Невозможно сохранить карту без спавнпоинтов')
                        else:
                            print('Saving')
                            with open('save.json', 'w', encoding='utf-8') as file:
                                json.dump(self.tilemap.tilemap, file)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.scroll_horizontal[0] = False
                    if event.key == pygame.K_d:
                        self.scroll_horizontal[1] = False
                    if event.key == pygame.K_w:
                        self.scroll_vertical[0] = False
                    if event.key == pygame.K_s:
                        self.scroll_vertical[1] = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.is_left_hold = True
                    if event.button == 3:
                        self.is_right_hold = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.is_left_hold = False
                    if event.button == 3:
                        self.is_right_hold = False

            if self.is_left_hold:
                self.place_tile()
            if self.is_right_hold:
                self.place_tile(remove_tile=True)

            if self.scroll_horizontal[0]:
                self.offset = [max(self.offset[0] - 1, 0), self.offset[1]]
            if self.scroll_horizontal[1]:
                self.offset = [min(self.offset[0] + 1, 400), self.offset[1]]
            if self.scroll_vertical[0]:
                self.offset = [self.offset[0], max(self.offset[1] - 1, 0)]
            if self.scroll_vertical[1]:
                self.offset = [self.offset[0], min(self.offset[1] + 1, 400)]
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0))
            pygame.display.update()


if __name__ == '__main__':
    Editor().run()

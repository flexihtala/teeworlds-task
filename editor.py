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

        self.scroll = [False, False]
        self.offset = 0

        self.rows = 20
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
            'spawnpoint': load_sprite('tiles/spawnpoint.png'),
            'heal': load_sprite('tiles/heal.png')
        }

        self.buttons = {}
        self.fill_buttons_list()
        self.current_tile = None

        self.tilemap = Tilemap(self)

        self.is_left_hold = False
        self.is_right_hold = False

    def fill_buttons_list(self):
        i = 0
        j = 0
        for asset in self.assets.items():
            self.buttons[asset[0]] = TileButton(425 + j, (i // 2) * 48 + 16, asset[1], 2)
            i += 1
            j = 48 * (i % 2)

    def draw_grid(self):
        for col in range(self.cols + 1):
            pygame.draw.line(self.display, 'white',
                             (col * self.tile_size - self.offset, 0),
                             (col * self.tile_size - self.offset, 600))
        for row in range(self.rows):
            pygame.draw.line(self.display, 'white',
                             (0, row * self.tile_size),
                             (400, row * self.tile_size))

    def place_tile(self, remove_tile=False):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > 800 or mouse_pos[1] > 600 or self.current_tile is None:
            return
        tile_pos = ((mouse_pos[0] + 2 * self.offset) // 32, mouse_pos[1] // 32)
        tilemap_key = str(tile_pos[0]) + ';' + str(tile_pos[1])
        if not remove_tile:
            self.tilemap.tilemap[tilemap_key] = {'type': self.current_tile,
                                                 'pos': tile_pos}
        else:
            self.tilemap.tilemap.pop(tilemap_key, None)


    def run(self):
        while True:
            self.display.fill((14, 219, 248))
            self.draw_grid()
            self.tilemap.render(self.display, [self.offset, 0])
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
                        self.scroll[0] = True
                    if event.key == pygame.K_d:
                        self.scroll[1] = True
                    if event.key == pygame.K_s:
                        print('Saving')
                        with open('save.json', 'w', encoding='utf-8') as file:
                            json.dump(self.tilemap.tilemap, file)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.scroll[0] = False
                    if event.key == pygame.K_d:
                        self.scroll[1] = False

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

            if self.scroll[0]:
                self.offset = max(self.offset - 1, 0)
            if self.scroll[1]:
                self.offset = min(self.offset + 1, 400)
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                (0, 0))
            pygame.display.update()


if __name__ == '__main__':
    Editor().run()

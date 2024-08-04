import pygame

NEIGHBOUR_OFFSETS = [(-1, 1), (0, 1), (1, 1),
                     (-1, 0), (0, 0), (1, 0),
                     (-1, -1), (0, -1), (1, -1)]

PHYSICS_TILES = {'grass',
                 'left_grass',
                 'right_grass',
                 'left_ground_wall',
                 'ground',
                 'right_ground_wall',
                 'left_bottom_ground',
                 'bottom_ground',
                 'right_bottom_ground',
                 'top_brick',
                 'top_left_brick',
                 'top_right_brick',
                 'left_brick',
                 'mid_brick',
                 'right_brick',
                 'bottom_brick',
                 'bottom_left_brick',
                 'bottom_right_brick',
                 'closed_door',
                 'closed_gray_door',
                 'glass',
                 'wood',
                 'gray_block'}

HIDING_TILES = {'bush',
                'big_wall'}


class Tilemap:
    def __init__(self, game, tile_size=(16, 16)):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.spawnpoint_positions = list()
        self.heal_positions = list()
        self.random_potion_positions = list()
        self.hiding_tiles_positions = list()
        self.door_positions = list()

    def find_spawnpoints(self):
        for tile in self.tilemap.values():
            if tile['type'] == 'spawnpoint':
                self.spawnpoint_positions.append(tile['pos'])

    def find_heal_positions(self):
        for tile in self.tilemap.values():
            if tile['type'] == 'heal':
                self.heal_positions.append(tile['pos'])

    def find_random_potion_positions(self):
        for tile in self.tilemap.values():
            if tile['type'] == 'random_potion':
                self.random_potion_positions.append(tile['pos'])

    def find_hiding_tiles_positions(self):
        for tile in self.tilemap.values():
            if 'hide' in tile:
                rect = pygame.Rect(tile['pos'][0] * self.tile_size[0],
                                   tile['pos'][1] * self.tile_size[1],
                                   tile['size'][0], tile['size'][1])
                self.hiding_tiles_positions.append(rect)

    def find_door_positions(self):
        for tile in self.tilemap.values():
            if tile['type'] == 'closed_door' or tile['type'] == 'closed_gray_door':
                self.door_positions.append(tile['pos'])

    def tiles_around(self, pos):
        """Возвращает tiles из tilemap вокруг pos"""
        tiles = list()
        tile_pos = (
        int(pos[0] // self.tile_size[0]), int(pos[1] // self.tile_size[1]))
        for offset in NEIGHBOUR_OFFSETS:
            check_pos = str(tile_pos[0] + offset[0]) + ';' + str(
                tile_pos[1] + offset[1])
            if check_pos in self.tilemap:
                tiles.append(self.tilemap[check_pos])
        return tiles

    def physics_rects_around(self, pos):
        """Возвращает Rects от физических tiles из tilemap вокруг pos"""
        tile_size = self.tile_size
        rects = list()
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                if tile['type'] == 'closed_door' or tile['type'] == 'closed_gray_door':
                    tile_size = (16, 32)
                rect = pygame.Rect(tile['pos'][0] * self.tile_size[0],
                                   tile['pos'][1] * self.tile_size[1],
                                   tile_size[0], tile_size[1])
                rects.append(rect)
        return rects

    def render(self, surface, is_editor=False, offset=(0, 0)):
        for tile in self.tilemap.values():
            if (self.game.assets[tile['type']] is None or
                    (tile['type'] in ("heal", "random_potion", "opened_door", "closed_door", "opened_gray_door", "closed_gray_door")
                     and not is_editor) or
                    'hide' in tile):
                continue
            tile_pos = (tile['pos'][0] * self.tile_size[0],
                        tile['pos'][1] * self.tile_size[1])
            surface.blit(self.game.assets[tile['type']],
                         (tile_pos[0] - offset[0], tile_pos[1] - offset[1]))

    def render_hiding_tile(self, surface, offset=(0, 0)):
        for tile in self.tilemap.values():
            if 'hide' in tile:
                tile_pos = (tile['pos'][0] * self.tile_size[0],
                            tile['pos'][1] * self.tile_size[1])
                surface.blit(self.game.assets[tile['type']],
                             (tile_pos[0] - offset[0], tile_pos[1] - offset[1]))

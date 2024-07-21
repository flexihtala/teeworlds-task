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
                 'right_bottom_ground'}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.spawnpoint_positions = list()

    def find_spawnpoints(self):
        for tile in self.tilemap.values():
            if tile['type'] == 'spawnpoint':
                self.spawnpoint_positions.append(tile['pos'])

    def tiles_around(self, pos):
        """Возвращает tiles из tilemap вокруг pos"""
        tiles = list()
        tile_pos = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOUR_OFFSETS:
            check_pos = str(tile_pos[0] + offset[0]) + ';' + str(
                tile_pos[1] + offset[1])
            if check_pos in self.tilemap:
                tiles.append(self.tilemap[check_pos])
        return tiles

    def physics_rects_around(self, pos):
        """Возвращает Rects от физических tiles из tilemap вокруг pos"""
        rects = list()
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rect = pygame.Rect(tile['pos'][0] * self.tile_size,
                                   tile['pos'][1] * self.tile_size,
                                   self.tile_size, self.tile_size)
                rects.append(rect)
        return rects

    def render(self, surface, offset=(0, 0)):
        for tile in self.tilemap.values():
            if self.game.assets[tile['type']] is None:
                continue
            tile_pos = (tile['pos'][0] * self.tile_size,
                        tile['pos'][1] * self.tile_size)
            surface.blit(self.game.assets[tile['type']], (tile_pos[0] - offset[0], tile_pos[1] - offset[1]))

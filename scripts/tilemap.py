import pygame

NEIGHBOUR_OFFSETS = [(-1, 1), (0, 1), (1, 1),
                     (-1, 0), (0, 0), (1, 0),
                     (-1, -1), (0, -1), (1, -1)]

PHYSICS_TILES = {'grass'}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass',
                                                'pos': (3 + i, 10)}
        for i in range(10):
            self.tilemap['10;' + str(3 + i)] = {'type': 'grass',
                                                'pos': (10, 3 + i)}

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

    def render(self, surface):
        for tile in self.tilemap.values():
            tile_pos = (tile['pos'][0] * self.tile_size,
                        tile['pos'][1] * self.tile_size)
            surface.blit(self.game.assets[tile['type']], tile_pos)

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass',
                                                'pos': (3 + i, 10)}

    def render(self, surface):
        for tile in self.tilemap.values():
            tile_pos = (tile['pos'][0] * self.tile_size,
                        tile['pos'][1] * self.tile_size)
            surface.blit(self.game.assets[tile['type']], tile_pos)

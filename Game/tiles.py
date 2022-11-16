import pygame, csv, os


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, type, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        # self.image = spritesheet.parse_sprite(image)
        self.image = pygame.transform.scale(
            pygame.image.load((os.path.join(os.path.dirname(__file__), 'assets/tiles', image))).convert_alpha(),
            (size, size))
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class TileMap():
    def __init__(self, filename, size):
        self.getTileList()
        self.tile_size = size
        self.start_x, self.start_y = 0, 0
        # self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def getTileList(self):
        # This may need to have the os.path.join(os.path.dirname(__file__), treatment
        with open(os.path.join(os.path.dirname(__file__), 'Assets/Tiles/tileID.csv'), mode='r',
                  encoding='utf-8-sig') as data:
            self.tileList = []
            reader = csv.reader(data)
            for row in reader:
                if row[0] != None:
                    self.tileList.append((row[0] + '.png', row[1]))

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                if tile == '0':
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '70':
                    image, type = self.tileList[int(tile) - 1]
                    self.exit = Tile(image, type, x * self.tile_size, y * self.tile_size, self.tile_size)
                    tiles.append(self.exit)
                elif tile == '71':
                    image, type = self.tileList[int(tile) - 1]
                    self.entrance = Tile(image, type, x * self.tile_size, y * self.tile_size, self.tile_size)
                    tiles.append(self.entrance)
                elif tile > '0':
                    image, type = self.tileList[int(tile) - 1]
                    tiles.append(Tile(image, type, x * self.tile_size, y * self.tile_size, self.tile_size))
                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

    def get_tiles(self):
        return self.tiles

    def getEntrance(self):
        return self.entrance

    def getExit(self):
        return self.exit

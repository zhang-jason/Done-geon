import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, type, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        #self.image = spritesheet.parse_sprite(image)
        self.image = pygame.transform.scale(pygame.image.load((os.path.join(os.path.dirname(__file__), 'assets/tiles', image))).convert_alpha(), (size, size))
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
        #self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def getTileList(self):
        with open('Assets/Tiles/tileID.csv', mode='r', encoding='utf-8-sig') as data:
            self.tileList = []
            reader = csv.reader(data)
            for row in reader:
                if row[0] != None:
                    self.tileList.append((row[0] + '.png', row[1]))

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map (self):
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
                elif tile > '0':
                    image, type = self.tileList[int(tile) - 1]
                    tiles.append(Tile(image, type, x * self.tile_size, y * self.tile_size, self.tile_size))
                    # print('Image:' + image + '\nType:' + type)
                    
                # elif tile == '258':
                #     tiles.append(Tile('wall_inner_corner_mid_left.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '36':
                #     tiles.append(Tile('wall_fountain_mid_red_anim_f0.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '33':
                #     tiles.append(Tile('wall_mid.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '34':
                #     tiles.append(Tile('wall_right.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '259':
                #     tiles.append(Tile('wall_inner_corner_mid_rigth.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '68':
                #     tiles.append(Tile('wall_fountain_basin_red_anim_f0.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '129':
                #     tiles.append(Tile('floor_1.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '323':
                #     tiles.append(Tile('wall_mid.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '5':
                #     tiles.append(Tile('wall_top_mid2.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '257':
                #     tiles.append(Tile('wall_side_mid_right.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '256':
                #     tiles.append(Tile('wall_side_mid_left.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '226':
                #     tiles.append(Tile('wall_top_mid.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '595':
                #     tiles.append(Tile('chest_full_open_anim_f0.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '294':
                #     tiles.append(Tile('hole.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '165':
                #     tiles.append(Tile('column_top.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '197':
                #     tiles.append(Tile('column_mid.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '229':
                #     tiles.append(Tile('coulmn_base.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '290':
                #     tiles.append(Tile('wall_inner_corner_l_top_left.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '291':
                #     tiles.append(Tile('wall_inner_corner_l_top_rigth.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                # elif tile == '195':
                #     tiles.append(Tile('floor_ladder.png', x * self.tile_size, y * self.tile_size, self.tile_size))
                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles

    def get_tiles(self):
        return self.tiles
import pygame
from os.path import join
from os.path import dirname
import pygame.locals as c


class Obj(pygame.sprite.Sprite):
    def __init__(self, origin, TILE_SIZE):
        super(Obj, self).__init__()
        # change this to generic nonmove obj later
        self.image = pygame.transform.scale(
            pygame.image.load(join(dirname(dirname(__file__)), 'assets', 'bushAsset1.png')).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'assets', 'bushAsset1.png'))
        trans_color = trans_image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        self.rect.top, self.rect.left = origin

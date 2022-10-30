import pygame
import math
from Entities.entity import Entity
from os.path import join
from os.path import dirname

class Powerup(Entity):
    # Team is whether Player or Enemy used projectile, Ability is type of projectile (e.g. fireball, arrow, etc.)
    def __init__(self, position, ability, TILE_SIZE):
        super(Powerup, self).__init__()

        self.position = position
        self.ability = ability
        #self.size = (TILE_SIZE*3//4, TILE_SIZE*3//4)

        # Image and Animations
        self.image = pygame.transform.scale(pygame.image.load(
                join(dirname(dirname(__file__)), f'assets/powerups', f'{ability}.png')), (TILE_SIZE*3//4, TILE_SIZE*3//4))
        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/powerups', f'{ability}.png'))
        trans_color = trans_image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        self.rect.center = position
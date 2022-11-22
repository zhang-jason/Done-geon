import pygame
from Entities.entity import Entity
from os.path import join, dirname
from random import choice, randint
from Entities.powerup import Powerup
from dirMods import getImages

class DestructableObj(Entity):
    def __init__(self, position, type, TILE_SIZE):
        super(DestructableObj, self).__init__()

        self.position = position
        self.hit = False
        reward = choice(['Speed', 'Heal', 'Shield', 'Bones'])
        if reward == 'Bones':
            self.reward = randint(2,8)
        else:
            self.reward = Powerup(position, reward, TILE_SIZE)

        # Image and Animations
        imageDir = join(dirname(dirname(__file__)), f'assets/Destructables/{type}')
        self.sprites = getImages(imageDir, (TILE_SIZE*2, TILE_SIZE*2))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = position

    def update(self):
        if self.hit:
            if int(self.current_sprite) < len(self.sprites):
                self.current_sprite += 0.25
                self.image = self.sprites[int(self.current_sprite)]
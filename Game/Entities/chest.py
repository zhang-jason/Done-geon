import pygame
from Entities.entity import Entity
from os.path import join, dirname
from dirMods import getImages

class Chest(Entity):
    def __init__(self, position, TILE_SIZE):
        super(Chest, self).__init__()

        self.position = position
        self.opened = False
        self.rewards = []

        # Image and Animations
        imageDir = join(dirname(dirname(__file__)), 'assets/Chest')
        self.sprites = getImages(imageDir, (TILE_SIZE, TILE_SIZE))

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update(self):
        if self.opened:
            if int(self.current_sprite) < len(self.sprites):
                self.current_sprite += 0.25
                self.image = self.sprites[int(self.current_sprite)]
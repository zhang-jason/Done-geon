import pygame
from Entities.entity import Entity
from os.path import join, dirname
from dirMods import getImages

class Door(Entity):
    def __init__(self, position, type, TILE_SIZE):
        super(Door, self).__init__()

        self.position = position
        self.type = type
        self.cooldown = 0

        imageDir = join(dirname(dirname(__file__)), f'assets/Doors/{type}')
        self.sprites = getImages(imageDir, (TILE_SIZE, TILE_SIZE))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update(self):
        if int(self.current_sprite) < len(self.sprites):
            self.current_sprite += 0.125
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
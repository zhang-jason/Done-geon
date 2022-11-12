import pygame
from pygame import mixer, Rect
from Entities.entity import Entity
from os import listdir
from os.path import join, dirname
from dirMods import getImages

class Trap(Entity):
    def __init__(self, position, type, TILE_SIZE):
        super(Trap, self).__init__()

        self.position = position
        self.type = type
        self.activate = False
        self.cooldown = 0
        #self.size = (TILE_SIZE*3//4, TILE_SIZE*3//4)

        # Image and Animations
        imageDir = join(dirname(dirname(__file__)), f'assets/Traps/{type}')
        match type:
            case 'Spike':
                scaling = (TILE_SIZE, TILE_SIZE)
            case 'Fire':
                scaling = (TILE_SIZE, TILE_SIZE * (41/32))
        self.sprites = getImages(imageDir, scaling)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.hitbox = Rect(position[0], position[1], TILE_SIZE, TILE_SIZE)

        match type:
            case 'Spike':
                self.rect.centery -= TILE_SIZE / 7
            case 'Fire':
                self.rect.centery -= TILE_SIZE / 2.25


    def update(self):
        if self.activate:
            if int(self.current_sprite) < len(self.sprites):
                self.current_sprite += 0.25
                if self.current_sprite >= len(self.sprites):
                    self.activate = False
                    self.current_sprite = 0

        # else:
        #     if self.current_sprite > 0:
        #         self.current_sprite -= 0.20
        #         if self.current_sprite <= 0:
        #             self.current_sprite = 0
        #         self.image = self.sprites[int(self.current_sprite)]

        if self.cooldown > 0:
            self.cooldown -= 0.05
        self.image = self.sprites[int(self.current_sprite)]
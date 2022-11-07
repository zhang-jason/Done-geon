import os
from os.path import join, dirname
from Entities.entity import Entity
from Entities.projectile import Projectile
from Entities.playerChar import Player
from math import sqrt
import pygame
import pygame.locals as c

class Reaper(Player):
    def __init__(self, startPosition, TILE_SIZE):

        size = (TILE_SIZE*5//6, TILE_SIZE*5//6)

        self.idleSprites = self.__getSprites__('Reaper', 'Idle', size)
        self.runSprites = self.__getSprites__('Reaper', 'Run', size)
        self.attackSprites = self.__getSprites__('Reaper', 'Attack', size)
        self.currentSprites = self.idleSprites

        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition

        super(Reaper, self).__init__(startPosition, TILE_SIZE)
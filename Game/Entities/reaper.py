from Entities.playerChar import Player
from math import sqrt
import pygame
import pygame.locals as c

class Reaper(Player):
    def __init__(self, startPosition, TILE_SIZE,player= None):
        size = (TILE_SIZE*5//6, TILE_SIZE*5//6)

        self.idleSprites = self.__getSprites__('Reaper', 'Idle', size)
        self.runSprites = self.__getSprites__('Reaper', 'Run', size)
        self.attackSprites = self.__getSprites__('Reaper', 'Attack', size)
        self.currentSprites = self.idleSprites

        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        if player is None:
            self.rect.left, self.rect.top = startPosition
        else:
            self.rect.left, self.rect.top = player.rect.left, player.rect.top

        self.canAttack = pygame.time.get_ticks() + 480
        super(Reaper, self).__init__(startPosition, TILE_SIZE,player)

    def update(self):
        if self.attacking:
            self.currentSprites = self.attackSprites
        else:
            if self.moving:
                self.currentSprites = self.runSprites
            else:
                self.currentSprites = self.idleSprites

        if self.attacking:
            self.current_sprite += 0.20  # Controls how fast the animations cycle
        else:
            self.current_sprite += 0.05

        super(Reaper, self).update()
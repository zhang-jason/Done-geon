from Entities.playerChar import Player
import pygame
import pygame.locals as c
from dirMods import __getSprites__

class Reaper(Player):
    def __init__(self, startPosition, TILE_SIZE,player= None):
        size = (TILE_SIZE*5//6, TILE_SIZE*5//6)

        self.idleSprites = __getSprites__('Reaper', 'Idle', size)
        self.runSprites = __getSprites__('Reaper', 'Run', size)
        self.attackSprites = __getSprites__('Reaper', 'Attack', size)
        self.currentSprites = self.idleSprites

        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        if player is None:
            self.rect.centerx, self.rect.centery = startPosition
        else:
            self.rect.centerx, self.rect.centery = player.rect.centerx, player.rect.centery

        self.canAttack = pygame.time.get_ticks() + 480
        self.damage = 4
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
import os
from os.path import join, dirname
from Entities.entity import Entity
from Entities.projectile import Projectile
from Entities.playerChar import Player
from math import sqrt
import pygame
import pygame.locals as c

class Necromancer(Player):
    def __init__(self, startPosition, TILE_SIZE,player= None):
        size = (TILE_SIZE*2//3, TILE_SIZE*5//6)

        self.idleSprites = self.__getSprites__('Necromancer', 'Idle', size)
        self.runSprites = self.__getSprites__('Necromancer', 'Run', size)
        self.attackSprites = self.__getSprites__('Necromancer', 'Attack', size)
        self.currentSprites = self.idleSprites

        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        if player is None:
            self.rect.left, self.rect.top = startPosition
        else:
            self.rect.left, self.rect.top = player.rect.left, player.rect.top
        print(self.rect)

        self.canAttack = pygame.time.get_ticks() + 480
        super(Necromancer, self).__init__(startPosition, TILE_SIZE,player)

    def attack(self, projectiles):
        if pygame.time.get_ticks() >= self.canAttack:
            player = self.rect.center
            cursor = pygame.mouse.get_pos()
            self.canAttack = pygame.time.get_ticks() + 480
            projectiles.add(Projectile(player, cursor, True, 'Magic Ball', self.TILE_SIZE))

    def update(self):
        if self.attacking:
            self.currentSprites = self.attackSprites
        else:
            if self.moving:
                self.currentSprites = self.runSprites
            else:
                self.currentSprites = self.idleSprites

        if self.attacking:
            self.current_sprite += 0.10  # Controls how fast the animations cycle
        else:
            self.current_sprite += 0.05

        super(Necromancer, self).update()
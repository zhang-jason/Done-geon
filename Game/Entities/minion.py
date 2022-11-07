import os
import random
from os.path import join, dirname
from random import randint

from Entities.entity import Entity
from Entities.projectile import Projectile
import pygame


class Minion(Entity):
    def __init__(self, startPosition, TILE_SIZE, player):
        super(Minion, self).__init__()
        self.iframes = 0
        self.player = player
        self.TILE_SIZE = TILE_SIZE
        # Sprite Animation
        self.sprites = player.runSprites
        # self.is_animating == False
        size = (TILE_SIZE*2//3, TILE_SIZE*5//6)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition

        # how often the character can move (every five ticks)
        self.canMove = pygame.time.get_ticks() + 5
        self.canAttack = pygame.time.get_ticks() + 240
        self.speed = 4  # how far it moves
        self.collidable = True
        self.current_health = 2
        self.max_health = 2
        self.alive = True

    def attack(self, projectiles, enemies):
        minion = self.rect.center
        if len(enemies):
            enemy = randint(0, len(enemies)-1)
            i = 0
            for e in enemies:
                if enemy == i:
                    eCoords = e.rect.center
                    projectiles.add(Projectile(minion, eCoords, True, 'Magic Ball', self.TILE_SIZE*2/3))
                    break
                i += 1

    def update(self, projectiles, enemies):
        super(Minion, self).update(projectiles)

        self.current_sprite += 0.05  # Controls how fast the animations cycle
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        
        if self.flippedImage:
            self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], True, False)
        else:
            self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], False, False)

        # Scuffed random attack pattern generator
        rand_attack = randint(1, 250)
        if rand_attack == 1:
            self.attack(projectiles, enemies)
        if self.iframes:
            self.iframes -= 1

    def get_hit(self, hitDmg):
        if not self.iframes:
            if (self.current_health - hitDmg) > 0:
                self.current_health -= hitDmg
                self.iframes = 60
            else:
                self.current_health = 0
                self.alive = False

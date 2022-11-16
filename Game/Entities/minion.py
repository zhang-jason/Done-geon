from os.path import join, dirname
from random import randint

from Entities.entity import Entity
from Entities.projectile import Projectile
from dirMods import getImages
import pygame


class Minion(Entity):
    def __init__(self, startPosition, TILE_SIZE, player, type):
        super(Minion, self).__init__()
        self.iframes = 0
        self.player = player
        self.TILE_SIZE = TILE_SIZE
        # Sprite Animation
        size = (TILE_SIZE*1//2, TILE_SIZE*1//2)
        self.sprites = getImages(join(dirname(dirname(__file__)), f'assets/minions/{type}'), size)
        self.type = type
        self.ranged = False
        if 'Ranged' in type:
            self.ranged = True

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition

        self.canMove = False
        self.canAttack = pygame.time.get_ticks() + 240
        self.speed = 4  # how far it moves
        self.collidable = True
        self.current_health = 2
        self.max_health = 2
        self.alive = True
        self.spawn_cooldown = 180

    def attack(self, projectiles, enemies):
        minion = self.rect.center
        if len(enemies):
            enemy = randint(0, len(enemies)-1)
            i = 0
            for e in enemies:
                if enemy == i:
                    eCoords = e.rect.center
                    if 'Archer' in self.type:
                        projectiles.add(Projectile(minion, eCoords, True, 'Arrow', (self.TILE_SIZE*1//2, self.TILE_SIZE*1//4)))
                    else:
                        projectiles.add(Projectile(minion, eCoords, True, 'Magic Ball', (self.TILE_SIZE*1//2, self.TILE_SIZE*1//2)))
                    break
                i += 1

    def update(self, projectiles, enemies):
        super(Minion, self).update(projectiles)
        if self.spawn_cooldown >= 0:
            self.spawn_cooldown -= 1
        else:
            self.canMove = True
        self.current_sprite += 0.05  # Controls how fast the animations cycle
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        
        if self.flippedImage:
            self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], True, False)
        else:
            self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], False, False)

        # Scuffed random attack pattern generator
        if self.ranged:
            rand_attack = randint(1, 125)
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

from os.path import join, dirname
from Entities.enemy import Entity
from Entities.projectile import Projectile
import pygame
import pygame.locals as c
from pygame import mixer
from dirMods import getImages

class Priestess(Entity):
    def __init__(self, startPosition, player, TILE_SIZE):
        super(Priestess, self).__init__()
        size = (TILE_SIZE*8,TILE_SIZE*8//2.25)
        
        self.idleSprites = getImages((join(dirname(dirname(__file__)), 'assets/Priestess/Idle')), size)
        self.runSprites = getImages((join(dirname(dirname(__file__)), 'assets/Priestess/Run')), size)
        self.meleeSprites = getImages((join(dirname(dirname(__file__)), 'assets/Priestess/Melee')), size)
        self.rangedSprites = getImages((join(dirname(dirname(__file__)), 'assets/Priestess/Ranged')), size)
        self.immuneSprites = getImages((join(dirname(dirname(__file__)), 'assets/Priestess/Immune')), size)
        self.deathSprites = getImages((join(dirname(dirname(__file__)), 'assets/Priestess/Death')), size)
        self.projectileSprites = getImages((join(dirname(dirname(__file__)), 'assets/Projectiles/Magic_Ball')), (TILE_SIZE, TILE_SIZE))
        self.currentSprites = self.idleSprites
        
        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = startPosition

        self.canMove = False
        self.spawn_cooldown = 180
        self.speed = 2
        self.health = 50
        self.player = player
        self.collidable = 1
        self.damage = 2

    def update(self, projectiles):
        if self.spawn_cooldown >= 0:
            self.spawn_cooldown -= 1
        else:
            self.canMove = True
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.currentSprites):
            self.current_sprite = 0
        self.image = self.currentSprites[int(self.current_sprite)]

        if self.flippedImage:
            self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
        else:
            self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)
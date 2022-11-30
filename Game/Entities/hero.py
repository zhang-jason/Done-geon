from os.path import join, dirname
from math import hypot
from random import choices
from Entities.enemy import Entity
from Entities.projectile import Projectile
import pygame
import pygame.locals as c
from pygame import mixer
from dirMods import getImages, __getSprites__

class Hero(Entity):
    def __init__(self, startPosition, player, TILE_SIZE):
        super(Hero, self).__init__()
        size = (TILE_SIZE*8,TILE_SIZE*8//2.25)
        self.TILE_SIZE = TILE_SIZE
        
        self.idleSprites = __getSprites__('Hero', 'Idle', size)
        self.runSprites = __getSprites__('Hero', 'Run', size)
        self.meleeSprites = __getSprites__('Hero', 'Melee', size)
        self.rangedSprites = __getSprites__('Hero', 'Ranged', size)
        self.immuneSprites = __getSprites__('Hero', 'Immune', size)
        self.deathSprites = __getSprites__('Hero', 'Death', size)
        self.projectileSprites = getImages((join(dirname(dirname(__file__)), 'assets/Projectiles/Phoenix')), (TILE_SIZE*3, TILE_SIZE*3))
        self.currentSprites = self.idleSprites
        
        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]

        # Hitbox Rect
        self.rect = pygame.rect.Rect(0, 0, TILE_SIZE//1.5, TILE_SIZE)
        self.rect.centerx, self.rect.centery = startPosition

        # Image Display Rect
        self.image_rect = self.image.get_rect()
        self.image_rect.midbottom = self.rect.midbottom

        self.canMove = False
        self.immune = True
        self.spawn_cooldown = 180
        self.speed = 2
        self.health = 50
        self.player = player
        self.collidable = 1
        self.damage = 2

        self.action = 'Idle'
        self.action_cooldown = pygame.time.get_ticks() + 1080
        self.action_finished = False
        self.animation_speed = 0.05
        self.immune_period = 0
        self.projectile_fired = True
        self.attackPosition = (0,0)
        self.attackRadius = 1
        self.MELEE_START = 10

        self.start = True

    def update(self, projectiles):
        if self.start:
            if self.spawn_cooldown >= 0:
                self.spawn_cooldown -= 1
            else:
                self.canMove = True
                self.immune = False
                self.action_finished = True
                self.start = False

        if self.health <= 0 and self.action not in ('Death', 'Done'):
            self.action = 'Death'
            self.action_finished = False
            self.canMove = False
            if self.currentSprites is not self.deathSprites:
                self.currentSprites = self.deathSprites
            return

        elif self.currentSprites is self.deathSprites and self.action_finished:
            return

        else:
            if self.currentSprites is not self.runSprites and self.action_finished:
                self.currentSprites = self.runSprites
                self.action = 'Run'

            if pygame.time.get_ticks() >= self.action_cooldown and self.action_finished:
                self.chooseState(self.__inRange__(self.player))
                self.action_cooldown = pygame.time.get_ticks() + 5000

            if self.immune_period >= 0:
                self.immune_period -= 1
            elif self.currentSprites is self.immuneSprites and self.immune_period <= 0:
                self.canMove = True
                self.action_finished = True
                self.immune = False

            if self.currentSprites is self.idleSprites and self.dx == 0 and self.dy == 0:
                self.currentSprites = self.idleSprites
            if self.currentSprites in (self.meleeSprites, self.rangedSprites, self.deathSprites):
                self.current_sprite += 0.15
                if self.current_sprite >= len(self.currentSprites):
                    self.action_finished = True
                    self.current_sprite = len(self.currentSprites) - 1
                    if self.currentSprites is not self.deathSprites:
                        self.canMove = True
            elif self.currentSprites in (self.idleSprites, self.runSprites):
                self.current_sprite += 0.15
                if self.current_sprite >= len(self.currentSprites):
                    self.current_sprite = 0
            elif self.currentSprites is self.immuneSprites:
                self.current_sprite += 0.15
                if self.current_sprite >= len(self.currentSprites) - 2 and self.immune:
                    self.current_sprite = len(self.currentSprites) - 3
                elif self.current_sprite >= len(self.currentSprites) and not self.immune:
                    self.action_finished = True
                    self.current_sprite = len(self.currentSprites) - 1

            if self.flippedImage:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
            else:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)

            if self.currentSprites is self.rangedSprites and int(self.current_sprite) == 8 and not self.projectile_fired:
                if self.flippedImage:
                    bossPos = self.rect.topleft
                else:
                    bossPos = self.rect.topright
                projectiles.add(Projectile(bossPos, self.player.rect.center, False, 'Phoenix', (self.TILE_SIZE, self.TILE_SIZE), self.projectileSprites, 8))
                self.projectile_fired = True

    def chooseState(self, inRange):
        if self.action_finished:
            if inRange:
                action_list = ['Melee','Immune']
                weights = (75, 25)
            else:
                action_list = ['Run', 'Ranged', 'Immune']
                weights = (30, 50, 20)

            self.action = choices(action_list, weights)[0]

            match self.action:
                case 'Run':
                    if self.currentSprites is not self.runSprites:
                        self.currentSprites = self.runSprites
                        self.current_sprite = 0
                    return
                case 'Melee':
                    self.action_finished = False
                    self.currentSprites = self.meleeSprites
                    self.current_sprite = 0
                case 'Ranged':
                    self.action_finished = False
                    self.canMove = False
                    self.projectile_fired = False
                    self.currentSprites = self.rangedSprites
                    self.current_sprite = 0
                case 'Immune':
                    self.action_finished = False
                    self.canMove = False
                    self.immune_period = 480
                    self.immune = True
                    self.currentSprites = self.immuneSprites
                    self.current_sprite = 0

        print(self.action)

    def __inRange__(self, ent):
        attackPosition = self.rect.center
        attackRadius = 2 * hypot(attackPosition[0] - self.rect.bottomright[0], attackPosition[1] - self.rect.bottomright[1])
        distance = hypot(attackPosition[0] - ent.rect.centerx, attackPosition[1] - ent.rect.centery)
        #self.canAttack = pygame.time.get_ticks() + 480
        
        if distance <= attackRadius:
            #self.player.get_hit(self.damage)
            return True
        else:
            return False
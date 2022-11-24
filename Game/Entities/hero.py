from os.path import join, dirname
from math import hypot
from random import choice
from Entities.enemy import Entity
from Entities.projectile import Projectile
import pygame
import pygame.locals as c
from pygame import mixer
from dirMods import getImages

class Hero(Entity):
    def __init__(self, startPosition, player, TILE_SIZE):
        super(Hero, self).__init__()
        size = (TILE_SIZE*8,TILE_SIZE*8//2.25)
        
        self.idleSprites = getImages((join(dirname(dirname(__file__)), 'assets/Hero/Idle')), size)
        self.runSprites = getImages((join(dirname(dirname(__file__)), 'assets/Hero/Run')), size)
        self.meleeSprites = getImages((join(dirname(dirname(__file__)), 'assets/Hero/Melee')), size)
        self.rangedSprites = getImages((join(dirname(dirname(__file__)), 'assets/Hero/Ranged')), size)
        self.immuneSprites = getImages((join(dirname(dirname(__file__)), 'assets/Hero/Immune')), size)
        self.deathSprites = getImages((join(dirname(dirname(__file__)), 'assets/Hero/Death')), size)
        self.projectileSprites = getImages((join(dirname(dirname(__file__)), 'assets/Projectiles/Magic_Ball')), (TILE_SIZE, TILE_SIZE))
        self.currentSprites = self.idleSprites
        
        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]

        # Image Display Rect
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx, self.image_rect.centery = startPosition

        # Hitbox Rect
        self.rect = pygame.rect.Rect(0, 0, TILE_SIZE, TILE_SIZE*1.3)
        self.rect.midbottom = self.image_rect.midbottom

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
        self.attackPosition = (0,0)
        self.attackRadius = 1

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

        else:
            if self.currentSprites is not self.runSprites and self.action_finished:
                self.currentSprites = self.runSprites
                self.action = 'Run'

            if pygame.time.get_ticks() >= self.action_cooldown and self.action_finished:
                # print(f'Curr Time: {pygame.time.get_ticks()}')
                # print(f'CD Time: {self.action_cooldown}')
                self.chooseState(self.__inRange__(self.player))
                self.action_cooldown = pygame.time.get_ticks() + 5000

            if self.immune_period >= 0:
                self.immune_period -= 1
            elif self.currentSprites is self.immuneSprites and self.immune_period <= 0:
                self.canMove = True
                self.action_finished = True

            if self.currentSprites is self.idleSprites and self.dx == 0 and self.dy == 0:
                self.currentSprites = self.idleSprites
            if self.currentSprites not in (self.idleSprites, self.runSprites, self.immuneSprites):
                self.current_sprite += 0.20
                if self.current_sprite >= len(self.currentSprites):
                    self.action_finished = True
                    self.canMove = True
                    self.current_sprite = len(self.currentSprites) - 1
            elif self.currentSprites in (self.idleSprites, self.runSprites):
                self.current_sprite += 0.05
                if self.current_sprite >= len(self.currentSprites):
                    self.current_sprite = 0
            elif self.currentSprites is self.immuneSprites:
                self.current_sprite += 0.20
                if self.current_sprite >= len(self.currentSprites) - 2 and self.immune:
                    self.current_sprite = len(self.currentSprites) - 3
                elif self.current_sprite >= len(self.currentSprites) and not self.immune:
                    self.action_finished = True
                    self.current_sprite = len(self.currentSprites) - 1

            if self.flippedImage:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
            else:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)

    def chooseState(self, inRange):
        if self.health <= 0:
            self.action = 'Death'
            self.currentSprites = self.deathSprites
            return

        if self.action_finished:
            if inRange:
                action_list = ['Melee','Immune']
            else:
                action_list = ['Run', 'Ranged', 'Immune']

            self.action = choice(action_list)

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
        self.attackPosition = self.rect.center
        self.attackRadius = 2 * hypot(self.attackPosition[0] - self.rect.bottomright[0], self.attackPosition[1] - self.rect.bottomright[1])
        distance = hypot(self.attackPosition[0] - ent.rect.centerx, self.attackPosition[1] - ent.rect.centery)
        #self.canAttack = pygame.time.get_ticks() + 480
        
        if distance <= self.attackRadius:
            #self.player.get_hit(self.damage)
            return True
        else:
            return False
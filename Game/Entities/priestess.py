from os.path import join, dirname
from math import sin, cos, radians
from random import choices
from Entities.enemy import Entity
from Entities.projectile import Projectile
import pygame
import pygame.locals as c
from pygame import mixer
from dirMods import getImages, __getSprites__

class Priestess(Entity):
    def __init__(self, startPosition, player, TILE_SIZE):
        super(Priestess, self).__init__()
        size = (TILE_SIZE*8,TILE_SIZE*8//2.25)
        self.TILE_SIZE = TILE_SIZE
        
        self.idleSprites = __getSprites__('Priestess', 'Idle', size)
        self.runSprites = __getSprites__('Priestess', 'Run', size)
        self.meleeSprites = __getSprites__('Priestess', 'Melee', size)
        self.rangedSprites = __getSprites__('Priestess', 'Ranged', size)
        self.immuneSprites = __getSprites__('Priestess', 'Immune', size)
        self.healSprites = __getSprites__('Priestess', 'Heal', size)
        self.deathSprites = __getSprites__('Priestess', 'Death', size)
        self.projectileSprites = getImages((join(dirname(dirname(__file__)), 'assets/Projectiles/Water_Ball')), (TILE_SIZE, TILE_SIZE))
        self.currentSprites = self.idleSprites
        
        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]

        # Image Display Rect
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx, self.image_rect.centery = startPosition

        # Hitbox Rect
        self.rect = pygame.rect.Rect(0, 0, TILE_SIZE//2, TILE_SIZE)
        self.rect.midbottom = self.image_rect.midbottom

        self.canMove = False
        self.immune = True
        self.spawn_cooldown = 180
        self.speed = 2
        self.MAX_HEALTH = 20
        self.health = self.MAX_HEALTH
        self.player = player
        self.collidable = 1
        self.damage = 1

        self.action = 'Idle'
        self.action_cooldown = pygame.time.get_ticks() + 1080
        self.action_finished = False
        self.animation_speed = 0.05
        self.immune_period = 0
        self.projectile_fired = True
        self.attackZone = pygame.rect.Rect(0,0,TILE_SIZE*2.25,TILE_SIZE)
        x, y = self.image_rect.center
        y += self.TILE_SIZE
        self.attackZone.midleft = (x, y)
        self.MELEE_START = 4

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
            if self.currentSprites in (self.meleeSprites, self.rangedSprites, self.deathSprites, self.healSprites):
                self.current_sprite += 0.15
                if self.current_sprite >= len(self.currentSprites):
                    self.action_finished = True
                    self.current_sprite = len(self.currentSprites) - 1
                    if self.currentSprites is self.healSprites:
                        self.health += 10
                        if self.health > self.MAX_HEALTH:
                            self.health = self.MAX_HEALTH
                    if self.currentSprites is not self.deathSprites:
                        self.canMove = True
            elif self.currentSprites in (self.idleSprites, self.runSprites):
                self.current_sprite += 0.15
                if self.current_sprite >= len(self.currentSprites):
                    self.current_sprite = 0
            elif self.currentSprites is self.immuneSprites:
                self.current_sprite += 0.15
                if self.current_sprite >= len(self.currentSprites) - 3 and self.immune:
                    self.current_sprite = len(self.currentSprites) - 4
                elif self.current_sprite >= len(self.currentSprites) and not self.immune:
                    self.action_finished = True
                    self.current_sprite = len(self.currentSprites) - 1

            x, y = self.image_rect.center
            y += self.TILE_SIZE

            if self.flippedImage:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
                self.attackZone.midright = (x, y)
            else:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)
                self.attackZone.midleft = (x, y)

            if self.currentSprites is self.rangedSprites and int(self.current_sprite) == 13 and not self.projectile_fired:
                size = (self.TILE_SIZE, self.TILE_SIZE)
                if self.flippedImage:
                    x, y = self.rect.bottomleft
                    origin = (x - self.TILE_SIZE, y)
                    target = (x - self.TILE_SIZE, y - self.TILE_SIZE)
                    angle = 0
                    for x in range(7):
                        output = self.__rotate__(origin, target, radians(angle))
                        projectiles.add(Projectile(origin, output, False, 'Water_Ball', size, self.projectileSprites, 4))
                        angle -= 30

                else:
                    x, y = self.rect.bottomright
                    origin = (x + self.TILE_SIZE, y)
                    target = (x + self.TILE_SIZE, y - self.TILE_SIZE)
                    angle = 0
                    for x in range(7):
                        output = self.__rotate__(origin, target, radians(angle))
                        projectiles.add(Projectile(origin, output, False, 'Water_Ball', size, self.projectileSprites, 4))
                        angle += 30
                
                self.projectile_fired = True

    def chooseState(self, inRange):
        if self.action_finished:
            if inRange:
                action_list = ['Melee','Immune']
                weights = (75, 25)
            else:
                action_list = ['Run', 'Ranged', 'Immune', 'Heal']
                weights = (30, 40, 10, 20)

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
                case 'Heal':
                    self.action_finished = False
                    self.canMove = False
                    self.currentSprites = self.healSprites
                    self.current_sprite = 0

        print(self.action)

    def __inRange__(self, ent):
        if self.attackZone.colliderect(ent.rect):
            return True
        return False

    # Use to perform projectile attacks in a semicircle
    def __rotate__(self, origin, target, angle):
        ox, oy = origin
        tx, ty = target

        qx = ox + cos(angle) * (tx - ox) - sin(angle) * (ty - oy)
        qy = oy + sin(angle) * (tx - ox) - cos(angle) * (ty - oy)
        return qx, qy
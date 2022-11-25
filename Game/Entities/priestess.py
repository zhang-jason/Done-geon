from os.path import join, dirname
from math import sin, cos, radians
from random import choices
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
        self.TILE_SIZE = TILE_SIZE
        
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

        # Image Display Rect
        self.image_rect = self.image.get_rect()
        self.image_rect.centerx, self.image_rect.centery = startPosition

        # Hitbox Rect
        self.rect = pygame.rect.Rect(0, 0, TILE_SIZE*0.8, TILE_SIZE*1.2)
        self.rect.midbottom = self.image_rect.midbottom

        self.canMove = False
        self.immune = True
        self.spawn_cooldown = 180
        self.speed = 2
        self.health = 50
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
            if self.currentSprites in (self.meleeSprites, self.rangedSprites):
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

            x, y = self.image_rect.center
            y += self.TILE_SIZE

            if self.flippedImage:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
                self.attackZone.midright = (x, y)
            else:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)
                self.attackZone.midleft = (x, y)

            if self.flippedImage:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
            else:
                self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)

            if self.currentSprites is self.rangedSprites and int(self.current_sprite) == 13 and not self.projectile_fired:
                size = (self.TILE_SIZE, self.TILE_SIZE)
                if self.flippedImage:
                    x, y = self.rect.bottomleft
                    origin = (x - self.TILE_SIZE, y)
                    target = (x - self.TILE_SIZE, y - self.TILE_SIZE)
                    angle = 0
                    for x in range(7):
                        output = self.__rotate__(origin, target, radians(angle))
                        projectiles.add(Projectile(origin, output, False, 'Water_Arrow', size, self.projectileSprites))
                        angle -= 30

                else:
                    x, y = self.rect.bottomright
                    origin = (x + self.TILE_SIZE, y)
                    target = (x + self.TILE_SIZE, y - self.TILE_SIZE)
                    angle = 0
                    for x in range(7):
                        output = self.__rotate__(origin, target, radians(angle))
                        projectiles.add(Projectile(origin, output, False, 'Water_Arrow', size, self.projectileSprites))
                        angle += 30
                
                self.projectile_fired = True

    def chooseState(self, inRange):
        if self.health <= 0:
            self.action = 'Death'
            self.currentSprites = self.deathSprites
            return

        if self.action_finished:
            if inRange:
                action_list = ['Melee','Immune']
                weights = (75, 25)
            else:
                action_list = ['Run', 'Ranged', 'Immune']
                weights = (40, 40, 20)

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
from os import listdir
from os.path import join, dirname, isfile
from Entities.entity import Entity
from Entities.projectile import Projectile
from math import sqrt
import pygame
import pygame.locals as c

class Player(Entity):
    def __init__(self, startPosition, TILE_SIZE, player= None):
        super(Player, self).__init__()
        if(player is None):
            self.bones = 3
            self.powerup = 'empty'
            self.powerupTimer = 0
            self.immune = False
            self.tile_x = 0
            self.tile_y = 0
            self.tile = "-1"
            self.fall = 0
            self.current_health = 4
        else:
            self.bones = player.bones
            self.powerup = player.powerup
            self.powerupTimer = player.powerupTimer
            self.immune = player.immune
            self.tile_x = player.tile_x
            self.tile_y = player.tile_y
            self.tile = player.tile
            self.fall = player.fall
            self.current_health = player.current_health
            
        self.sprint_cooldown = 0
        self.TILE_SIZE = TILE_SIZE

        # self.idleSprites.append(pygame.transform.scale(pygame.image.load(
        #     join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f0.png')), size))
        # self.idleSprites.append(pygame.transform.scale(pygame.image.load(
        #     join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f1.png')), size))
        # self.idleSprites.append(pygame.transform.scale(pygame.image.load(
        #     join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f2.png')), size))
        # self.idleSprites.append(pygame.transform.scale(pygame.image.load(
        #     join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f3.png')), size))

        # trans_image = pygame.image.load(
        #     join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f0.png'))
        # trans_color = trans_image.get_at((0, 0))
        # for x in self.idleSprites:
        #     x.set_colorkey(trans_color)

        # self.current_sprite = 0
        # self.image = self.currentSprites[self.current_sprite]
        # self.rect = self.image.get_rect()
        # self.rect.left, self.rect.top = startPosition
        # self.flippedImage = False

        # how often the character can move (every five ticks)
        self.canMove = pygame.time.get_ticks() + 5
        self.attacking = False
        self.moving = False
        self.speed = 5  # how far it moves
        self.set_speed(self.speed)  # is this necessary? should test later... prior to sprint mechanics
        self.collidable = True
        self.max_health = 4
        self.iframes = 0
        self.alive = True

        # self.velocity = pygame.math.Vector2()

    # def move(self, keys):
    #     # move = pygame.math.Vector2()
    #     self.velocity = pygame.math.Vector2()
    #     if pygame.time.get_ticks() >= self.canMove:
    #         if keys[c.K_w] and self.collideDir != 2:
    #             # move.y -= self.speed
    #             self.velocity.y -= self.speed
    #         if keys[c.K_s] and self.collideDir != 1:
    #             # move.y += self.speed
    #             self.velocity.y += self.speed
    #         if keys[c.K_a] and self.collideDir != 3:
    #             self.flippedImage = True
    #             # move.x -= self.speed
    #             self.velocity.x -= self.speed
    #         if keys[c.K_d] and self.collideDir != 4:
    #             self.flippedImage = False
    #             # move.x += self.speed
    #             self.velocity.x += self.speed
    #         # if move.x != 0 or move.y != 0:
    #         # move.scale_to_length(self.speed)
    #         if self.velocity.x != 0 or self.velocity.y != 0:
    #             self.velocity.scale_to_length(self.speed)
    #         if self.flippedImage == True:
    #             self.image = pygame.transform.flip(self.idleSprites[int(self.current_sprite)], True, False)
    #         else:
    #             self.image = pygame.transform.flip(self.idleSprites[int(self.current_sprite)], False, False)
    #
    #         self.canMove = pygame.time.get_ticks() + 5
    #         self.collideDir = 0
    #     self.rect.move_ip(self.velocity)

    def sprint(self):
        if self.sprint_cooldown <= 0:
            self.speed = 20
            self.sprint_cooldown = 90
            self.iframes = 15

    # def checkCollide(self, group):
    #     health = self.current_health
    #     if pygame.time.get_ticks() >= self.iframes:
    #         for e in group:
    #             if self.rect.colliderect(e.rect):
    #                 self.iframes = pygame.time.get_ticks() + 1000
    #                 self.get_hit(1)
    #                 break
    #     if self.current_health != health:
    #         print(self.current_health)

    def get_health(self):
        return self.current_health

    def get_hit(self, hitDmg):
        if not self.iframes:
            if (self.current_health - hitDmg) > 0:
                self.current_health -= hitDmg
                self.iframes = 60
            else:
                self.current_health = 0
                self.alive = False

    def get_regen(self, regenAmt):
        if (regenAmt + self.current_health) < self.max_health:
            self.current_health += regenAmt
        else:
            self.current_health = self.max_health

    def get_powerup(self, powerup):
        self.powerup = powerup

    def use_powerup(self,powerup= None):
        if powerup is None:
            powerup = self.powerup
        match powerup:
            case 'Speed':
                self.speed += 2
                self.powerupTimer = 1000
            case 'Heal':
                self.get_regen(1)
            case 'Shield':
                self.powerupTimer = 1000
                self.immune = True

        print(f'used {powerup}')
        self.powerup = 'empty'
    # def get_collisions(self, tiles):
    #     collisions = []
    #     for t in tiles:
    #         if self.rect.colliderect(t):
    #             collisions.append(t)
    #     return collisions
    #
    # def check_wall_collisions(self, tiles):
    #     collisions = self.get_collisions(tiles)
    #     # self.rect.bottom += 1
    #     for t in collisions:
    #         verticalMove = False
    #         if self.velocity.y != 0:
    #             verticalMove = True
    #         if self.velocity.x > 0:
    #             if verticalMove == False:
    #                 self.rect.x = t.rect.left - self.rect.w
    #                 self.collideDir = 4
    #                 self.velocity.x = 0
    #             else:
    #                 left = sqrt(pow(t.rect.left - self.rect.centerx, 2) + pow(t.rect.centery - self.rect.centery, 2))
    #                 up = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.top - self.rect.centery, 2))
    #                 down = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.bottom - self.rect.centery, 2))
    #                 min1 = min(left, up, down)
    #                 if min1 == left:
    #                     self.rect.x = t.rect.left - self.rect.w
    #                     self.collideDir = 4
    #                     self.velocity.x = 0
    #                     self.velocity.y = 0
    #                 elif min1 == up:
    #                     self.velocity.y = 0
    #                     self.velocity.x = 0
    #                     self.rect.bottom = t.rect.top
    #                     self.collideDir = 1
    #                 elif min1 == down:
    #                     self.velocity.y = 0
    #                     self.velocity.x = 0
    #                     self.rect.bottom = t.rect.bottom + self.rect.h
    #                     self.collideDir = 2
    #         if self.velocity.x < 0:
    #             if verticalMove == False:
    #                 self.rect.x = t.rect.right
    #                 self.collideDir = 3
    #                 self.velocity.x = 0
    #             else:
    #                 right = sqrt(pow(t.rect.right - self.rect.centerx, 2) + pow(t.rect.centery - self.rect.centery, 2))
    #                 up = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.top - self.rect.centery, 2))
    #                 down = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.bottom - self.rect.centery, 2))
    #                 min1 = min(right, up, down)
    #                 if min1 == right:
    #                     self.rect.x = t.rect.right
    #                     self.collideDir = 3
    #                     self.velocity.y = 0
    #                     self.velocity.x = 0
    #                 elif min1 == up:
    #                     self.velocity.y = 0
    #                     self.velocity.x = 0
    #                     self.rect.bottom = t.rect.top
    #                     self.collideDir = 1
    #                 elif min1 == down:
    #                     self.velocity.y = 0
    #                     self.velocity.x = 0
    #                     self.rect.bottom = t.rect.bottom + self.rect.h
    #                     self.collideDir = 2
    #         elif self.velocity.y > 0:
    #             self.velocity.y = 0
    #             self.rect.bottom = t.rect.top
    #             self.collideDir = 1
    #         elif self.velocity.y < 0:
    #             self.velocity.y = 0
    #             self.rect.bottom = t.rect.bottom + self.rect.h
    #             self.collideDir = 2

    # def update(self, keys, group, tiles):
    def update(self):
        # Update Sprite Animation
        if self.current_sprite >= len(self.currentSprites):
            self.current_sprite = 0
            if self.attacking:
                self.attacking = False
        self.image = self.currentSprites[int(self.current_sprite)]

        if self.flippedImage:
            self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
        else:
            self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)
        if self.iframes:
            self.iframes -= 1
        if self.sprint_cooldown:
            self.sprint_cooldown -= 1
            if self.speed > 5:
                self.speed -= 1

        if self.powerupTimer > 0:
            self.powerupTimer -= 1
            if self.powerupTimer == 0:
                self.speed = 5
                self.immune = False

        # self.move(keys)
        # self.checkCollide(group)
        # self.check_wall_collisions(tiles)

    # Reset char after dying; doesn't work quite yet
    def reset(self):
        self.current_health = 4
        self.alive = True

    def __getSprites__(self, type, status, size):
        spriteList = []

        dirPath = join(dirname(dirname(__file__)), f'assets/{type}/{status}')
        for i, file in enumerate(listdir(dirPath)):
            f = join(dirPath, f'{i}.png')
            if isfile(f):
                spriteList.append(pygame.transform.scale(pygame.image.load(f), size))

        trans_image = pygame.image.load(join(dirPath, '0.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in spriteList:
            x.set_colorkey(trans_color)

        return spriteList

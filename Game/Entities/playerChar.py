import os
from os.path import join, dirname
from Entities.entity import Entity
from Entities.projectile import Projectile
from math import sqrt
import pygame
import pygame.locals as c


class Player(Entity):
    def __init__(self, startPosition, TILE_SIZE):
        super(Player, self).__init__()
        self.TILE_SIZE = TILE_SIZE
        # Sprite Animation
        self.idleSprites = []
        # self.is_animating == False
        size = (TILE_SIZE*2//3, TILE_SIZE*5//6)
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f0.png')), size))
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f1.png')), size))
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f2.png')), size))
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f3.png')), size))

        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f0.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in self.idleSprites:
            x.set_colorkey(trans_color)

        self.current_sprite = 0
        self.image = self.idleSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition
        self.flippedImage = False

        # how often the character can move (every five ticks)
        self.canMove = pygame.time.get_ticks() + 5
        self.canAttack = pygame.time.get_ticks() + 240
        self.speed = 5  # how far it moves
        self.set_speed(self.speed)  # is this necessary? should test later... prior to sprint mechanics
        self.collidable = True
        self.current_health = 4
        self.max_health = 4
        self.iframes = 0
        self.alive = True

        self.bones = 0
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

    def attack(self, projectiles):
        if pygame.time.get_ticks() >= self.canAttack:
            player = self.rect.center
            cursor = pygame.mouse.get_pos()
            self.canAttack = pygame.time.get_ticks() + 240
            projectiles.add(Projectile(player, cursor, True, 'Magic Ball', self.TILE_SIZE))

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
        self.current_sprite += 0.05  # Controls how fast the animations cycle
        if self.current_sprite >= len(self.idleSprites):
            self.current_sprite = 0
        self.image = self.idleSprites[int(self.current_sprite)]
        if self.flippedImage:
            self.image = pygame.transform.flip(self.idleSprites[int(self.current_sprite)], True, False)
        else:
            self.image = pygame.transform.flip(self.idleSprites[int(self.current_sprite)], False, False)
        if self.iframes:
            self.iframes -= 1

        # self.move(keys)
        # self.checkCollide(group)
        # self.check_wall_collisions(tiles)

    # Reset char after dying; doesn't work quite yet
    def reset(self):
        self.current_health = 4
        self.alive = True

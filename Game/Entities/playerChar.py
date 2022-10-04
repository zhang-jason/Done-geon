from math import sqrt
from os.path import join
from os.path import dirname
from Entities.entity import Entity
from Entities.projectile import Projectile
import pygame
import pygame.locals as c


class Player(Entity):
    def __init__(self, startPosition):
        super(Player, self).__init__()
        
        # Sprite Animation
        self.idleSprites = []
        # self.is_animating == False
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f0.png')), (80, 100)))
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f1.png')), (80, 100)))
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f2.png')), (80, 100)))
        self.idleSprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Necromancer/Idle', 'necromancer_idle_anim_f3.png')), (80, 100)))
        self.current_sprite = 0
        self.image = self.idleSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition
        self.flippedImage = False
        
        # how often the character can move (every five ticks)
        self.canMove = pygame.time.get_ticks() + 5
        self.speed = 5  # how far it moves
        self.current_health = 4
        self.max_health = 4
        self.iframes = 0
        self.alive = True
        self.velocity = pygame.math.Vector2()
        self.collideDir = 0

    def move(self, keys):
        self.velocity = pygame.math.Vector2()
        if pygame.time.get_ticks() >= self.canMove:
            if keys[c.K_w] and self.collideDir != 2:
                #move.y -= self.speed
                self.velocity.y -= self.speed
            if keys[c.K_s] and self.collideDir != 1 and self.collideDir != 5:
                #move.y += self.speed
                self.velocity.y += self.speed
            if keys[c.K_a] and self.collideDir != 3 and self.collideDir != 5:
                self.flippedImage = True
                #move.x -= self.speed
                self.velocity.x -= self.speed
            if keys[c.K_d] and self.collideDir != 4:
                self.flippedImage = False
                #move.x += self.speed
                self.velocity.x += self.speed
            #if (move.x != 0 or move.y != 0):
                #move.scale_to_length(self.speed)
            if (self.velocity.x != 0 or self.velocity.y != 0):
                self.velocity.scale_to_length(self.speed)
            if self.flippedImage == True:
                self.image = pygame.transform.flip(self.idleSprites[int(self.current_sprite)], True, False)
            else:
                self.image = pygame.transform.flip(self.idleSprites[int(self.current_sprite)], False, False)

            self.canMove = pygame.time.get_ticks() + 5
            self.collideDir = 0
        self.rect.move_ip(self.velocity)

    def attack(self, projectiles):
        player = self.rect.center
        cursor = pygame.mouse.get_pos()
        projectiles.add(Projectile(player, cursor, True, 'Magic Ball'))

    def checkCollide(self, group):
        health = self.current_health
        if (pygame.time.get_ticks() >= self.iframes):
            for e in group:
                if self.rect.colliderect(e.rect):
                    self.iframes = pygame.time.get_ticks() + 1000
                    self.get_hit(1)
                    break
        if self.current_health != health:
            print(self.current_health)

    def get_health(self):
        return self.current_health

    def get_hit(self, hitDmg):
        if (self.current_health - hitDmg) > 0:
            self.current_health -= hitDmg
        else:
            self.current_health = 0
            self.alive = False

    def get_regen(self, regenAmt):
        if (regenAmt + self.current_health) < self.max_health:
            self.current_health += regenAmt
        else:
            self.current_health = self.max_health

    def get_collisions(self, tiles):
        collisions = []
        for t in tiles:
            if self.rect.colliderect(t):
                collisions.append(t)
        return collisions

    def check_collisionsx(self, tiles):
        collisions = self.get_collisions(tiles)
        for t in collisions:
            if self.velocity.x > 0:
                self.rect.x = t.rect.left - self.rect.w - 1
                self.collideDir = 4
            elif self.velocity.x < 0:
                self.rect.x = t.rect.right + 1
                self.collideDir = 3
            elif self.velocity.y > 0:
                #self.velocity.y = 0
                self.rect.bottom = t.rect.top - 1
                self.collideDir = 1
            elif self.velocity.y < 0:
                #self.velocity.y = 0
                self.rect.bottom = t.rect.bottom + self.rect.h + 1
                self.collideDir = 2
    
    def check_collisionsy(self, tiles):
        collisions = self.get_collisions(tiles)
        #self.rect.bottom += 1
        for t in collisions:
            verticalMove = False
            if self.velocity.y != 0:
                verticalMove = True
            if self.velocity.x > 0:
                if verticalMove == False:
                    self.rect.x = t.rect.left - self.rect.w
                    self.collideDir = 4
                    self.velocity.x = 0
                else:
                    horizontal = sqrt(pow(t.rect.left - self.rect.centerx, 2) + pow(t.rect.centery - self.rect.centery, 2))
                    vertical = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.top - self.rect.centery, 2))
                    vertical2 = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.bottom - self.rect.centery, 2))
                    min1 = min(horizontal, vertical, vertical2)
                    if min1 == horizontal:
                        self.rect.x = t.rect.left - self.rect.w
                        self.collideDir = 4
                        self.velocity.x = 0
                        self.velocity.y = 0
                    elif min1 == vertical:
                        self.velocity.y = 0
                        self.velocity.x = 0
                        self.rect.bottom = t.rect.top
                        self.collideDir = 1
                    elif min1 == vertical2:
                        self.velocity.y = 0
                        self.velocity.x = 0
                        self.rect.bottom = t.rect.bottom + self.rect.h
                        self.collideDir = 2
            if self.velocity.x < 0:
                if verticalMove == False:
                    self.rect.x = t.rect.right
                    self.collideDir = 3
                    self.velocity.x = 0
                else:
                    horizontal = sqrt(pow(t.rect.right - self.rect.centerx, 2) + pow(t.rect.centery - self.rect.centery, 2))
                    vertical = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.top - self.rect.centery, 2))
                    vertical2 = sqrt(pow(t.rect.centerx - self.rect.centerx, 2) + pow(t.rect.bottom - self.rect.centery, 2))
                    min1 = min(horizontal, vertical, vertical2)
                    if min1 == horizontal:
                        self.rect.x = t.rect.left - self.rect.w
                        self.collideDir = 4
                        self.velocity.y = 0
                        self.velocity.x = 0
                    elif min1 == vertical:
                        self.velocity.y = 0
                        self.velocity.x = 0
                        self.rect.bottom = t.rect.top
                        self.collideDir = 1
                    elif min1 == vertical2:
                        self.velocity.y = 0
                        self.velocity.x = 0
                        self.rect.bottom = t.rect.bottom + self.rect.h
                        self.collideDir = 2
            if self.velocity.y > 0:
                self.velocity.y = 0
                self.rect.bottom = t.rect.top
                self.collideDir = 1
            if self.velocity.y < 0:
                self.velocity.y = 0
                self.rect.bottom = t.rect.bottom + self.rect.h
                self.collideDir = 2


    def update(self, keys, group, tiles):
        #Update Sprite Animation
        self.current_sprite += 0.05 # Controls how fast the animations cycle
        if self.current_sprite >= len(self.idleSprites):
            self.current_sprite = 0
        self.image = self.idleSprites[int(self.current_sprite)]

        self.move(keys)
        self.checkCollide(group)
        #self.check_collisionsx(tiles)
        self.check_collisionsy(tiles)

    # Reset char after dying; doesn't work quite yet
    def reset(self):
        self.current_health = 4
        self.alive = True

    
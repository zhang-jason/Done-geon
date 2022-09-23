from os.path import join
from os.path import dirname
from Entities.entity import Entity
import pygame
import pygame.locals as c


class Player(Entity):
    def __init__(self, startPosition):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets', 'candleA_01.png')), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition
        # how often the character can move (every five ticks)
        self.canMove = pygame.time.get_ticks() + 5
        self.speed = 5  # how far it moves
        self.current_health = 4
        self.max_health = 4
        self.iframes = 0
        self.alive = True

    def move(self, keys):
        move = pygame.math.Vector2()
        if pygame.time.get_ticks() >= self.canMove:
            if keys[c.K_UP] and self.collideDir != 2:
                move.y -= self.speed
            if keys[c.K_DOWN] and self.collideDir != 1:
                move.y += self.speed
            if keys[c.K_LEFT] and self.collideDir != 3:
                move.x -= self.speed
            if keys[c.K_RIGHT] and self.collideDir != 4:
                move.x += self.speed
            if (move.x != 0 or move.y != 0):
                move.scale_to_length(self.speed)
            self.canMove = pygame.time.get_ticks() + 5
            self.collideDir = 0
        self.rect.move_ip(move)

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

    def update(self, keys, group):
        self.move(keys)
        self.checkCollide(group)

    # Reset char after dying; doesn't work quite yet
    def reset(self):
        self.current_health = 4
        self.alive = True
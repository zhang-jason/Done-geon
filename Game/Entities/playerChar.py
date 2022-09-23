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
        self.speed = 2  # how far it moves
        self.health = 10
        self.iframes = 0

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

    # temp function to demo how health system could look

    def checkCollide(self, group):
        health = self.health
        if (pygame.time.get_ticks() >= self.iframes):
            for e in group:
                if self.rect.colliderect(e.rect):
                    self.iframes = pygame.time.get_ticks() + 1000
                    self.health -= 1
                    break
        if self.health != health:
            print(self.health)

    def update(self, keys, group):
        self.move(keys)
        self.checkCollide(group)

   
import pygame
import math
from Entities.entity import Entity
from os.path import join
from os.path import dirname

class Projectile(Entity):
    def __init__(self, startPosition, endPosition):
        super(Projectile, self).__init__()

        self.sprites = []
        for i in range(1, 30, 1):
            self.sprites.append(pygame.transform.scale(pygame.image.load(
                join(dirname(dirname(__file__)), 'assets/projectiles/fireball', f'{i}.png')), (16, 16)))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.distance = endPosition - startPosition
        self.speed = 5
        self.canMove = 0
        
    #Override
    def update(self, WIN):
        # Update Animation
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        # Update Position
        move = pygame.math.Vector2(self.endPosition[0]-self.startPosition[0], self.endPosition[1]-self.startPosition[1])
        if pygame.time.get_ticks() >= self.canMove:
            if self.collideDir == 3 or self.collideDir == 4:
                move.x = 0
            if self.collideDir == 1 or self.collideDir == 2:
                move.y = 0
            if (move.x != 0 or move.y != 0):
                move.scale_to_length(self.speed)
                #move *= -1
                # uncomment to have enemies run from player
            self.canMove = pygame.time.get_ticks() + 10
            self.rect.move_ip(move)
            self.collideDir = 0
        WIN.blit(self.image, self.rect)
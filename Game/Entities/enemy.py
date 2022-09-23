import pygame
from Entities.entity import Entity
from os.path import join
from os.path import dirname


class Enemy(Entity):
    def __init__(self, startPosition, player):
        super(Enemy, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets', 'candleA_01.png')), (32, 32))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition
        self.canMove = 0
        self.speed = 3
        self.player = player

    def update(self):
        pCoords = self.player.rect.center
        coords = self.rect.center
        move = pygame.math.Vector2(pCoords[0]-coords[0], pCoords[1]-coords[1])
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
    
    

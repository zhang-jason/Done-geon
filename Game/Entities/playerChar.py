from os.path import join
from os.path import dirname
import pygame
import pygame.locals as c

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(join(dirname(dirname(__file__)), 'assets', 'candleA_01.png')),(32,32))
        self.rect = self.image.get_rect()
        self.canMove = pygame.time.get_ticks() + 5  #how often the character can move (every five ticks)
        self.speed = 1  #how far it moves


    def move(self, keys):
        x,y = 0,0
        if pygame.time.get_ticks() >= self.canMove:
            if keys[c.K_UP]:
                y -= self.speed
            if keys[c.K_DOWN]:
                y += self.speed
            if keys[c.K_LEFT]:
                x -= self.speed
            if keys[c.K_RIGHT]:
                x += self.speed
            self.canMove = pygame.time.get_ticks() + 5
        self.rect.move_ip(x,y)
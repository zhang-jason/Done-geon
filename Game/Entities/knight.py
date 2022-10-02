import pygame
from Entities.enemy import Enemy
from Entities.projectile import Projectile
from os.path import join
from os.path import dirname

class Knight(Enemy):
    def __init__(self, startPosition, player):
        super(Knight, self).__init__(startPosition, player)

        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Knight/Idle', 'knight_f_idle_anim_f0.png')), (48, 84)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Knight/Idle', 'knight_f_idle_anim_f1.png')), (48, 84)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Knight/Idle', 'knight_f_idle_anim_f2.png')), (48, 84)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Knight/Idle', 'knight_f_idle_anim_f3.png')), (48, 84)))
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition

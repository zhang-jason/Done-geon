import pygame

from Game.Entities.enemy import Enemy
from Game.Entities.entity import Entity
from Game.Entities.projectile import Projectile
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

        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Knight/Idle', 'knight_f_idle_anim_f0.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in self.sprites:
            x.set_colorkey(trans_color)

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition

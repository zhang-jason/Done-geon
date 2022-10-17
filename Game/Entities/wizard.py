import pygame

from Entities.enemy import Enemy
from Entities.projectile import Projectile
from os.path import join
from os.path import dirname
from random import randint


class Wizard(Enemy):
    def __init__(self, startPosition, player):
        super(Wizard, self).__init__(startPosition, player)

        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Wizard/Idle', 'wizzard_m_idle_anim_f0.png')).convert_alpha(),
                                                   (48, 84)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Wizard/Idle', 'wizzard_m_idle_anim_f1.png')).convert_alpha(),
                                                   (48, 84)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Wizard/Idle', 'wizzard_m_idle_anim_f2.png')).convert_alpha(),
                                                   (48, 84)))
        self.sprites.append(pygame.transform.scale(pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Wizard/Idle', 'wizzard_m_idle_anim_f3.png')).convert_alpha(),
                                                   (48, 84)))
        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/Wizard/Idle', 'wizzard_m_idle_anim_f0.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in self.sprites:
            x.set_colorkey(trans_color)

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition

    # Ranged enemy has special attack
    def attack(self, projectiles):
        enemy = self.rect.center
        pCoords = self.player.rect.center
        projectiles.add(Projectile(enemy, pCoords, False, 'Pink Ball'))

    def update(self, projectiles):
        super(Wizard, self).update(projectiles)

        # Scuffed random attack pattern generator
        randAttack = randint(1, 250)
        if randAttack == 1:
            self.attack(projectiles)

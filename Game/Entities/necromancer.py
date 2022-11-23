from Entities.projectile import Projectile
from Entities.playerChar import Player
from os.path import join, dirname
import pygame
import pygame.locals as c
from pygame import mixer
from dirMods import getImages

class Necromancer(Player):
    def __init__(self, startPosition, TILE_SIZE,player= None):
        size = (TILE_SIZE*2//3, TILE_SIZE*5//6)

        self.idleSprites = self.__getSprites__('Necromancer', 'Idle', size)
        self.runSprites = self.__getSprites__('Necromancer', 'Run', size)
        self.attackSprites = self.__getSprites__('Necromancer', 'Attack', size)
        self.projectileSprites = getImages((join(dirname(dirname(__file__)), 'assets/Projectiles/Magic_Ball')), (TILE_SIZE*3//4, TILE_SIZE*3//4))
        self.currentSprites = self.idleSprites

        self.current_sprite = 0
        self.image = self.currentSprites[self.current_sprite]
        self.rect = self.image.get_rect()
        if player is None:
            self.rect.centerx, self.rect.centery = startPosition
        else:
            self.rect.centerx, self.rect.centery = player.rect.centerx, player.rect.centery

        self.canAttack = pygame.time.get_ticks() + 480
        self.attack_sound = mixer.Sound(join(dirname(dirname(__file__)), 'assets/SFX/Game/Player', 'Ranged_Attack.wav'))
        super(Necromancer, self).__init__(startPosition, TILE_SIZE,player)

    def attack(self, projectiles):
        player = self.rect.center
        cursor = pygame.mouse.get_pos()
        self.canAttack = pygame.time.get_ticks() + 480
        projectiles.add(Projectile(player, cursor, True, 'Magic Ball', (self.TILE_SIZE*3//4, self.TILE_SIZE*3//4), self.projectileSprites))

    def update(self):
        if self.attacking:
            self.currentSprites = self.attackSprites
        else:
            if self.moving:
                self.currentSprites = self.runSprites
            else:
                self.currentSprites = self.idleSprites

        if self.attacking:
            self.current_sprite += 0.10  # Controls how fast the animations cycle
        else:
            self.current_sprite += 0.05

        super(Necromancer, self).update()
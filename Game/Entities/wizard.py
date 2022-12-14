from Entities.enemy import Enemy
from Entities.projectile import Projectile
from dirMods import getImages
from os.path import join, dirname
from random import randint
import numpy as np

class Wizard(Enemy):
    def __init__(self, startPosition, player, TILE_SIZE, boss):
        self.TILE_SIZE = TILE_SIZE
        super(Wizard, self).__init__(startPosition, player, boss)
        size = (TILE_SIZE // 2, TILE_SIZE * 3 // 4)
        self.sprites = self.__getSprites__('Wizard', 'Run', np.array(size) * (4 if boss else 1))
        self.projectileSprites = getImages((join(dirname(dirname(__file__)), f'assets/Projectiles/Enemy_Ball_{randint(1,6)}')), (TILE_SIZE*3//4, TILE_SIZE*3//4))
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = startPosition

    # Ranged enemy has special attack
    def attack(self, projectiles):
        enemy = self.rect.center
        pCoords = self.player.rect.center
        projectiles.add(Projectile(enemy, pCoords, False, f'Enemy_Ball', (self.TILE_SIZE*3//4, self.TILE_SIZE*3//4), self.projectileSprites))

    def update(self, projectiles):
        super(Wizard, self).update(projectiles)

        # Scuffed random attack pattern generator
        randAttack = randint(1, 250)
        if randAttack == 1:
            self.attack(projectiles)

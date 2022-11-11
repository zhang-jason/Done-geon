from Entities.enemy import Enemy
from Entities.projectile import Projectile
from random import randint

class Wizard(Enemy):
    def __init__(self, startPosition, player, TILE_SIZE):
        self.TILE_SIZE = TILE_SIZE
        super(Wizard, self).__init__(startPosition, player)
        size = (TILE_SIZE // 2, TILE_SIZE * 3 // 4)
        self.sprites = self.__getSprites__('Wizard', 'Run', size)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = startPosition

    # Ranged enemy has special attack
    def attack(self, projectiles):
        enemy = self.rect.center
        pCoords = self.player.rect.center
        projectiles.add(Projectile(enemy, pCoords, False, 'Pink Ball', self.TILE_SIZE))

    def update(self, projectiles):
        super(Wizard, self).update(projectiles)

        # Scuffed random attack pattern generator
        randAttack = randint(1, 250)
        if randAttack == 1:
            self.attack(projectiles)

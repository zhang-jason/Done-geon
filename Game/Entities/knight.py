from Entities.enemy import Enemy
import numpy as np
class Knight(Enemy):
    def __init__(self, startPosition, player, TILE_SIZE, boss):
        super(Knight, self).__init__(startPosition, player,boss)
        size = (TILE_SIZE // 2, TILE_SIZE * 3 // 4)
        self.sprites = self.__getSprites__('Knight', 'Run', np.array(size) * (4 if boss else 1))
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = startPosition

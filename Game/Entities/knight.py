from Entities.enemy import Enemy
class Knight(Enemy):
    def __init__(self, startPosition, player, TILE_SIZE):
        super(Knight, self).__init__(startPosition, player)
        size = (TILE_SIZE // 2, TILE_SIZE * 3 // 4)
        self.sprites = self.__getSprites__('Knight', 'Run', size)
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = startPosition

import pygame
from Entities.entity import Entity
from os import listdir
from os.path import join, dirname, isfile

class VFX(Entity):
    def __init__(self, type, size, position, one_time=False, sprites=None):
        super(VFX, self).__init__()

        self.type = type
        self.one_time = one_time
        if self.one_time:
            self.done = False
        if sprites == None:
            self.sprites = self.__getSprites__(type, size)
        else:
            self.sprites = sprites
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.static_position = position

    def update(self, position=None, speed=0.20):
        # Update Sprite Animation
        self.current_sprite += speed
        if self.current_sprite >= len(self.sprites):
            if self.one_time:
                self.done = True
                return
            else:
                self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]
        self.rect = self.image.get_rect()
        if position is not None:
            self.rect.center = position
        else:
            self.rect.center = self.static_position


    def __getSprites__(self, type, size):
        spriteList = []
        dirPath = join(dirname(dirname(__file__)), f'game/assets/VFX/{type}')
        for i, file in enumerate(listdir(dirPath)):
            f = join(dirPath, f'{i}.png')
            if isfile(f):
                spriteList.append(pygame.transform.scale(pygame.image.load(f), size))

        trans_image = pygame.image.load(join(dirPath, '0.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in spriteList:
            x.set_colorkey(trans_color)

        return spriteList
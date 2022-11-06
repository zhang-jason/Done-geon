import pygame
from Entities.entity import Entity
from os.path import join
from os.path import dirname

class Trap(Entity):
    def __init__(self, position, type, TILE_SIZE):
        super(Trap, self).__init__()

        self.position = position
        self.type = type
        self.activate = False
        self.cooldown = 0
        #self.size = (TILE_SIZE*3//4, TILE_SIZE*3//4)

        # Image and Animations
        self.sprites = []
        for i in range(1, 5, 1):
            image = pygame.transform.scale(pygame.image.load(
                join(dirname(dirname(__file__)), f'assets/Traps/{type}', f'{i}.png')), (TILE_SIZE, TILE_SIZE))
            self.sprites.append(image)
        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), f'assets/Traps/{type}', '1.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in self.sprites:
            x.set_colorkey(trans_color)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = position

    def update(self):
        if self.activate:
            if self.activate:
                self.cooldown = 10

                if int(self.current_sprite) <= 3:
                    self.current_sprite += 0.20
                    if self.current_sprite > len(self.sprites):
                        self.current_sprite = 3
                        self.activate = False
                    self.image = self.sprites[int(self.current_sprite)]
                else:
                    self.activate = False
        else:
            if self.current_sprite > 0:
                self.current_sprite -= 0.20
                if self.current_sprite <= 0:
                    self.current_sprite = 0
                self.image = self.sprites[int(self.current_sprite)]
            if self.cooldown > 0:
                self.cooldown -= 0.05
from os.path import join
from os.path import dirname
import pygame
import pygame.locals as c
from pygame import font

from Entities.entity import Entity
from Entities.playerChar import Player


class HealthBar():

    def __init__(self, WIN, player, TILE_SIZE):
        super(HealthBar, self).__init__()
        self.TILE_SIZE = TILE_SIZE
        # Variable Stuff
        self.max_health = player.current_health
        self.current_health = self.max_health
        self.health_bar_length = TILE_SIZE * 4
        self.health_ratio = self.max_health / self.health_bar_length

        # Debugging Stuff
        # print("Player Health: " + str(player.max_health))
        # print("Health Ratio: " + str(self.health_ratio))
        # print("Health Length: " + str(self.health_bar_length))

        # Actual Health Image 
        self.image = pygame.transform.scale(pygame.image.load(join(dirname(dirname(__file__)), 'game/assets',
                                                                   'health_ui.png')), (TILE_SIZE * 5, TILE_SIZE))
        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'game/assets', 'health_ui.png'))
        trans_color = trans_image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()

    def update(self, WIN, player):
        self.current_health = player.current_health
        self.healthBarRect = (
            self.rect.left + self.TILE_SIZE + self.TILE_SIZE // 16, self.rect.top + self.TILE_SIZE // 6,
            self.current_health * self.TILE_SIZE * 15 // 16, self.TILE_SIZE * 2 // 3)
        pygame.draw.rect(WIN, (255, 0, 0), self.healthBarRect)  # Should this be done here??
        WIN.blit(self.image, self.rect)


class BoneCounter():

    def __init__(self, WIN, player, TILE_SIZE):
        super(BoneCounter, self).__init__()
        self.TILE_SIZE = TILE_SIZE
        # Variable Stuff
        self.bones = player.bones
        self.bone_counter_length = TILE_SIZE * 4

        # Debugging Stuff
        # print("Player Health: " + str(player.max_health))
        # print("Health Ratio: " + str(self.health_ratio))
        # print("Health Length: " + str(self.health_bar_length))

        # Actual Health Image
        self.image = pygame.transform.scale(pygame.image.load(join(dirname(dirname(__file__)), 'game/assets',
                                                                   'bone_counter.png')),
                                            (TILE_SIZE * 3, TILE_SIZE))
        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'game/assets', 'health_ui.png'))
        trans_color = trans_image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        fontDir = join(dirname(dirname(__file__)), 'Game/', 'Toriko.ttf')
        self.font = pygame.font.Font(fontDir, round(TILE_SIZE))

    def update(self, WIN, player):
        self.bones = player.bones
        self.rect.left = self.TILE_SIZE * 12
        text = self.font.render(str(player.bones), True, pygame.color.Color(0))
        text_rect = text.get_rect()
        text_rect.left = self.TILE_SIZE * 13
        text_rect.centery = self.rect.centery + self.rect.centery // 3
        WIN.blit(self.image, self.rect)
        WIN.blit(text, text_rect)
        # TODO: Change this to update in main, we're passing the whole freaking window in here

class Inventory():
    
    def __init__(self, WIN, TILE_SIZE):
        super(Inventory, self).__init__()
        self.TILE_SIZE = TILE_SIZE
        self.image = pygame.transform.scale(pygame.image.load(join(dirname(dirname(__file__)), 'game/assets/inventory',
                                                                    'empty.png')), (self.TILE_SIZE, self.TILE_SIZE))

        # Variable Stuff
        self.currItem = ''
        #self.itemList = []

    def update(self, WIN, player):
        self.currItem = player.powerup

        self.image = pygame.transform.scale(pygame.image.load(join(dirname(dirname(__file__)), 'game/assets/inventory',
                                                                f'{self.currItem}.png')), (self.TILE_SIZE, self.TILE_SIZE))
        self.image_rect = self.image.get_rect()
        self.image_rect.left = self.TILE_SIZE * 14
        self.image_rect.centery = self.TILE_SIZE * 8 + (self.TILE_SIZE // 2)
        WIN.blit(self.image, self.image_rect)

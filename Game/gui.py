from os.path import join
from os.path import dirname
import pygame
import pygame.locals as c
from Entities.entity import Entity
from Entities.playerChar import Player

class HealthBar():

    def __init__(self, WIN, player, position, TILE_SIZE):
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

        # Pos
        self.rect.left, self.rect.top = position

    def update(self, WIN, player):
        self.current_health = player.current_health
        self.healthBarRect = (self.rect.left + self.TILE_SIZE + self.TILE_SIZE//16, self.rect.top + self.TILE_SIZE//6, self.current_health * self.TILE_SIZE*15//16, self.TILE_SIZE*2//3)
        pygame.draw.rect(WIN, (255, 0, 0), self.healthBarRect)  # Should this be done here??
        WIN.blit(self.image, self.rect)
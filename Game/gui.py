from os.path import join
from os.path import dirname
import pygame
import pygame.locals as c
from Game.Entities.entity import Entity
from Game.Entities.playerChar import Player

class HealthBar():

    def __init__(self, WIN, player, position):
        super(HealthBar, self).__init__()

        # Variable Stuff
        self.max_health = player.current_health
        self.current_health = self.max_health
        self.health_bar_length = 290
        self.health_ratio = self.max_health / self.health_bar_length

        # Debugging Stuff
        print("Player Health: " + str(player.max_health))
        print("Health Ratio: " + str(self.health_ratio))
        print("Health Length: " + str(self.health_bar_length))

        # Actual Health Image 
        self.image = pygame.transform.scale(pygame.image.load(join(dirname(dirname(__file__)), 'game/assets', 'health_ui.png')),(400,80))
        self.rect = self.image.get_rect()

        # Pos
        self.rect.left, self.rect.top = position

    def update(self, WIN, player):
        self.current_health = player.current_health
        self.healthBarRect = (115, 40, self.current_health / self.health_ratio, 60)
        pygame.draw.rect(WIN, (255, 0, 0), self.healthBarRect)
        WIN.blit(self.image, self.rect)
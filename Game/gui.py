import pygame

class HealthBar():

    def __init__(self, health):
        self.max_health, self.current_health = health

    def hit(self):
        self.current_health -= 0.5
        if self.current_health == 0:
            return True # Use for Game End maybe

    def regen(self, regenAmt):
        if (regenAmt + self.current_health) > self.max_health:
            self.current_health += regenAmt
        else:
            self.current_health = self.max_health

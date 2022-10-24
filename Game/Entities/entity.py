import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.target = [0, 0]
        self.speed = 0
        self.collidable = 1
        self.dx = 0
        self.dy = 0

    def set_target(self, target):
        self.target = target

    def set_speed(self, speed):
        self.speed = speed

    # def collide(self, group2):
    #         collideTol = 10
    #         for j in group2:
    #             if self.rect.colliderect(j.rect):
    #                 if abs(j.rect.top - self.rect.bottom) < collideTol:
    #                     self.collideDir = 1 #cant move down
    #                 elif abs(j.rect.bottom - self.rect.top) < collideTol:
    #                     self.collideDir = 2 #cant move up
    #                 elif abs(j.rect.right - self.rect.left) < collideTol:
    #                     self.collideDir = 3 #cant move left
    #                 elif abs(j.rect.left - self.rect.right) < collideTol:
    #                     self.collideDir = 4 #cant move right
                        
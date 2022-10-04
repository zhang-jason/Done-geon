import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super(Entity, self).__init__()
        self.collideDir = 0

    def collide(self, group2):
            collideTol = 10
            for j in group2:
                if self.rect.colliderect(j.rect):
                    if abs(j.rect.top - self.rect.bottom) < collideTol:
                        self.collideDir = 1 #cant move down
                    elif abs(j.rect.bottom - self.rect.top) < collideTol:
                        self.collideDir = 2 #cant move up
                    elif abs(j.rect.right - self.rect.left) < collideTol:
                        if(self.collideDir == 1):
                            self.collideDir = 5
                        else:
                            self.collideDir = 3 #cant move left
                    elif abs(j.rect.left - self.rect.right) < collideTol:
                        self.collideDir = 4 #cant move right
                        
import pygame
from Entities.entity import Entity
from Entities.projectile import Projectile
from os import listdir
from os.path import join, dirname, isfile


class Enemy(Entity):
    def __init__(self, startPosition, player):
        super(Enemy, self).__init__()

        # Sprite Info
        self.sprites = []
        self.current_sprite = 0
        self.canMove = False
        self.speed = 3
        self.health = 4
        self.player = player
        self.collidable = 1
        self.damage = 1
        self.spawn_cooldown = 180
        # self.collideDir = 0

    def update(self, projectiles):
        # Update Sprite Animation
        if self.spawn_cooldown >= 0:
            self.spawn_cooldown -= 1
        else:
            self.canMove = True
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        if self.flippedImage:
            self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], True, False)
        else:
            self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], False, False)

    def __getSprites__(self, type, status, size):
        spriteList = []

        dirPath = join(dirname(dirname(__file__)), f'assets/{type}/{status}')
        for i, file in enumerate(listdir(dirPath)):
            f = join(dirPath, f'{i}.png')
            if isfile(f):
                spriteList.append(pygame.transform.scale(pygame.image.load(f), size))

        trans_image = pygame.image.load(join(dirPath, '0.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in spriteList:
            x.set_colorkey(trans_color)

        return spriteList

        # pCoords = self.player.rect.center
        # coords = self.rect.center
        # move = pygame.math.Vector2(pCoords[0]-coords[0], pCoords[1]-coords[1])
        # if pygame.time.get_ticks() >= self.canMove:
        #     if self.collideDir == 3 or self.collideDir == 4:
        #         move.x = 0
        #     if self.collideDir == 1 or self.collideDir == 2:
        #         move.y = 0
        #     if (move.x != 0 or move.y != 0):
        #         move.scale_to_length(self.speed)
        #         #move *= -1
        #         # uncomment to have enemies run from player
        #     self.canMove = pygame.time.get_ticks() + 10
        #     self.rect.move_ip(move)
        #     self.collideDir = 0

    # def collide(self, group2):
    #     collideTol = 10
    #     for j in group2:
    #         if self.rect.colliderect(j.rect):
    #             if abs(j.rect.top - self.rect.bottom) < collideTol:
    #                 self.collideDir = 1 #cant move down
    #             elif abs(j.rect.bottom - self.rect.top) < collideTol:
    #                 self.collideDir = 2 #cant move up
    #             elif abs(j.rect.right - self.rect.left) < collideTol:
    #                 self.collideDir = 3 #cant move left
    #             elif abs(j.rect.left - self.rect.right) < collideTol:
    #                 self.collideDir = 4 #cant move right
    

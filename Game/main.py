import os
from random import randint
import sys
from math import floor

# Modular Files
import components
from Entities.playerChar import Player
from Entities.nonMoveObj import Obj
from Entities.enemy import Enemy

import pygame
from pygame import QUIT

pygame.init()

display_info = pygame.display.Info()
width = display_info.current_w
height = display_info.current_h - 70  # 70 for window headers
NUM_TILES_X, NUM_TILES_Y = 16, 9


# 16x9 tiles
ASSET_SIZE = 32
scale = min(floor(height / NUM_TILES_Y / ASSET_SIZE), floor(width / NUM_TILES_X / ASSET_SIZE))
TILE_SIZE = ASSET_SIZE * scale
print(height)
print("TILE_SIZE =", TILE_SIZE)
WIDTH = TILE_SIZE * NUM_TILES_X
HEIGHT = TILE_SIZE * NUM_TILES_Y
print(WIDTH)
print(HEIGHT)  # Just double-checking my math here

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Done-geon")

print("Created Window")


def scale_image(image):
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


# temporary, to be modularized later:
STONE_TILE = scale_image(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'TileAsset32x32.png'))
                         .convert())
# to explain what this does, we define the stone tile sprite from the os' current directory/assets/TileAsset...,
# convert it to usable pygame image object, then load scale it to the biggest factor of 32x32 we can fit in the screen
print("Created STONE_TILE")

enemies = pygame.sprite.Group()
player = Player((width/2,height/2))
for i in range(5):
    enemies.add(Enemy((randint(0,width),randint(0,height)),player))

#testing collision - bush object
bush = Obj((150,150))

'''
TODO put non move objs in group for easy collision detecting
adding obj to object group
objects = pygame.sprite.Group()
objects.add(bush)
'''
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for x in range(NUM_TILES_X):
        for y in range(NUM_TILES_Y):
            WIN.blit(STONE_TILE, (x * TILE_SIZE, y * TILE_SIZE))

    # testing collision - printing
    WIN.blit(bush.image, bush.rect)

    WIN.blit(player.image, player.rect)

    for e in enemies:
        WIN.blit(e.image,e.rect)
        e.update()
    keys = pygame.key.get_pressed()
    player.update(keys,enemies)


    #detecting collision - TODO this should be func later 
    if player.rect.colliderect(bush.rect):
        print("collision detected")

    pygame.display.update()

import os
import sys
from math import floor
from time import sleep

# Modular Files
import components

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

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    for x in range(NUM_TILES_X):
        for y in range(NUM_TILES_Y):
            WIN.blit(STONE_TILE, (x * TILE_SIZE, y * TILE_SIZE))
    pygame.display.update()

import os
from random import randint
import sys
from math import floor

# Modular Files
import components
from Entities.playerChar import Player
from Entities.nonMoveObj import Obj
from Entities.wizard import Wizard
from Entities.knight import Knight
from gui import HealthBar
from tiles import *

import pygame
from pygame import MOUSEBUTTONDOWN, QUIT

pygame.init()

display_info = pygame.display.Info()
width = display_info.current_w
height = display_info.current_h - 70  # 70 for window headers
NUM_TILES_X, NUM_TILES_Y = 16, 9
FPS_CLOCK = pygame.time.Clock()

# 16x9 tiles
ASSET_SIZE = 16
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
pygame.mouse.set_visible(False)
cursor_img = pygame.transform.scale(pygame.image.load(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Game/Assets', 'Crosshair02.png')), (28, 28))
cursor_img_rect = cursor_img.get_rect()

print("Created Window")

map = TileMap(os.path.join(os.path.dirname(__file__), 'assets/tiles', 'Test Room 3_Tile Layer 1.csv'), TILE_SIZE)
map2 = TileMap(os.path.join(os.path.dirname(__file__), 'assets/tiles', 'Test Room 3_Tile Layer 2.csv'), TILE_SIZE)
map3 = TileMap(os.path.join(os.path.dirname(__file__), 'assets/tiles', 'Test Room 3_Tile Layer 3.csv'), TILE_SIZE)

def scale_image(image):
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

# temporary, to be modularized later:
STONE_TILE = scale_image(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'TileAsset32x32.png'))
                         .convert())
# to explain what this does, we define the stone tile sprite from the os' current directory/assets/TileAsset...,
# convert it to usable pygame image object, then load scale it to the biggest factor of 32x32 we can fit in the screen
print("Created STONE_TILE")

enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player = Player((width/2,height/2))
health = HealthBar(WIN, player, (20, 20))
for i in range(3):
    enemies.add(Wizard((randint(0,width),randint(0,height)),player))
    enemies.add(Knight((randint(0,width),randint(0,height)),player))

#non movable object group
nonMovingObj = pygame.sprite.Group()
for i in range(10):
    nonMovingObj.add(Obj((randint(0,width),randint(0,height))))

#nonMovingObj.add(map2.get_tiles())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            player.attack(projectiles)
    #for x in range(NUM_TILES_X):
    #    for y in range(NUM_TILES_Y):
    #        WIN.blit(STONE_TILE, (x * TILE_SIZE, y * TILE_SIZE))

    map.draw_map(WIN)
    map2.draw_map(WIN)
    map3.draw_map(WIN)

    # printing bushes 
    #for i in nonMovingObj:
        #WIN.blit(i.image, i.rect)
        #i.update()

    #nonMovingObj.add(map2.get_tiles())
    #hitbox = (player.rect.topleft[0], player.rect.topleft[1], player.rect.width, player.rect.height) # NEW
    #pygame.draw.rect(WIN, (255,0,0), hitbox,2)
    WIN.blit(player.image, player.rect)

    # Update Functions
    for e in enemies:
        WIN.blit(e.image,e.rect)
        e.update(projectiles)
        e.collide(nonMovingObj)
    for p in projectiles:
        WIN.blit(p.image, p.rect)
        p.update()
    keys = pygame.key.get_pressed()
    player.update(keys, enemies, map2.tiles)
    health.update(WIN, player)

    #detecting collision
    #player.collide1(nonMovingObj)
    #player.check_collisionsx(map2.tiles)
    #player.collide(map2.tiles)

    cursor_img_rect.center = pygame.mouse.get_pos()
    WIN.blit(cursor_img, cursor_img_rect)

    pygame.display.update()
    FPS_CLOCK.tick(120)
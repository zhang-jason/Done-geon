import os
from random import randint
import sys
from math import floor, sqrt
import pygame.locals as c

# Modular Files
import components
from Entities.playerChar import Player
from Entities.projectile import Projectile
from Entities.nonMoveObj import Obj
from Entities.wizard import Wizard
from Entities.knight import Knight
from gui import HealthBar
from tiles import *
from RandomGen.roomGen import Room
from server import Server

import pygame
from pygame import MOUSEBUTTONDOWN, QUIT, K_w

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
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'game/assets', 'Crosshair02.png')), (28, 28))
cursor_img_rect = cursor_img.get_rect()

print("Created Window")

# Creating a random number of generated rooms

# roomList = []
# for index, iter in enumerate(range(randint(3,6))):
#    room = Room(index, NUM_TILES_X, NUM_TILES_Y, TILE_SIZE)
#    roomList.append(room)


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

enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
player = Player((width / 3, height / 2), TILE_SIZE)
health = HealthBar(WIN, player, (20, 20), TILE_SIZE)
for i in range(3):
    enemies.add(Wizard((randint(0, width), randint(0, height)), player, TILE_SIZE))
    enemies.add(Knight((randint(0, width), randint(0, height)), player, TILE_SIZE))

# non movable object group
nonMovingObj = pygame.sprite.Group()
for i in range(5):
    nonMovingObj.add(Obj((randint(0, width), randint(0, height)), TILE_SIZE))

server = Server()
# server test variables
time = 0
roomIndex = 0


def clearTempContents():
    directory = os.path.join(os.path.dirname(__file__), 'assets/tiles/temprooms/')
    for file in os.listdir(directory):
        # fileName = os.path.join(dir, file)
        os.remove(os.path.join(directory, file))
        # print(fileName)


updateCount = 0
screen = "Game"  # can be "Start", "Game", "Pause", maybe lose/win?


def get_player_move(player, keys):  # sets target relative to player center
    player.dx = 0
    player.dy = 0
    if keys[c.K_w]:
        player.dy = -player.speed
    if keys[c.K_s]:
        player.dy = player.speed
    if keys[c.K_a]:
        player.flippedImage = True
        player.dx = -player.speed
    if keys[c.K_d]:
        player.flippedImage = False
        player.dx = player.speed


def move_calc(ent, speed):
    dx = ent.dx
    dy = ent.dy
    if speed == 0:
        ent.dx = 0
        ent.dy = 0
    elif abs(dx) == speed and abs(dy) == speed:
        ent.dx = (dx / abs(dx)) * speed / sqrt(2)  # todo: calculate this fraction based on target for enemies
        ent.dy = (dy / abs(dy)) * speed / sqrt(2)


#   TODO: get collision map
#  1234567890123456
# 11111111111111111
# 20000000000000000
# 30000000000000000
# 40000000000000000
# 50000000100000000
# 60000000100000000
# 70000000100000000
# 80000000100000000
# 91111111111111111
m1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
m2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
m3 = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
collision_map = [m1, m2, m2, m2, m3, m3, m3, m3, m1]  # uses y, x coords bc i'm lazy and messed it up


# TODO: add a boundary layer so even if there's no collidable tiles, the char doesn't go offscreen

def get_tile_at(x, y):
    tile_x = round(x / TILE_SIZE)
    tile_y = round(y / TILE_SIZE)
    # TODO: add some checks for out of bounds in array
    return collision_map[tile_y][tile_x]


def detect_collision(ent):
    if ent.dx > 0:  # check if tile ent would end up in is collidable, if so reduce d to 0
        if get_tile_at(player.rect.right + player.dx, player.rect.centery):
            ent.dx = 0
    elif ent.dx < 0:
        if get_tile_at(player.rect.left + player.dx, player.rect.centery):
            ent.dx = 0
    if ent.dy < 0:  # Down and up are backwards bc window is drawn top to bottom...
        if get_tile_at(player.rect.centerx, player.rect.top + player.dy):
            ent.dy = 0
    elif ent.dy > 0:
        if get_tile_at(player.rect.centerx, player.rect.bottom + player.dy):
            ent.dy = 0


def move_entities():
    move_calc(player, player.speed)
    detect_collision(player)
    player.rect.center = (player.rect.centerx + player.dx, player.rect.centery + player.dy)
    for p in projectiles:
        p.x += p.dx
        p.y += p.dy
        p.rect.center = (int(p.x), int(p.y))


while True:
    # User interaction:
    for event in pygame.event.get():
        if event.type == QUIT:  # User Quits, end server and clear cache
            pygame.quit()
            # server.endServer()
            clearTempContents()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                player.attack(projectiles)
                '''
                #Testing Random Room Hopping
                roomIndex += 1
                if roomIndex >= len(roomList):
                    roomIndex = 0
                room = roomList[roomIndex]
                '''

    # Remove old sprites to not hog resources; trust me, this got ugly on my old PC
    WIN.fill(0)
    keys = pygame.key.get_pressed()

    match screen:
        case "Game":
            # room.drawRoom(WIN)
            map.draw_map(WIN)
            map2.draw_map(WIN)
            map3.draw_map(WIN)
            # printing bushes
            for i in nonMovingObj:
                WIN.blit(i.image, i.rect)
                i.update()

            # hitbox = (player.rect.topleft[0], player.rect.topleft[1], player.rect.width, player.rect.height) # NEW
            # pygame.draw.rect(WIN, (255,0,0), hitbox,2)
            WIN.blit(player.image, player.rect)

            # Update Functions
            for e in enemies:  # TODO: refactor for updated movement
                WIN.blit(e.image, e.rect)
                e.update(projectiles)
                e.collide(nonMovingObj)
            for p in projectiles:
                WIN.blit(p.image, p.rect)
                p.update()
            get_player_move(player, keys)
            move_entities()  # TODO: Add enemies to this
            player.update()
            health.update(WIN, player)
            # To be deleted:
            #   detecting collision
            #   player.collide(nonMovingObj)
            #   player.collide(map2.get_tiles())  ?

            cursor_img_rect.center = pygame.mouse.get_pos()
            WIN.blit(cursor_img, cursor_img_rect)

        case "Start":
            print("Start screen!")
            screen = "Start"

        case other:
            print("Invalid state, return to start screen!")
            screen = "Start"
        # End match case

    # test server sender
    if keys[K_w] and time < pygame.time.get_ticks():
        server.sendMsg(str(pygame.time.get_ticks()))
        time = pygame.time.get_ticks() + 1000

    pygame.display.update()
    updateCount += 1
    if updateCount % 600 == 0:
        print("FPS:", int(FPS_CLOCK.get_fps()))
        updateCount = 1
    FPS_CLOCK.tick(120)
    # end while loop

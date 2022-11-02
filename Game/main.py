import os
from random import choice, randint
import sys
from math import floor, sqrt
from numpy import power
import pygame.locals as c

# Modular Files
import components
from Entities.playerChar import Player
from Entities.projectile import Projectile
from Entities.powerup import Powerup
from Entities.nonMoveObj import Obj
from Entities.wizard import Wizard
from Entities.knight import Knight
from gui import *
from tiles import *
from RandomGen.roomGen import Room
from server import Server

import pygame
from pygame import constants

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

'''
map = TileMap(os.path.join(os.path.dirname(__file__), 'assets/tiles', 'Test Room 3_Tile Layer 1.csv'), TILE_SIZE)
map2 = TileMap(os.path.join(os.path.dirname(__file__), 'assets/tiles', 'Test Room 3_Tile Layer 2.csv'), TILE_SIZE)
map3 = TileMap(os.path.join(os.path.dirname(__file__), 'assets/tiles', 'Test Room 3_Tile Layer 3.csv'), TILE_SIZE)
'''


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
mouse_pressed = 0
mouse_right_pressed = 0
key_shift_pressed = 0
health = HealthBar(WIN, player, TILE_SIZE)
bone_bar = BoneCounter(WIN, player, TILE_SIZE)
inventory = Inventory(WIN, TILE_SIZE)

server = Server()
# server test variables
time = 0
roomIndex = 0


def clearTempContents():
    directory = os.path.join(os.path.dirname(__file__), 'assets/tiles/temprooms/')
    retain = ['.gitignore']
    for file in os.listdir(directory):
        if file not in retain:
            os.remove(os.path.join(directory, file))


updateCount = 0
screen = "Game"  # can be "Start", "Game", "Pause", maybe lose/win?


def get_player_move(player_ent, keys_main):  # sets target relative to player center
    player_ent.dx = 0
    player_ent.dy = 0
    if keys_main[c.K_w]:
        player_ent.dy = -player_ent.speed
    if keys_main[c.K_s]:
        player_ent.dy = player_ent.speed
    if keys_main[c.K_a]:
        player_ent.flippedImage = True
        player_ent.dx = -player_ent.speed
    if keys_main[c.K_d]:
        player_ent.flippedImage = False
        player_ent.dx = player_ent.speed


def move_calc_player(ent):
    dx = ent.dx
    dy = ent.dy
    if ent.speed == 0:
        ent.dx = 0
        ent.dy = 0
    elif abs(dx) == ent.speed and abs(dy) == ent.speed:
        ent.dx = (dx / abs(dx)) * ent.speed / sqrt(2)
        ent.dy = (dy / abs(dy)) * ent.speed / sqrt(2)


#   TODO: get collision map
#   123456789012345678
# 1 111111111111111111
# 2 111111111111111111
# 3 100000000000000001
# 4 101000000000000101
# 5 100011000010000001
# 6 100011000000000001
# 7 100011000000000001
# 8 101000000000000001
# 9 111111111111111111
m1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
m3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
m4 = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
m5 = [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
m6 = [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
m7 = [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
m8 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
collision_map = [m1, m1, m3, m4, m5, m6, m7, m8, m1]  # uses y, x coords bc i'm lazy and messed it up


def get_tile_at(x, y):
    x = x - TILE_SIZE / 2
    y = y - TILE_SIZE / 2
    tile_x = round(x / TILE_SIZE)
    tile_y = round(y / TILE_SIZE)
    if tile_x < 0 or tile_x > 15:
        return 1
    return collision_map[tile_y][tile_x]


def detect_collision(ent):
    if ent.collidable:
        if ent.dx > 0:  # check if tile ent would end up in is collidable, if so reduce d to 0
            if get_tile_at(ent.rect.right + ent.dx, ent.rect.centery):
                ent.dx = 0
        elif ent.dx < 0:
            if get_tile_at(ent.rect.left + ent.dx, ent.rect.centery):
                ent.dx = 0
        if ent.dy < 0:  # Down and up are backwards bc window is drawn top to bottom...
            if get_tile_at(ent.rect.centerx, ent.rect.top + ent.dy):
                ent.dy = 0
        elif ent.dy > 0:
            if get_tile_at(ent.rect.centerx, ent.rect.bottom + ent.dy):
                ent.dy = 0
    else:
        print("ent is non-collidable! This is probably an error!")


def move_calc_enemy(ent):
    if ent.speed != 3:
        print(ent.speed)
    player_x = ent.player.rect.centerx
    player_y = ent.player.rect.centery
    if ent.speed == 0:
        ent.dx = 0
        ent.dy = 0
    else:
        diff_x = player_x - ent.rect.centerx
        diff_y = player_y - ent.rect.centery
        if diff_x == 0 and diff_y == 0:
            ent.dx = 0
            ent.dy = 0
        else:
            # custom scaling bc the scaling was being weird with vector math
            #
            diff_x_scaled = diff_x / sqrt(pow(diff_x, 2) + pow(diff_y, 2))
            diff_y_scaled = diff_y / sqrt(pow(diff_x, 2) + pow(diff_y, 2))
            diff_x_scaled *= ent.speed
            diff_y_scaled *= ent.speed
            ent.dx = diff_x_scaled
            ent.dy = diff_y_scaled


def move_entities():
    move_calc_player(player)
    detect_collision(player)
    player.rect.center = (player.rect.centerx + player.dx, player.rect.centery + player.dy)
    for e in enemies:
        move_calc_enemy(e)
        detect_collision(e)
        e.x = e.rect.centerx + e.dx
        e.y = e.rect.centery + e.dy
        e.rect.center = (int(e.x), int(e.y))
    for p in projectiles:
        p.x += p.dx
        p.y += p.dy
        p.rect.center = (int(p.x), int(p.y))
        # TODO: remove projectiles upon OOB or tile collision?


def detect_projectile(p):
    if p.type:  # true for friendly
        for e in enemies:
            if e.rect.collidepoint(p.rect.center):
                p.kill()
                e.kill()
                player.bones += 1
    else:
        if player.rect.collidepoint(p.rect.center):
            p.kill()
            player.get_hit(p.damage)


def detect_melee(e):
    if player.rect.collidepoint(e.rect.center):
        player.get_hit(e.damage)


def detect_item(p):
    if player.rect.collidepoint(p.rect.center):
        player.get_powerup(p.ability)
        p.kill()


roomList = []
for index, iter in enumerate(range(randint(3, 6))):
    room = Room(index, NUM_TILES_X, NUM_TILES_Y, TILE_SIZE)
    roomList.append(room)

font = pygame.font.SysFont('Arial', round(TILE_SIZE))

while True:
    # User interaction:
    for event in pygame.event.get():
        if event.type == constants.QUIT:  # User Quits, end server and clear cache
            pygame.quit()
            server.endServer()
            clearTempContents()
            sys.exit()
        if event.type == constants.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pressed = 1
            elif event.button == 3:
                mouse_right_pressed = 1
            # if event.button == 1:
            #     player.attack(projectiles)

        if event.type == constants.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pressed = 0
            elif event.button == 3:
                mouse_right_pressed = 0

        if event.type == constants.KEYDOWN:
            if event.key == constants.K_e:
                player.use_powerup()
            elif event.key == constants.K_SPACE:
                # Testing Random Room Hopping
                roomIndex += 1
                if roomIndex >= len(roomList):
                    roomIndex = 0
                room = roomList[roomIndex]
            elif event.key == constants.K_RSHIFT or event.key == constants.K_LSHIFT:
                key_shift_pressed = 1
        if event.type == constants.KEYUP:
            if event.key == constants.K_RSHIFT or event.key == constants.K_LSHIFT:
                key_shift_pressed = 0

    # Remove old sprites to not hog resources; trust me, this got ugly on my old PC
    WIN.fill(0)
    keys = pygame.key.get_pressed()

    match screen:
        case "Game":
            room.drawRoom(WIN)
            # map.draw_map(WIN)
            # map2.draw_map(WIN)
            # map3.draw_map(WIN)

            # hitbox = (player.rect.topleft[0], player.rect.topleft[1], player.rect.width, player.rect.height) # NEW
            # pygame.draw.rect(WIN, (255,0,0), hitbox,2)

            # Update Functions
            if len(enemies) < 1:
                for i in range(round(player.bones / 4 + 1)):
                    enemies.add(
                        Wizard((randint(TILE_SIZE * 2, width - TILE_SIZE * 2),
                                randint(TILE_SIZE * 2, height - TILE_SIZE * 2)), player,
                               TILE_SIZE))
                    enemies.add(
                        Knight((randint(TILE_SIZE * 2, width - TILE_SIZE * 2),
                                randint(TILE_SIZE * 2, height - TILE_SIZE * 2)), player,
                               TILE_SIZE))
            for e in enemies:
                WIN.blit(e.image, e.rect)
                e.update(projectiles)
            for p in projectiles:
                WIN.blit(p.image, p.rect)
                p.update()
            get_player_move(player, keys)
            move_entities()
            for p in projectiles:
                detect_projectile(p)
            for e in enemies:
                if e.__class__ == Knight:  # TODO: change to be in the melee function, shouldn't be exclusive to knights
                    detect_melee(e)
            for p in room.powerups:
                detect_item(p)
            player.update()
            if mouse_pressed:
                player.attack(projectiles)
            if key_shift_pressed:
                player.sprint()
            WIN.blit(player.image, player.rect)
            health.update(WIN, player)
            bone_bar.update(WIN, player)
            inventory.update(WIN, player)

            # player_tile_x = round((player.rect.centerx - TILE_SIZE / 2) / TILE_SIZE)
            # player_tile_y = round((player.rect.centery - TILE_SIZE / 2) / TILE_SIZE)
            # print("Tile:", player_tile_x, player_tile_y)  # for debugging
            # WIN.blit(STONE_TILE, (player_tile_x * TILE_SIZE, player_tile_y * TILE_SIZE))
            # i = 0
            # for e in enemies:
            #     if i == 0:
            #         enemy0_tile_x = round((e.rect.centerx - TILE_SIZE / 2) / TILE_SIZE)
            #         enemy0_tile_y = round((e.rect.centery - TILE_SIZE / 2) / TILE_SIZE)
            #         print("Tile:", enemy0_tile_x, enemy0_tile_y)  # for debugging
            #         WIN.blit(STONE_TILE, (enemy0_tile_x * TILE_SIZE, enemy0_tile_y * TILE_SIZE))
            #     i += 1

            # To be deleted:
            #   detecting collision
            #   player.collide(nonMovingObj)
            #   player.collide(map2.get_tiles())  ?

            cursor_img_rect.center = pygame.mouse.get_pos()
            WIN.blit(cursor_img, cursor_img_rect)
            if player.get_health() <= 0:
                screen = "Lose"

        case "Start":
            print("Start screen!")
            screen = "Game"
            # Todo: add start screen

        case "Lose":
            print("Lose screen!")
            screen = "Reset"
            # Todo: add start screen

        case "Reset":
            enemies = pygame.sprite.Group()
            projectiles = pygame.sprite.Group()
            player = Player((width / 3, height / 2), TILE_SIZE)
            mouse_pressed = 0
            health = HealthBar(WIN, player, TILE_SIZE)
            bone_bar = BoneCounter(WIN, player, TILE_SIZE)
            screen = "Start"

        case other:
            print("Invalid state, return to start screen!")
            screen = "Start"
        # End match case

    # test server sender
    if keys[constants.K_w] and time < pygame.time.get_ticks():
        server.sendMsg(str(pygame.time.get_ticks()))
        time = pygame.time.get_ticks() + 1000

    pygame.display.update()
    updateCount += 1
    if updateCount % 600 == 0:
        print("FPS:", int(FPS_CLOCK.get_fps()))
        updateCount = 1
    FPS_CLOCK.tick(120)
    # end while loop

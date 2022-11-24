import os
from random import choice, randint
import sys
from math import floor, sqrt, hypot
from numpy import power
import pygame.locals as c

# Modular Files
from Entities.necromancer import Necromancer
from Entities.reaper import Reaper
from Entities.wizard import Wizard
from Entities.knight import Knight
from Entities.minion import Minion
from Entities.hero import Hero
from Entities.priestess import Priestess
from vfx import VFX
from gui import *
from tiles import *
from RandomGen.roomGen import Room
from RandomGen.ladderGen import LadderRoom
from server import Server
from dirMods import getImages

import pygame
from pygame import constants
from pygame import mixer

pygame.init()
pygame.mixer.init(channels=10)

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

fontDir = join(dirname(dirname(__file__)), 'Game/', 'Toriko.ttf')
font = pygame.font.Font(fontDir, round(TILE_SIZE))

# Sound Effects (Not BGM)
dirSFX = join(dirname(dirname(__file__)), 'game/assets/SFX/Menu')
menu_hover = mixer.Sound(join(dirSFX, 'Hover.wav'))
menu_click = mixer.Sound(join(dirSFX, 'Click.wav'))
lose_sound = mixer.Sound(join(dirSFX, 'Lose.wav'))
start_BGM = join(dirSFX, 'Start_BGM.wav')
lose_BGM = join(dirSFX, 'Lose_BGM.wav')

dirSFX = join(dirname(dirname(__file__)), 'game/assets/SFX/Game/Player')
melee_attack = mixer.Sound(join(dirSFX, 'Melee_Attack.wav'))
ranged_attack = mixer.Sound(join(dirSFX, 'Ranged_Attack.wav'))
player_hurt = mixer.Sound(join(dirSFX, 'Hurt.wav'))
player_death = mixer.Sound(join(dirSFX, 'Death.wav'))

dirSFX = join(dirname(dirname(__file__)), 'game/assets/SFX/Game/Env')
spike_trap = mixer.Sound(join(dirSFX, 'Spike.wav'))
fire_trap = mixer.Sound(join(dirSFX, 'Fire.wav'))
game_BGM = join(dirSFX, 'Game_BGM.wav')

# Sound Settings Adjustment
audio_master = 0.50
audio_BGM = 0.50 * audio_master
audio_sfx = 0.50 * audio_master

def setVolume(audio_sfx):
    menu_hover.set_volume(audio_sfx)
    menu_click.set_volume(audio_sfx)
    lose_sound.set_volume(audio_sfx)
    melee_attack.set_volume(audio_sfx)
    ranged_attack.set_volume(audio_sfx)
    player_hurt.set_volume(audio_sfx)
    player_death.set_volume(audio_sfx)
    spike_trap.set_volume(audio_sfx)
    fire_trap.set_volume(audio_sfx)
    player.setVolume(audio_sfx)

# Preloading Some Longer Animations for Performance
heal_vfx = getImages(join(dirname(dirname(__file__)), f'game/assets/vfx/heal'), (TILE_SIZE, TILE_SIZE))
shield_vfx = getImages(join(dirname(dirname(__file__)), f'game/assets/vfx/shield'), (TILE_SIZE*4//3, TILE_SIZE*4//3))
speed_vfx = getImages(join(dirname(dirname(__file__)), f'game/assets/vfx/speed'), (TILE_SIZE, TILE_SIZE))
blood_vfx = getImages(join(dirname(dirname(__file__)), f'game/assets/vfx/blood'), (TILE_SIZE, TILE_SIZE))
enemy_spawn_vfx = getImages(join(dirname(dirname(__file__)), f'game/assets/vfx/enemy_spawn'), (TILE_SIZE*2, TILE_SIZE*2))
minion_spawn_vfx = getImages(join(dirname(dirname(__file__)), f'game/assets/vfx/minion_spawn'), (TILE_SIZE, TILE_SIZE))
projectile_hit_vfx = getImages(join(dirname(dirname(__file__)), f'game/assets/vfx/projectile_hit'), (TILE_SIZE*3, TILE_SIZE*3))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Done-geon")
pygame.mouse.set_visible(False)
cursor_img = pygame.transform.scale(pygame.image.load(
    join(dirname(dirname(__file__)), 'game/assets', 'Crosshair02.png')), (28, 28))
cursor_img_rect = cursor_img.get_rect()

print("Created Window")


def scale_image(image):
    return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))


# temporary, to be modularized later:
STONE_TILE = scale_image(pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets', 'TileAsset32x32.png'))
                         .convert())

# to explain what this does, we define the stone tile sprite from the os' current directory/assets/TileAsset...,
# convert it to usable pygame image object, then load scale it to the biggest factor of 32x32 we can fit in the screen
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
minions = pygame.sprite.Group()
bosses = pygame.sprite.Group()
playerVFX = pygame.sprite.Group()
staticVFX = pygame.sprite.Group()
playerType = 'Necromancer'
mouse_pressed = 0
mouse_right_pressed = 0
key_shift_pressed = 0
key_e_pressed = 0
minion_cooldown = pygame.time.get_ticks() + 720
# server test variables
time = 0
roomIndex = 0

def clearTempContents():
    directory = join(dirname(__file__), 'assets/tiles/temprooms/')
    retain = ['.gitignore']
    for file in os.listdir(directory):
        if file not in retain:
            os.remove(join(directory, file))


updateCount = 0
screen = "Start"  # can be "Start", "Game", "Pause", maybe lose/win?


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
    if player_ent.fall:
        player_ent.dx = 0
        player_ent.dy = player_ent.speed
    if player_ent.dx == 0 and player_ent.dy == 0:
        player_ent.moving = False
    else:
        player_ent.moving = True


def move_calc_player(ent):
    dx = ent.dx
    dy = ent.dy
    if ent.speed == 0:
        ent.dx = 0
        ent.dy = 0
    elif abs(dx) == ent.speed and abs(dy) == ent.speed:
        ent.dx = (dx / abs(dx)) * ent.speed / sqrt(2)
        ent.dy = (dy / abs(dy)) * ent.speed / sqrt(2)


# uses y, x coords
room_collision_maps = []


def get_tile_at(x, y, ent):
    global roomIndex
    global room
    global screen
    global player
    x = x - TILE_SIZE / 2
    y = y - TILE_SIZE / 2
    tile_x = round(x / TILE_SIZE)
    tile_y = round(y / TILE_SIZE)
    if tile_x < 0 or tile_x > 15:
        return True

    if ladder_maps[roomIndex][tile_y][tile_x] == "9" and isinstance(ent, Player):
        if(roomIndex < roomListLength):
            room = ladderList[roomIndex]
            roomIndex += roomListLength
            player.rect.center = (WIDTH / 2, HEIGHT / 2)
        return False

    elif ladder_maps[roomIndex][tile_y][tile_x] == "73" and isinstance(ent, Player):
        if(roomIndex >= roomListLength):
            roomIndex -= roomListLength
            room = roomList[roomIndex]
            tile = room.__getTileMap__(3).getLadder()
            player.rect.center = (tile.rect.x + (TILE_SIZE / 2), tile.rect.y + TILE_SIZE + (TILE_SIZE / 3))
        return False

    elif room_collision_maps[roomIndex][tile_y][tile_x] == "-1":
        return False
    
    elif room_collision_maps[roomIndex][tile_y][tile_x] == "71" and isinstance(ent, Player):
        roomIndex -= 1
        if(roomIndex < 0):
            roomIndex = len(roomList) - 1
        room = roomList[roomIndex]
        tile = room.__getTileMap__(2).getExit()
        player.rect.center = (tile.rect.x + (TILE_SIZE / 2), tile.rect.y + TILE_SIZE + (TILE_SIZE / 3))

        #screen = "Transition"
        return False

    elif room_collision_maps[roomIndex][tile_y][tile_x] == "72" and isinstance(ent, Player):
        roomIndex += 1
        if(roomIndex >= len(roomList)):
            roomIndex = 0
        room = roomList[roomIndex]
        tile = room.__getTileMap__(2).getEntrance()
        player.rect.center = (tile.rect.x + (TILE_SIZE / 2), tile.rect.y - (TILE_SIZE / 2))

        #screen = "Transition"
        return False

    else:
        return True



def detect_collision(ent):
    if ent.collidable:
        if ent.dx > 0:  # check if tile ent would end up in is collidable, if so reduce d to 0
            if get_tile_at(ent.rect.right + ent.dx, ent.rect.centery, ent):
                ent.dx = 0
        elif ent.dx < 0:
            if get_tile_at(ent.rect.left + ent.dx, ent.rect.centery, ent):
                ent.dx = 0
        if ent.dy < 0:  # Down and up are backwards bc window is drawn top to bottom...
            if get_tile_at(ent.rect.centerx, ent.rect.top + ent.dy, ent):
                ent.dy = 0
        elif ent.dy > 0:
            if get_tile_at(ent.rect.centerx, ent.rect.bottom + ent.dy, ent):
                ent.dy = 0
    else:
        print("ent is non-collidable! This is probably an error!")

def detect_projectile_collision(p):
    if p.dx > 0:  # check if tile ent would end up in is collidable, if so reduce d to 0
        if get_tile_at(p.rect.right + p.dx, p.rect.centery, p):
            p.kill()
    elif p.dx < 0:
        if get_tile_at(p.rect.left + p.dx, p.rect.centery, p):
            p.kill()
    if p.dy < 0:  # Down and up are backwards bc window is drawn top to bottom...
        if get_tile_at(p.rect.centerx, p.rect.top + p.dy, p):
            p.kill()
    elif p.dy > 0:
        if get_tile_at(p.rect.centerx, p.rect.bottom + p.dy, p):
            p.kill()

def move_calc_enemy(ent):
    player_x = ent.player.rect.centerx
    player_y = ent.player.rect.centery
    if ent.speed == 0 or ent.canMove == False:
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
            diff_x_scaled = diff_x / sqrt(pow(diff_x, 2) + pow(diff_y, 2))
            diff_y_scaled = diff_y / sqrt(pow(diff_x, 2) + pow(diff_y, 2))
            diff_x_scaled *= ent.speed
            diff_y_scaled *= ent.speed
            ent.dx = diff_x_scaled
            ent.dy = diff_y_scaled

    diff_x = player_x - ent.rect.centerx

    if ent.dx < 0 or diff_x < 0:
        ent.flippedImage = True
    else:
        ent.flippedImage = False


room_fall_maps = []


def move_entities():
    global roomIndex
    global room
    move_calc_player(player)
    detect_collision(player)
    player.rect.center = (player.rect.centerx + player.dx, player.rect.centery + player.dy)
    player.tile_x = round((player.rect.centerx - TILE_SIZE / 2) / TILE_SIZE)
    player.tile_y = round((player.rect.bottom - TILE_SIZE / 2) / TILE_SIZE)
    player.tile = room_fall_maps[roomIndex][player.tile_y][player.tile_x]
    tile1 = ladder_maps[roomIndex][player.tile_y][player.tile_x]
    if player.tile == "-1" and player.fall == 0 and player.speed <= 5 and tile1 != "9" and player.iframes <= 0:  # for holes
        player.fall = 10
        player.get_hit(1)
        player.iframes = 10
    for b in bosses:
        move_calc_enemy(b)
        detect_collision(b)
        x = b.image_rect.centerx + b.dx
        y = b.image_rect.centery + b.dy
        b.image_rect.center = (x, y)
        b.rect.midbottom = b.image_rect.midbottom
    for e in enemies:
        if e.canMove:
            move_calc_enemy(e)
        detect_collision(e)
        e.x = e.rect.centerx + e.dx
        e.y = e.rect.centery + e.dy
        e.rect.center = (e.x, e.y)
    for m in minions:
        if m.canMove:
            move_calc_enemy(m)
        detect_collision(m)
        m.x = m.rect.centerx + m.dx
        m.y = m.rect.centery + m.dy
        m.rect.center = (m.x, m.y)
    for p in projectiles:
        p.x += p.dx
        p.y += p.dy
        p.rect.center = (int(p.x), int(p.y))
        detect_projectile_collision(p)

def detect_projectile(p):
    if p.type:  # true for friendly
        for e in enemies:
            if e.rect.collidepoint(p.rect.center):
                staticVFX.add(VFX('Projectile_Hit', (TILE_SIZE, TILE_SIZE), e.rect.center, True, projectile_hit_vfx))
                p.kill()
                e.health -= p.damage * 4
                if e.health <= 0:
                    e.kill()
                    player.bones += 1
    else:
        for m in minions:
            if m.rect.collidepoint(p.rect.center):
                p.kill()
                m.get_hit(p.damage)
                staticVFX.add(VFX('Blood', (TILE_SIZE, TILE_SIZE), m.rect.center, True, blood_vfx))
                if m.current_health <= 0:
                    m.kill()
        if player.rect.collidepoint(p.rect.center):
            p.kill()
            if not player.immune:
                staticVFX.add(VFX('Blood', (TILE_SIZE, TILE_SIZE), player.rect.center, True, blood_vfx))
                player.get_hit(p.damage)

def detect_melee(e):
    for m in minions:
        if m.rect.collidepoint(e.rect.center):
            m.get_hit(e.damage)
            staticVFX.add(VFX('Blood', (TILE_SIZE, TILE_SIZE), m.rect.center, True, blood_vfx))
            if 'Melee' in m.type:
                e.kill()
            if m.current_health <= 0:
                m.kill()
    if player.rect.collidepoint(e.rect.center):
        if not player.immune and not player.iframes:
            playerVFX.add(VFX('Blood', (TILE_SIZE, TILE_SIZE), player.rect.center, True, blood_vfx))
            player.get_hit(e.damage)

def detect_player_melee():
    if pygame.time.get_ticks() >= player.canAttack:
        mixer.Sound.play(melee_attack)
        
        for e in enemies:
            attackPosition = player.rect.center
            attackRadius = 2 * hypot(attackPosition[0] - player.rect.bottomright[0], attackPosition[1] - player.rect.bottomright[1])
            distance = hypot(attackPosition[0] - e.rect.centerx, attackPosition[1] - e.rect.centery)
            player.canAttack = pygame.time.get_ticks() + 480 # make sure this matches the canAttack in reaper

            direction = attackPosition[0] - e.rect.centerx
            if player.flippedImage:
                if distance <= attackRadius and direction >= 0:
                    staticVFX.add(VFX('Blood', (TILE_SIZE, TILE_SIZE), e.rect.center, True, blood_vfx))
                    e.kill()
                    player.bones += 1
            else:
                if distance <= attackRadius and direction <= 0:
                    staticVFX.add(VFX('Blood', (TILE_SIZE, TILE_SIZE), e.rect.center, True, blood_vfx))
                    e.kill()
                    player.bones += 1

def detect_boss_melee(b):
    if b.__inRange__(player) and b.currentSprites is b.meleeSprites:
        if not player.immune and not player.iframes and b.current_sprite >= 3:
            print('hit')
            player.get_hit(b.damage)

    for m in minions:
        if b.__inRange__(m) and b.currentSprites is b.meleeSprites:
            m.get_hit(b.damage)


def detect_item(p):
    if player.rect.collidepoint(p.rect.center):
        player.get_powerup(p.ability)
        server.sendMsg("p " + p.ability)
        p.kill()

def detect_trap(t):
    t.update()

    if t.cooldown <= 0:
        killed = False
        for e in enemies:
            if e.rect.colliderect(t.hitbox):
                t.activate = True
                t.cooldown = 10
                e.kill()
                killed = True
        
        if killed:
            match t.type:
                case 'Spike':
                    mixer.Sound.play(spike_trap)
                case 'Fire':
                    mixer.Sound.play(fire_trap)

def addVFX(type):
    match type:
        case 'Empty':
            return
        case 'Heal':
            playerVFX.add(VFX(type, (TILE_SIZE, TILE_SIZE), player.rect.center, True, heal_vfx))
        case 'Speed':
            playerVFX.add(VFX(type, (TILE_SIZE, TILE_SIZE), player.rect.center, sprites=speed_vfx))
        case 'Shield':
            playerVFX.add(VFX(type, (TILE_SIZE, TILE_SIZE), player.rect.center, sprites=shield_vfx))

roomList = []
ladderList = []
ladder_maps = []
roomListLength = randint(3, 6)
for index, iter in enumerate(range(roomListLength)):
    room = Room(index, NUM_TILES_X, NUM_TILES_Y, TILE_SIZE, roomListLength - 1)
    roomList.append(room)
    ladderRoom = LadderRoom(index, TILE_SIZE)
    ladderList.append(ladderRoom)
    ladder_maps.append(room.getMap(index, 3))
    room_collision_maps.append(room.getMap(index, 2))
    room_fall_maps.append(room.getMap(index, 1))

for index, iter in enumerate(range(roomListLength)):
    room = ladderList[index]
    ladder_maps.append(room.getMap(index, 3))
    room_collision_maps.append(room.getMap(index, 2))
    room_fall_maps.append(room.getMap(index, 1))

roomIndex = 0
room = roomList[roomIndex]

def random_spawn(): 
    validCoord = choice(room.validTiles)
    y = validCoord[0] * TILE_SIZE + TILE_SIZE // 2
    x = validCoord[1] * TILE_SIZE + TILE_SIZE // 2
    return (x, y)

match playerType:
    case 'Necromancer':
        print('Created Necromancer')
        player = Necromancer(random_spawn(), TILE_SIZE)
    case 'Reaper':
        print('Created Reaper')
        player = Reaper(random_spawn(), TILE_SIZE)

health = HealthBar(WIN, player, TILE_SIZE)
bone_bar = BoneCounter(WIN, player, TILE_SIZE)
inventory = Inventory(WIN, TILE_SIZE)
server = Server(player)

setVolume(audio_sfx)

minionType = 'Random'

def spawnMinion():
    player.bones -= 3
    # add something to specify melee vs. ranged, but for now it's random
    minionList = ['Melee_Corpse_Zombie', 'Melee_Sand_Zombie', 'Melee_Skeleton_Knight', 'Ranged_Sand_Archer', 'Ranged_Witch']
    spawn_coord = random_spawn()
    if minionType == 'Random':
        spawned_minion = Minion(spawn_coord,TILE_SIZE, player, choice(minionList))
    else:
        spawned_minion = Minion(spawn_coord,TILE_SIZE, player, minionType)
    minions.add(spawned_minion)
    staticVFX.add(VFX('Minion_Spawn', (TILE_SIZE, TILE_SIZE), spawned_minion.rect.center, True, minion_spawn_vfx))

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
            if event.key == constants.K_q:
                server.sendMsg("u " + player.powerup)
                addVFX(player.powerup)
                player.use_powerup()
            elif event.key == constants.K_RSHIFT or event.key == constants.K_LSHIFT:
                key_shift_pressed = 1
            elif event.key == constants.K_e:
                key_e_pressed = 1
            elif event.key == constants.K_UP and audio_master <= 0.95:
                audio_master += 0.05
                audio_BGM *= audio_master
                audio_sfx *= audio_master
                setVolume(audio_sfx)
                player.setVolume(audio_sfx)
                print('Increase Volume')
            elif event.key == constants.K_DOWN and audio_master >= 0.05:
                audio_master -= 0.05
                audio_BGM *= audio_master
                audio_sfx *= audio_master
                setVolume(audio_sfx)
                player.setVolume(audio_sfx)
                print('Decrease Volume')
        if event.type == constants.KEYUP:
            if event.key == constants.K_RSHIFT or event.key == constants.K_LSHIFT:
                key_shift_pressed = 0
            elif event.key == constants.K_e:
                key_e_pressed = 0

    # Remove old sprites to not hog resources; trust me, this got ugly on my old PC
    WIN.fill(0)
    keys = pygame.key.get_pressed()
    

    match screen:
        case "Game":
            #print("Game!")
            if player.fall == 1:
                enemies = pygame.sprite.Group()
                projectiles = pygame.sprite.Group()
                #roomIndex += 1
                #if roomIndex >= len(roomList):
                    #roomIndex = 0
                #room = roomList[roomIndex]
            room.drawRoom(WIN)

            # hitbox = (player.rect.topleft[0], player.rect.topleft[1], player.rect.width, player.rect.height) # NEW
            # pygame.draw.rect(WIN, (255,0,0), hitbox,2)

            # Update Functions
            enemy_choice = ['Wizard', 'Knight']
            if len(enemies) < 1:
                if(room.wave1):
                    bosses.add(Hero((WIDTH//2, HEIGHT//2), player, TILE_SIZE))
                    for i in range(round(player.bones / 4 + 1)):
                        spawn_coord = random_spawn()
                        match choice(enemy_choice):
                            #set bool to true to make boss
                            case 'Wizard':
                                spawned_enemy = Wizard(spawn_coord, player, TILE_SIZE,False)
                            case 'Knight':
                                spawned_enemy = Knight(spawn_coord, player, TILE_SIZE,False)
                        enemies.add(spawned_enemy)
                        staticVFX.add(VFX('Enemy_Spawn', (TILE_SIZE, TILE_SIZE), spawned_enemy.rect.midtop, True, enemy_spawn_vfx))
                    room.wave1 = False
                elif(room.wave2):
                    bosses.add(Priestess((WIDTH//2, HEIGHT//2), player, TILE_SIZE))
                    for i in range(round(player.bones / 4 + 1)):
                        spawn_coord = random_spawn()
                        match choice(enemy_choice):
                            #set bool to true to make boss
                            case 'Wizard':
                                spawned_enemy = Wizard(spawn_coord, player, TILE_SIZE,False)
                            case 'Knight':
                                spawned_enemy = Knight(spawn_coord, player, TILE_SIZE,False)
                        enemies.add(spawned_enemy)
                        staticVFX.add(VFX('Enemy_Spawn', (TILE_SIZE, TILE_SIZE), spawned_enemy.rect.midtop, True, enemy_spawn_vfx))
                    room.wave2 = False
                elif(room.locked):
                    room.unlock()
                    room_collision_maps[roomIndex] = room.getMap(roomIndex, 2)
                    #room.drawRoom(WIN)
            for m in minions:
                WIN.blit(m.image, m.rect)
                m.update(projectiles, enemies)
            for e in enemies:
                WIN.blit(e.image, e.rect)
                e.update(projectiles)
            for p in projectiles:
                WIN.blit(p.image, p.rect)
                p.update()
            for b in bosses:
                #pygame.draw.rect(WIN, (0,0,0), b.rect) # HITBOX
                #pygame.draw.circle(WIN, (240,248,255), b.attackPosition, b.attackRadius) # ATTACK HITBOX
                WIN.blit(b.image, b.image_rect)
                b.update(projectiles)
            get_player_move(player, keys)
            move_entities()
            for p in projectiles:
                detect_projectile(p)
            for e in enemies:
                if e.__class__ == Knight:  # TODO: change to be in the melee function, shouldn't be exclusive to knights
                    detect_melee(e)
            for p in room.powerups:
                detect_item(p)
            for t in room.traps:
                detect_trap(t)
            for b in bosses:
                detect_boss_melee(b)
            player.update()
            if mouse_pressed:
                player.attacking = True
                match playerType:
                    case 'Necromancer':
                        if pygame.time.get_ticks() >= player.canAttack:
                            mixer.Sound.play(ranged_attack)
                            player.attack(projectiles)
                    case 'Reaper':
                        detect_player_melee()
            if key_shift_pressed:
                player.sprint()
            if key_e_pressed:
                if player.bones >= 3 and pygame.time.get_ticks() >= minion_cooldown:  # selected_minion.cost
                    minion_cooldown = pygame.time.get_ticks() + 720
                    spawnMinion()
                    
            if player.fall:
                player.fall -= 1
            WIN.blit(player.image, player.rect)
            for v in playerVFX:
                if v.one_time:
                    v.update(player.rect.center)
                    if v.done:
                        v.kill()
                    else:
                        WIN.blit(v.image, v.rect)
                if player.powerupTimer > 0 and not v.one_time:
                    WIN.blit(v.image, v.rect)
                    v.update(player.rect.center)
                elif player.powerupTimer <= 0 and not v.one_time:
                    v.kill()
            for v in staticVFX:
                if v.done:
                    v.kill()
                else:
                    WIN.blit(v.image, v.rect)
                    if v.type in ['Enemy_Spawn', 'Minion_Spawn']:
                        speedVal = 0.15
                    else:
                        speedVal = 1
                    v.update(speed=speedVal)
            health.update(WIN, player)
            bone_bar.update(WIN, player)
            inventory.update(WIN, player)

            pygame.mouse.set_visible(False)
            cursor_img_rect.center = pygame.mouse.get_pos()
            WIN.blit(cursor_img, cursor_img_rect)
            if player.get_health() <= 0:
                server.sendMsg("lose")
                screen = "Lose"
                mixer.stop()
                mixer.music.stop()

        case "Start":
            print("Start screen!")
            WIN.fill(pygame.color.Color(0))
            color = pygame.color.Color(255, 255, 255)
            neon_yellow_color = pygame.color.Color(224, 231, 34)
            title_text = font.render('Done-geon', True, color, pygame.SRCALPHA)
            start_text = font.render('Click Here To Start!', True, color, pygame.SRCALPHA)
            button_rect = start_text.get_rect()
            button_rect[0] = width / 6
            button_rect[1] = height / 2
            run = True
            hovered = False
            mixer.music.load(start_BGM)
            mixer.music.set_volume(audio_BGM)
            mixer.music.play(-1)
            start_text_yellow = False
            while run:
                WIN.fill(pygame.color.Color(0))
                # WIN.fill(0)
                if start_text_yellow:
                    start_text = font.render('Click Here To Start!', True, neon_yellow_color, pygame.SRCALPHA)
                else:
                    start_text = font.render('Click Here To Start!', True, color, pygame.SRCALPHA)
                WIN.blit(title_text, (width / 6, height / 3))
                WIN.blit(start_text, (width / 6, height / 2))
                pygame.mouse.set_visible(True)
                for event in pygame.event.get():
                    mouse = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse):
                        start_text_yellow = True
                        if not hovered:
                            hovered = True
                            mixer.Sound.play(menu_hover)
                    else:
                        start_text_yellow = False
                        hovered = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        server.endServer()
                        clearTempContents()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if button_rect.collidepoint(mouse):
                            mixer.Sound.play(menu_click)
                            screen = "Reset"
                            run = False
                pygame.display.update()
            mixer.stop()
            mixer.music.stop()

        case "Lose":
            print("Lose screen!")
            color = pygame.color.Color(255, 255, 255)
            neon_yellow_color = pygame.color.Color(224, 231, 34)
            title_text = font.render('Game Over!', True, color, pygame.SRCALPHA)
            start_text = font.render('Click Here To Return To Menu!', True, color, pygame.SRCALPHA)
            game_text = font.render('Click Here To Play Again!', True, color, pygame.SRCALPHA)
            button_rect = start_text.get_rect()
            button_rect[0] = width / 6
            button_rect[1] = height / 2
            button_rect_2 = game_text.get_rect()
            button_rect_2[0] = width / 6
            button_rect_2[1] = height / 2.5
            run = True
            startHovered = False
            playHovered = False
            mixer.Sound.play(player_death)
            mixer.Sound.play(lose_sound)
            mixer.music.load(lose_BGM)
            mixer.music.set_volume(audio_BGM)
            mixer.music.play(-1)
            while run:
                WIN.fill(0)
                WIN.blit(title_text, (width / 6, height / 3.5))
                WIN.blit(start_text, (width / 6, height / 2))
                WIN.blit(game_text, (width / 6, height / 2.5))
                pygame.mouse.set_visible(True)
                for event in pygame.event.get():
                    mouse = pygame.mouse.get_pos()
                    if button_rect.collidepoint(mouse):
                        start_text = font.render('Click Here To Return To Menu!', True, neon_yellow_color, pygame.SRCALPHA)
                        if not startHovered:
                            startHovered = True
                            mixer.Sound.play(menu_hover)
                    else:
                        start_text = font.render('Click Here To Return To Menu!', True, color, pygame.SRCALPHA)
                        startHovered = False
                    if button_rect_2.collidepoint(mouse):
                        game_text = font.render('Click Here To Play Again!', True, neon_yellow_color, pygame.SRCALPHA)
                        if not playHovered:
                            playHovered = True
                            mixer.Sound.play(menu_hover)
                    else:
                        game_text = font.render('Click Here To Play Again!', True, color, pygame.SRCALPHA)
                        playHovered = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        server.endServer()
                        clearTempContents()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if button_rect.collidepoint(mouse):
                            mixer.Sound.play(menu_click)
                            mixer.music.stop()
                            screen = "Start"
                            run = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if button_rect_2.collidepoint(mouse):
                            mixer.Sound.play(menu_click)
                            mixer.music.stop()
                            screen = "Reset"
                            run = False
                pygame.display.update()
            mixer.stop()
            mixer.music.stop()

        case "Reset":
            enemies = pygame.sprite.Group()
            projectiles = pygame.sprite.Group()
            minions = pygame.sprite.Group()
            match playerType:
                case 'Necromancer':
                    print('Created Necromancer')
                    player = Necromancer(random_spawn(), TILE_SIZE)
                case 'Reaper':
                    print('Created Reaper')
                    player = Reaper(random_spawn(), TILE_SIZE)
            mouse_pressed = 0
            health = HealthBar(WIN, player, TILE_SIZE)
            bone_bar = BoneCounter(WIN, player, TILE_SIZE)
            screen = "Game"

        #case "Transition":
            #WIN.fill(0)
            #pygame.time.delay(3000)
            #screen = "Game"

        case other:
            print("Invalid state, return to start screen!")
            screen = "Start"
        # End match case

    # test server sender
    if time < pygame.time.get_ticks():
        server.sendMsg("h " + str(player.get_health()))
        server.sendMsg("b " + str(player.bones))
        time = pygame.time.get_ticks() + 500

    if server.newPowerup:
        server.newPowerup = False
        addVFX(server.powerup)
        player.use_powerup(server.powerup)
    if server.newPlayer:
        server.newPlayer = False
        playerType = server.playerType
        match playerType:
            case 'Necromancer':
                player = Necromancer(random_spawn(), TILE_SIZE,player)
            case 'Reaper':
                player = Reaper(random_spawn(), TILE_SIZE,player)
        for m in minions:
            m.player = player
    if server.newMinion:
        server.newMinion = False
        minionType = server.minionType
        if(player.bones >= 3):
            minion_cooldown = pygame.time.get_ticks() + 720
            spawnMinion()
    if server.checkConnection() is False:
        minionType = 'Random'

    pygame.display.update()
    updateCount += 1
    if updateCount % 600 == 0:
        print("FPS:", int(FPS_CLOCK.get_fps()))
        updateCount = 1
    FPS_CLOCK.tick(120)
    # end while loop

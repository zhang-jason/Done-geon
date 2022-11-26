from os import listdir
from os.path import join, dirname, isfile
from Entities.entity import Entity
from Entities.projectile import Projectile
from math import sqrt
import pygame
import pygame.locals as c
from pygame import mixer

class Player(Entity):
    def __init__(self, startPosition, TILE_SIZE, player= None):
        super(Player, self).__init__()
        if(player is None):
            self.bones = 3
            self.powerup = 'empty'
            self.powerupTimer = 0
            self.immune = False
            self.tile_x = 0
            self.tile_y = 0
            self.tile = "-1"
            self.fall = 0
            self.current_health = 4
        else:
            self.bones = player.bones
            self.powerup = player.powerup
            self.powerupTimer = player.powerupTimer
            self.immune = player.immune
            self.tile_x = player.tile_x
            self.tile_y = player.tile_y
            self.tile = player.tile
            self.fall = player.fall
            self.current_health = player.current_health
            
        self.sprint_cooldown = 0
        self.sprint_sound = mixer.Sound(join(dirname(dirname(__file__)), 'assets/SFX/Game/Player', 'Sprint.wav'))
        self.hurt_sound = mixer.Sound(join(dirname(dirname(__file__)), 'assets/SFX/Game/Player', 'Hurt.wav'))
        self.powerup_loop = mixer.Sound(join(dirname(dirname(__file__)), 'assets/SFX/Game/Player', 'Powerup_Loop.wav'))
        self.powerup_one_time = mixer.Sound(join(dirname(dirname(__file__)), 'assets/SFX/Game/Player', 'Powerup_One_Time.wav'))
        self.powerupChannel = None
        self.TILE_SIZE = TILE_SIZE

        # how often the character can move (every five ticks)
        self.canMove = pygame.time.get_ticks() + 5
        self.attacking = False
        self.moving = False
        self.max_speed = 5           # 
        self.speed = self.max_speed  # how far it moves
        self.set_speed(self.speed)  # is this necessary? should test later... prior to sprint mechanics
        self.collidable = True
        self.max_health = 4
        self.iframes = 0
        self.alive = True

    def sprint(self):
        if self.sprint_cooldown <= 0:
            mixer.Sound.play(self.sprint_sound)
            self.speed = 20
            self.sprint_cooldown = 90
            self.iframes = 15

    def get_health(self):
        return self.current_health

    def get_hit(self, hitDmg):
        if (self.current_health - hitDmg) > 0:
            self.current_health -= hitDmg
            self.iframes = 120
            mixer.Sound.play(self.hurt_sound)
        else:
            self.current_health = 0
            self.alive = False

    def get_regen(self, regenAmt):
        if (regenAmt + self.current_health) < self.max_health:
            self.current_health += regenAmt
        else:
            self.current_health = self.max_health

    # Takes Powerup Object
    def get_powerup(self, powerup):
        if powerup.consumable:
            self.powerup = powerup.ability
        else:
            self.use_powerup(powerup.ability)

    # Takes Powerup Ability String
    def use_powerup(self,powerup= None):
        if powerup is None:
            powerup = self.powerup
        match powerup:
            case 'Speed':
                self.speed += 2
                self.powerupTimer = 1000
            case 'Heal':
                mixer.Sound.play(self.powerup_one_time)
                self.get_regen(1)
            case 'Shield':
                self.powerupTimer = 1000
                self.immune = True
            case 'Perm_Damage':
                self.damage += 2
            case 'Perm_Speed':
                self.max_speed += 1
                self.speed = self.max_speed
            case 'Full_Heal':
                self.get_regen(self.max_health)
            case 'Bones':
                self.bones += 10
            

        print(f'used {powerup}')
        self.powerup = 'empty'

    # def update(self, keys, group, tiles):
    def update(self):
        # Update Sprite Animation
        if self.current_sprite >= len(self.currentSprites):
            self.current_sprite = 0
            if self.attacking:
                self.attacking = False
        self.image = self.currentSprites[int(self.current_sprite)]

        if self.flippedImage:
            self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], True, False)
        else:
            self.image = pygame.transform.flip(self.currentSprites[int(self.current_sprite)], False, False)
        if self.iframes:
            self.iframes -= 1
        if self.sprint_cooldown:
            self.sprint_cooldown -= 1
            if self.speed > self.max_speed:
                self.speed -= 1

        if self.powerupTimer > 0:
            if self.powerupChannel is None:
                self.powerupChannel = mixer.find_channel()
                self.powerupChannel.play(self.powerup_loop, -1)
            self.powerupTimer -= 1
            if self.powerupTimer == 0:
                self.powerupChannel.stop()
                self.powerupChannel = None
                self.speed = self.max_speed
                self.immune = False

    # Reset char after dying; doesn't work quite yet
    def reset(self):
        self.current_health = 4
        self.alive = True

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

    def setVolume(self, audio_sfx):
        self.sprint_sound.set_volume(audio_sfx)
        self.hurt_sound.set_volume(audio_sfx)
        self.powerup_loop.set_volume(audio_sfx)
        self.powerup_one_time.set_volume(audio_sfx)
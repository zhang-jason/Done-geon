import os
import csv
import pygame
from random import randint, choice

from tiles import TileMap
from Entities.powerup import Powerup

class LadderRoom():
    def __init__(self, roomIndex, tileSize, type):
        self.type = type
        self.room = self.genRoom(roomIndex, tileSize)
        self.traps = []
        self.wave1 = False
        self.wave2 = False
        self.locked = False
        self.animation = False
        self.validTiles = self.findValidTiles(roomIndex)
        self.powerups = pygame.sprite.Group()
        self.genPowerups(tileSize)
        self.type = type

    def genRoom(self, roomIndex, tileSize):
        room = []
        floor_map = [[-1 for x in range(16)] for y in range(9)]
        wall_map = [[-1 for x in range(16)] for y in range(9)]
        third_map = [[-1 for x in range(16)] for y in range(9)]

        for i in range(5, 11):
            for j in range(2, 7):
                floor_map[j][i] = 1
        
        for i in range(5, 11):
            j = 1
            wall_map[j][i] = 14
            j = 7
            wall_map[j][i] = 13
        for j in range(0, 9):
            for i in range(0, 5):
                wall_map[j][i] = 42
            for i in range(11, 16):
                wall_map[j][i] = 42

        j = 0
        for i in range(5, 11):
            wall_map[j][i] = 42
        j = 8
        for i in range(5, 11):
            wall_map[j][i] = 42
        
        third_map[1][5] = 30 #top left L corner
        third_map[6][5] = 28 #bottom left L corner
        third_map[1][10] = 31 #top right L corner
        third_map[6][10] = 20 #bottom right L corner
        for j in range(2, 6):
            i = 5
            third_map[j][i] = 18 #left wall
            i = 10
            third_map[j][i] = 17 #right wall

        for i in range(6, 10):
            j = 1
            third_map[j][i] = 16 #top wall
            j = 6
            third_map[j][i] = 15 #bottom wall
        
        third_map[2][6] = 73 #ladder

        
        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'ladder_room{roomIndex}_1.csv'),
                  'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(floor_map)

            file.close()
        
        room.append(self.__getTileMap__(1, roomIndex, tileSize))

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'ladder_room{roomIndex}_2.csv'),
                  'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(wall_map)

            file.close()

        room.append(self.__getTileMap__(2, roomIndex, tileSize))

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'ladder_room{roomIndex}_3.csv'),
                  'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(third_map)

            file.close()

        room.append(self.__getTileMap__(3, roomIndex, tileSize))

        return room

    def drawRoom(self, WIN):
        self.room[0].draw_map(WIN)
        self.room[1].draw_map(WIN)
        self.powerups.draw(WIN)
        self.room[2].draw_map(WIN)

    def getMap(self, roomIndex, layerIndex):
        map = []
        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms',
                               f'ladder_room{roomIndex}_{layerIndex}.csv')) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def findValidTiles(self, roomIndex):
        collide = self.getMap(roomIndex, 2)
        noncollide = self.getMap(roomIndex, 3)
        specialHoles = ['9','10','11']
        validTiles = []

        for i in range(len(collide)):
            for j in range(len(collide[0])):
                if collide[i][j] == '-1' and noncollide[i][j] not in specialHoles:
                    validTiles.append((i, j))

        return validTiles

    def genPowerups(self, tileSize):
        currPowerups = 0
        maxPowerups = randint(2,4)
        powerupType = ['Bones', 'Perm_Dmg', 'Perm_Speed', 'Full_Heal']

        while currPowerups < maxPowerups:
            validCoord = choice(self.validTiles)
            self.validTiles.remove(validCoord)
            y = validCoord[0] * tileSize + tileSize // 2
            x = validCoord[1] * tileSize + tileSize // 2
            powerupChoice = choice(powerupType)
            powerupType.remove(powerupChoice)
            self.powerups.add(Powerup((x, y), powerupChoice, tileSize, False))
            currPowerups += 1

    def __getTileMap__(self, layerIndex, roomIndex, tileSize):
        filename = os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms',
                                f'ladder_room{roomIndex}_{layerIndex}.csv')
        return TileMap(filename, tileSize, self.type)
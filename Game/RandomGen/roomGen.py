import os
import csv
from random import randint, choice

import pygame

from RandomGen.floorGen import FloorGen
from RandomGen.wallGen import WallGen
from RandomGen.collideGen import CollideGen
from tiles import TileMap
from Entities.powerup import Powerup
from Entities.traps import Trap


class Room():
    def __init__(self, roomIndex, width, height, tileSize, numRooms):
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.roomIndex = roomIndex
        self.room = self.genMap(numRooms)
        self.validTiles = self.findValidTiles()
        self.powerups = pygame.sprite.Group()
        self.genPowerups()
        self.traps = pygame.sprite.Group()
        self.genTraps()
        self.wave1 = True
        self.wave2 = True
        self.locked = True
        self.animation = True

    def getMap(self, roomIndex, layerIndex):
        map = []
        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms',
                               f'room{roomIndex}_{layerIndex}.csv')) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def drawRoom(self, WIN):
        self.room[0].draw_map(WIN)
        self.room[1].draw_map(WIN)
        self.traps.draw(WIN)
        self.powerups.draw(WIN)
        self.room[2].draw_map(WIN)

    def genMap(self, num):
        room = []

        FloorGen(self.roomIndex, self.width, self.height)
        room.append(self.__getTileMap__(1))

        floorMap = self.getMap(self.roomIndex, 1)
        WallGen(floorMap, self.roomIndex, num)
        room.append(self.__getTileMap__(2))

        room.append(self.__getTileMap__(3))

        return room

    # Randomly generate powerups around the room
    def genPowerups(self):
        currPowerups = 0
        maxPowerups = randint(2,4)
        powerupType = ['Speed', 'Heal', 'Shield']

        while currPowerups < maxPowerups:
            validCoord = choice(self.validTiles)
            self.validTiles.remove(validCoord)
            y = validCoord[0] * self.tileSize + self.tileSize // 2
            x = validCoord[1] * self.tileSize + self.tileSize // 2
            self.powerups.add(Powerup((x, y), choice(powerupType), self.tileSize))
            currPowerups += 1

    def genTraps(self):
        currTraps = 0
        maxTraps = randint(2,4)
        trapType = ['Spike', 'Fire']

        while currTraps < maxTraps:
            validCoord = choice(self.validTiles)
            self.validTiles.remove(validCoord)
            y = validCoord[0] * self.tileSize
            x = validCoord[1] * self.tileSize
            self.traps.add(Trap((x, y), choice(trapType), self.tileSize))
            currTraps += 1

    # Returns a list of empty floor tiles (valid tiles to spawn entities)
    def findValidTiles(self):
        collide = self.getMap(self.roomIndex, 2)
        noncollide = self.getMap(self.roomIndex, 3)
        specialHoles = ['9','10','11']
        validTiles = []

        for i in range(len(collide)):
            for j in range(len(collide[0])):
                if collide[i][j] == '-1' and noncollide[i][j] not in specialHoles:
                    validTiles.append((i, j))

        return validTiles

    def unlock(self):
        collide = self.getMap(self.roomIndex, 2)
        for i in range(len(collide)):
            for j in range(len(collide[0])):
                if collide[i][j] == "70":
                    collide[i][j] = "72"
        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{self.roomIndex}_2.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(collide)

            file.close()
        self.room[1] = self.__getTileMap__(2)
        self.locked = False

    def __getTileMap__(self, layerIndex):
        filename = os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms',
                                f'room{self.roomIndex}_{layerIndex}.csv')
        return TileMap(filename, self.tileSize)

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
    def __init__(self, roomIndex, width, height, tileSize):
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.roomIndex = roomIndex
        self.room = self.genMap()
        self.holeList = self.findHoles()
        self.powerups = pygame.sprite.Group()
        self.genPowerups()
        self.traps = pygame.sprite.Group()
        self.genTraps()

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
        self.powerups.draw(WIN)
        self.traps.draw(WIN)
        self.room[2].draw_map(WIN)
        

    def genMap(self):
        room = []

        FloorGen(self.roomIndex, self.width, self.height)
        room.append(self.__getTileMap__(1))

        floorMap = self.getMap(self.roomIndex, 1)
        WallGen(floorMap, self.roomIndex)
        room.append(self.__getTileMap__(2))

        room.append(self.__getTileMap__(3))

        return room

    # Randomly generate powerups around the room
    def genPowerups(self):
        currPowerups = 0
        maxPowerups = randint(2,4)
        powerupType = ['Speed', 'Heal'] #add shield later

        while currPowerups < maxPowerups:
            validCoord = choice(self.holeList)
            y = validCoord[0] * self.tileSize + self.tileSize // 2
            x = validCoord[1] * self.tileSize + self.tileSize // 2
            self.powerups.add(Powerup((x, y), choice(powerupType), self.tileSize))
            currPowerups += 1

    def genTraps(self):
        currTraps = 0
        maxTraps = randint(2,4)
        trapType = ['Spikes']

        while currTraps < maxTraps:
            validCoord = choice(self.holeList)
            y = validCoord[0] * self.tileSize + self.tileSize // 2
            x = validCoord[1] * self.tileSize + self.tileSize // 2
            self.traps.add(Trap((x, y), choice(trapType), self.tileSize))
            currTraps += 1

    # Returns a list of empty floor tiles (valid tiles to spawn entities)
    def findHoles(self):
        collide = self.getMap(self.roomIndex, 2)
        noncollide = self.getMap(self.roomIndex, 3)
        specialHoles = ['9','10','11']
        holeList = []

        for i in range(len(collide)):
            for j in range(len(collide[0])):
                if collide[i][j] == '-1' and noncollide[i][j] not in specialHoles:
                    holeList.append((i, j))

        return holeList

    def __getTileMap__(self, layerIndex):
        filename = os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms',
                                f'room{self.roomIndex}_{layerIndex}.csv')
        return TileMap(filename, self.tileSize)

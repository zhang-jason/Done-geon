import os
import csv
from random import randint, choice

from RandomGen.floorGen import FloorGen
from RandomGen.wallGen import WallGen
from RandomGen.collideGen import CollideGen
from tiles import TileMap
from Entities.powerup import Powerup

class Room():
    def __init__(self, roomIndex, width, height, tileSize, powerups):
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.roomIndex = roomIndex
        self.room = self.genMap()
        self.powerups = self.genPowerups()

    def getMap(self, roomIndex, layerIndex):
        map = []
        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_{layerIndex}.csv')) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def drawRoom(self, WIN):
        for i in self.room:
            i.draw_map(WIN)

        for p in self.powerups:
            WIN.blit(p.image, p.rect)

    def genMap(self):
        room = []

        FloorGen(self.roomIndex, self.width, self.height)
        room.append(self.__getTileMap__(1))

        floorMap = self.getMap(self.roomIndex, 1)
        WallGen(floorMap, self.roomIndex)
        room.append(self.__getTileMap__(2))
        
        room.append(self.__getTileMap__(3))

        return room

    def genPowerups(self):
        currPowerups = 0
        maxPowerups = 3
        powerupType = ['heal', 'damage', 'shield']
        powerups = []

        map = self.getMap(self.roomIndex, 2)

        while currPowerups < maxPowerups:
            x = randint(2, len(map)-1)
            y = randint(2, len(map[0])-1)

            if map[x][y] == '-1':
                powerups.append(Powerup((x, y), choice(powerupType), self.tileSize))
                currPowerups += 1

        return powerups

    def __getTileMap__(self, layerIndex):
        filename = os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{self.roomIndex}_{layerIndex}.csv')
        return TileMap(filename, self.tileSize)
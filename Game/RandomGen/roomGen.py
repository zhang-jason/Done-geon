import os
import csv

from RandomGen.floorGen import FloorGen
from RandomGen.wallGen import WallGen
from tiles import TileMap

class Room():
    def __init__(self, roomIndex, width, height, tileSize):
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.roomIndex = roomIndex
        self.room = self.initMap()

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

    def initMap(self):
        room = []

        FloorGen(self.roomIndex, self.width, self.height)
        room.append(self.__getTileMap__(1))

        WallGen(self.getMap(self.roomIndex, 1), self.roomIndex)
        room.append(self.__getTileMap__(2))

        return room

    def __getTileMap__(self, layerIndex):
        filename = os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{self.roomIndex}_{layerIndex}.csv')
        return TileMap(filename, self.tileSize)
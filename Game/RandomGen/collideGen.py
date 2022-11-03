import csv
from math import floor
import os
from random import randint, choice

COLUMN = [[-1], [-1], [27]]
CHEST = [12]
POWERUP = [25]
CLUSTER_LIST = [COLUMN, CHEST, POWERUP]


class CollideGen():
    def __init__(self, floorMap, wallMap, roomIndex):
        self.floorMap = floorMap
        self.wallMap = wallMap
        self.roomIndex = roomIndex
        self.map = self.initMap(len(floorMap[0]), len(floorMap))
        self.genMap()

    def genFloors(self):
        holeLimit = 2
        holeCount = 0
        floorIDs = [9, 10, 11]

        # Generate special floor tiles
        for i in range(1, len(self.floorMap) - 1):
            for j in range(1, len(self.floorMap[i]) - 1):
                if self.__isHole__(i, j):
                    genID = choice(floorIDs)

                    if genID == 9:
                        floorIDs.remove(9)
                    elif genID == 10:
                        holeCount += 1

                    if holeCount == holeLimit:
                        floorIDs.remove(10)
                        holeCount += 1  # Can never enter this loop again

                    self.map[i][j] = genID

    def genObjects(self):
        return

    def genCluster(self):
        return

    def genMap(self):
        self.genFloors()
        self.genObjects()

        with open(
                os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{self.roomIndex}_3.csv'),
                'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.map)

            file.close()

    def initMap(self, width, height):
        map = [[-1 for x in range(width)] for y in range(height)]
        return map

    def __isHole__(self, i, j):
        if (self.floorMap[i][j] == '-1'):
            if (self.floorMap[i - 1][j] != '-1') and (self.floorMap[i + 1][j] != '-1') and (
                    self.floorMap[i][j - 1] != '-1') and (self.floorMap[i][j + 1] != '-1'):
                return True

        return False

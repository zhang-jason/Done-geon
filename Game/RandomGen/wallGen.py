import csv
from math import floor
import os
from random import randint

TOP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
TOP_RIGHT = 5
DOWN_RIGHT = 6
TOP_LEFT = 7
DOWN_LEFT = 8

class WallGen():
    def __init__(self, floorMap, roomIndex):

        self.genWalls(floorMap, roomIndex)

    def genWalls(self, floorMap, roomIndex):
        wallMap = []
        for i in range(1, len(floorMap)):
            for j in range(len(floorMap[0])):
                if floorMap[i][j] == 1:
                    adjacent = self.checkAdjacent(floorMap, wallMap, i, j)

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_2.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(wallMap)

            file.close()

    def checkAdjacent(self, floorMap, wallMap, i, j):
        empty = []


        if floorMap[i][j] == 4:
            return

        
        

import csv
import os
from random import randint
from copy import deepcopy


class FloorGen():
    def __init__(self, roomIndex, width, height):
        self.chance = 50  # Chance of generating a floor tile
        self.iterations = 3  # How many recursive calls
        self.minCount = 5  # Greater the number, less risk of islands (unless it's two large ones)
        self.minTiles = 70  # Minimum number of playable tiles allowed

        self.genMap(roomIndex, width, height)

    def genMap(self, roomIndex, width, height):
        satisfied = False

        while not satisfied:
            # Initialize list map and randomly populate it
            map = self.initMap(width, height)
            map = self.randomizeMap(map)

            for i in range(self.iterations):
                map = self.cellularAutomata(map)

            # Fill perimeter with preliminary empty pieces
            for i in range(len(map)):
                for j in range(len(map[i])):
                    if (i == 0) or (j == 0) or (i == len(map) - 1) or (j == len(map[0]) - 1):
                        map[i][j] = -1

            # Make sure the playable area is a certain number of tiles
            if sum(row.count(1) for row in map) > self.minTiles:
                print('Num Tiles: ' + str(sum(row.count(1) for row in map)))
                # Make sure there's not stray islands that the player can't get to
                if self.countIslands(map) == 1:
                    satisfied = True

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_1.csv'),
                  'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(map)

            file.close()

    def initMap(self, width, height):
        map = [[-1 for x in range(width)] for y in range(height)]
        return map

    def randomizeMap(self, map):
        for i in range(len(map)):
            for j in range(len(map[0])):
                if randint(0, 100) <= self.chance:
                    map[i][j] = self.__genRandomFloorID__()
        return map

    def cellularAutomata(self, map):
        map = [row[:] for row in map]
        for i in range(1, len(map) - 1):
            for j in range(1, len(map[0]) - 1):
                count = 0
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if map[i + k][j + l] == -1:
                            count += 1
                if count >= self.minCount or count == 0:
                    map[i][j] = -1
                else:
                    map[i][j] = self.__genRandomFloorID__()
        return map

    def countIslands(self, map):
        visited = deepcopy(map)
        numIslands = 0

        for i in range(len(map)):
            for j in range(len(map[0])):
                if visited[i][j] == 1:
                    numIslands += 1
                self.__checkAdjacent__(visited, i, j)

        return numIslands

    def __checkAdjacent__(self, visited, i, j):
        if (i < 0) or (j < 0) or (i >= len(visited)) or (j >= len(visited[0])):
            return
        if visited[i][j] == -1:
            return
        else:
            visited[i][j] = -1

        # Recursively check adjacent tiles (cross)
        self.__checkAdjacent__(visited, i + 1, j)
        self.__checkAdjacent__(visited, i, j + 1)
        self.__checkAdjacent__(visited, i - 1, j)
        self.__checkAdjacent__(visited, i, j - 1)

    def __genRandomFloorID__(self):
        if randint(0, 100) <= 90:
            return 1
        else:
            return randint(2, 8)

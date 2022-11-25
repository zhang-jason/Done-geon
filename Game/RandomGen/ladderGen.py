import os
import csv

from tiles import TileMap

class LadderRoom():
    def __init__(self, roomIndex, tileSize):
        self.room = self.genRoom(roomIndex, tileSize)
        self.powerups = []
        self.traps = []
        self.wave1 = False
        self.wave2 = False
        self.locked = False
        self.validTiles = self.findValidTiles(roomIndex)

    def genRoom(self, roomIndex, tileSize):
        room = []
        floor_map = [[-1 for x in range(16)] for y in range(9)]
        wall_map = [[-1 for x in range(16)] for y in range(9)]
        third_map = [[-1 for x in range(16)] for y in range(9)]

        for i in range(6, 10):
            for j in range(3, 6):
                floor_map[j][i] = 1
        
        for i in range(6, 10):
            j = 2
            wall_map[j][i] = 14
            j = 6
            wall_map[j][i] = 13
        for j in range(0, 9):
            for i in range(0, 6):
                wall_map[j][i] = 42
            for i in range(10, 16):
                wall_map[j][i] = 42
        
        third_map[2][6] = 30 #top left L corner
        third_map[5][6] = 28 #bottom left L corner
        third_map[2][9] = 31 #top right L corner
        third_map[5][9] = 20 #bottom right L corner
        for j in range(3, 5):
            i = 6
            third_map[j][i] = 18 #left wall
            i = 9
            third_map[j][i] = 17 #right wall

        for i in range(7, 9):
            j = 2
            third_map[j][i] = 16 #top wall
            j = 5
            third_map[j][i] = 15 #bottom wall
        
        third_map[3][7] = 73 #ladder

        
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

    def __getTileMap__(self, layerIndex, roomIndex, tileSize):
        filename = os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms',
                                f'ladder_room{roomIndex}_{layerIndex}.csv')
        return TileMap(filename, tileSize)
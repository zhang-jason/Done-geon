import csv
from math import floor
import os
from random import randint, choice

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
        self.floorMap = floorMap
        self.wallMap = []
        self.thirdLayer = []
        self.genMap(roomIndex)

    def initMap(self):
        self.wallMap = [[-1 for x in range(16)] for y in range(9)]
        self.thirdLayer = [[-1 for x in range(16)] for y in range(9)]

    def genMap(self, roomIndex):
        self.initMap()
        self.genFloors()
        self.genWalls()
        self.genBorders()
        self.fillWalls()
        

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_2.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.wallMap)

            file.close()

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_3.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.thirdLayer)

            file.close()

    def genWalls(self):
        for i in range(1, len(self.wallMap) - 1):
            for j in range(1, len(self.wallMap[0]) - 1):
                if(self.floorMap[i][j] != "-1"):
                    if(self.floorMap[i + 1][j] == "-1" and (self.wallMap[i + 1][j] == -1 or self.wallMap[i + 1][j] == 13) and self.wallMap[i + 1][j] == -1):
                        self.wallMap[i + 1][j] = 13
                    if(self.floorMap[i - 1][j] == "-1" and (self.wallMap[i - 1][j] == -1 or self.wallMap[i - 1][j] == 13) and self.wallMap[i - 1][j] == -1):
                        self.wallMap[i - 1][j] = 14

    def genBorders(self):

        for i in range(1, len(self.wallMap) - 1):
            for j in range(1, len(self.wallMap[0]) - 1):
                if(self.floorMap[i][j] != "-1" or self.wallMap[i][j] == 14):
                    self.checkAdjacent(i, j)
        

    def checkAdjacent(self, i, j):
        top = False
        topright = False
        topleft = False
        right = False
        left = False
        bottom = False
        bottomleft = False
        bottomright = False

        if(self.floorMap[i][j - 1] == "-1" and self.wallMap[i][j - 1] != 14 and (self.wallMap[i][j - 1] == -1 or self.wallMap[i][j - 1] == 13)):
            left = True
        if(self.floorMap[i][j + 1] == "-1" and self.wallMap[i][j + 1] != 14 and (self.wallMap[i][j + 1] == -1 or self.wallMap[i][j + 1] == 13)):
            right = True
        if(self.floorMap[i + 1][j] == "-1" and self.wallMap[i + 1][j] != 14 and (self.wallMap[i + 1][j] == -1 or self.wallMap[i + 1][j] == 13)):
            bottom = True
        if(self.floorMap[i - 1][j] == "-1" and self.wallMap[i - 1][j] != 14 and (self.wallMap[i - 1][j] == -1 or self.wallMap[i - 1][j] == 13)):
            top = True
        if(self.floorMap[i + 1][j - 1] == "-1" and self.wallMap[i + 1][j - 1] != 14 and (self.wallMap[i + 1][j - 1] == -1 or self.wallMap[i + 1][j - 1] == 13)):
            bottomleft = True
        if(self.floorMap[i + 1][j + 1] == "-1" and self.wallMap[i + 1][j + 1] != 14 and (self.wallMap[i + 1][j + 1] == -1 or self.wallMap[i + 1][j + 1] == 13)):
            bottomright = True
        if(self.floorMap[i - 1][j + 1] == "-1" and self.wallMap[i - 1][j + 1] != 14 and (self.wallMap[i - 1][j + 1] == -1 or self.wallMap[i - 1][j + 1] == 13)):
            topright = True
        if(self.floorMap[i - 1][j - 1] == "-1" and self.wallMap[i - 1][j - 1] != 14 and (self.wallMap[i - 1][j - 1] == -1 or self.wallMap[i - 1][j - 1] == 13)):
            topleft = True

        
        #i is y, j is x

        
        if(self.floorMap[i][j] != '-1' or self.wallMap[i][j] == 14):
            #if(bottom and self.wallMap[i + 1][j] == -1):
                #self.wallMap[i + 1][j] = 13
            #if(top and self.wallMap[i - 1][j] == -1):
                #self.wallMap[i - 1][j] = 14
    
            if(right):
                if(bottom):
                    if(top):
                        if(left):
                            self.thirdLayer[i][j] = -1
                        else:
                            self.thirdLayer[i][j] = 33 #three_sides_right
                    elif(left):
                        self.thirdLayer[i][j] = 35 #three_sides_bottom
                    else:
                        self.thirdLayer[i][j] = 20 #wall_inner_corner_l_top_right, bottom right L corner
                elif(top):
                    if(left):
                        self.thirdLayer[i][j] = 34 #three sides top
                    else:
                        if(bottomleft):
                            self.thirdLayer[i][j] = -1 # CHANGE THIS VALUE
                        else:
                            self.thirdLayer[i][j] = 31 #wall_corner_top_right_1 top right L corner
                elif(left):
                    self.thirdLayer[i][j] = 36 #two_sides_left_right
                else:
                    self.thirdLayer[i][j] = 17 #wall_side_mid_left right wall
            elif(left):
                if(bottom):
                    if(top):
                        self.thirdLayer[i][j] = 32 #three_sides_left
                    else:
                        self.thirdLayer[i][j] = 28 #wall_corner_bottom_left left bottom L corner
                elif(top):
                    self.thirdLayer[i][j] = 30 #wall_corner_top_left_1 top left L corner
                    #self.thirdLayer[i][j] = 18
                else:
                    self.thirdLayer[i][j] = 18 #wall_side_mid_right left wall
            elif(top):
                if(bottom):
                    self.thirdLayer[i][j] = 37 #two_sides_top_bottom
                else:
                    self.thirdLayer[i][j] = 16 #wall_top_mid2 top wall
            elif(bottom):
                self.thirdLayer[i][j] = 15 #wall_top_mid bottom wall
            elif(topright):
                self.thirdLayer[i][j] = 41 #top_right_corner dot corner
            elif(topleft):
                self.thirdLayer[i][j] = 40 #top_left_corner dot corner
            elif(bottomright):
                self.thirdLayer[i][j] = 39 #wall_side_top_left bottom right dot corner
            elif(bottomleft):
                self.thirdLayer[i][j] = 38 #wall_side_top_right bottom left dot corner

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
                            holeCount += 1 # Can never enter this loop again
                        
                        self.wallMap[i][j] = genID

    def __isHole__(self, i, j):
        if (self.floorMap[i][j] == '-1'):
            if (self.floorMap[i-1][j] != '-1') and (self.floorMap[i+1][j] != '-1') and (self.floorMap[i][j-1] != '-1') and (self.floorMap[i][j+1] != '-1'):
                return True
        
        return False


    def fillWalls(self):
        if self.wallMap[0][0] != -1:
            if self.wallMap[0][1] == -1:
                self.thirdLayer[0][0] = 34 #three sides top
            else:
                self.thirdLayer[0][0] = 30 #wall_corner_top_left_1 top left L corner
        if self.wallMap[0][15] != -1:
            if self.wallMap[0][14] == -1:
                self.thirdLayer[0][15] = 34 #three sides top
            else:
                self.thirdLayer[0][15] = 31 #wall_corner_top_right_1 top right L corner

        for j in range(1, len(self.wallMap[0]) - 1):
            left = False
            right = False
            if(self.wallMap[0][j] != -1):
                if(self.wallMap[0][j + 1] == -1):
                    right = True
                if(self.wallMap[0][j - 1] == -1):
                    left = True
                if(right):
                    if(left):
                        self.thirdLayer[0][j] = 34 #three sides top
                    else:
                        self.thirdLayer[0][j] = 31 #wall_corner_top_right_1 top right L corner
                elif(left):
                    self.thirdLayer[0][j] = 30 #wall_corner_top_left_1 top left L corner
                else:
                    self.thirdLayer[0][j] = 16 #wall_top_mid2 top wall
        
        for i in range(0, len(self.wallMap)):
            for j in range(0, len(self.wallMap[0])):
                if(self.floorMap[i][j] == "-1" and self.wallMap[i][j] == -1):
                    self.wallMap[i][j] = 42 #black tile

#right self.floorMap[i + 1][j]
#left  self.floorMap[i - 1][j]
#top self.floorMap[i][j - 1]
#bottom self.floorMap[i][j + 1]

#topright self.floorMap[i + 1][j - 1]
#topleft self.floorMap[i - 1][j - 1]
#bottomright self.floorMap[i + 1][j + 1]
#bottomleft self.floorMap[i - 1][j + 1]



        
        

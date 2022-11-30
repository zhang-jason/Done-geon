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
    def __init__(self, floorMap, roomIndex, numRooms):
        self.floorMap = floorMap
        self.wallMap = []
        self.thirdLayer = []
        self.genMap(roomIndex, numRooms)
        

    def initMap(self):
        self.wallMap = [[-1 for x in range(16)] for y in range(9)]
        self.thirdLayer = [[-1 for x in range(16)] for y in range(9)]

    def genMap(self, roomIndex, numRooms):
        self.initMap()
        self.genFloors()
        self.genWalls()
        self.genBorders()
        self.fillWalls()
        self.genDoors(roomIndex, numRooms)
        

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_2.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.wallMap)

            file.close()

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_3.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.thirdLayer)

            file.close()

    def genWalls(self):
        for i in range(len(self.wallMap) - 1, 0, -1):
            for j in range(1, len(self.wallMap[0]) - 1):
                if(self.floorMap[i][j] != "-1"):
                    if(self.floorMap[i - 1][j] == "-1" and self.wallMap[i - 1][j] == -1):
                        if(i > 1):
                            if(self.floorMap[i - 2][j] == "-1" and self.wallMap[i - 1][j] == -1):
                                self.wallMap[i - 1][j] = 14
                            else:
                                self.wallMap[i - 1][j] = 13
                        else:
                            self.wallMap[i - 1][j] = 14
                    if(self.floorMap[i + 1][j] == "-1" and self.wallMap[i + 1][j] == -1):
                        self.wallMap[i + 1][j] = 13

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
                        if(topleft):
                            self.thirdLayer[i][j] = 43 #bottom_right_corner_with_corner, bottom right L corner and topleft corner
                        else:
                            self.thirdLayer[i][j] = 20 #wall_inner_corner_l_top_right, bottom right L corner
                elif(top):
                    if(left):
                        self.thirdLayer[i][j] = 34 #three sides top
                    else:
                        if(bottomleft):
                            self.thirdLayer[i][j] = 45 #top_right_corner_with_corner top right L corner and bottomleft corner
                        else:
                            self.thirdLayer[i][j] = 31 #wall_corner_top_right_1 top right L corner
                elif(left):
                    self.thirdLayer[i][j] = 36 #two_sides_left_right
                else:
                    if(topleft):
                        if(bottomleft):
                            self.thirdLayer[i][j] = 59 #rightwall_bottomleft_topleft_corners right wall with both left corners
                        else:
                            self.thirdLayer[i][j] = 60 #rightwall_topleft_corner right wall with topleft corner
                    elif(bottomleft):
                        self.thirdLayer[i][j] = 58 #rightwall_bottomleft_corner right wall with bottomleft corner
                    else:
                        self.thirdLayer[i][j] = 17 #wall_side_mid_left right wall
            elif(left):
                if(bottom):
                    if(top):
                        self.thirdLayer[i][j] = 32 #three_sides_left
                    else:
                        if(topright):
                            self.thirdLayer[i][j] = 44 #bottom_left_corner_with_corner left bottom L corner and topright corner
                        else:
                            self.thirdLayer[i][j] = 28 #wall_corner_bottom_left left bottom L corner
                elif(top):
                    if(bottomright):
                        self.thirdLayer[i][j] = 46 #top_left_corner_with_corner top left L corner and bottom right corner
                    else:
                        self.thirdLayer[i][j] = 30 #wall_corner_top_left_1 top left L corner
                else:
                    if(topright):
                        if(bottomright):
                            self.thirdLayer[i][j] = 62 #leftwall_bottomright_topright_corners left wall with both right corners
                        else:
                            self.thirdLayer[i][j] = 63 #leftwall_topright_corner left wall with topright corner
                    elif(bottomright):
                        self.thirdLayer[i][j] = 61 #leftwall_bottomright_corner left wall with bottomright corner
                    else:
                        self.thirdLayer[i][j] = 18 #wall_side_mid_right left wall
            elif(top):
                if(bottom):
                    self.thirdLayer[i][j] = 37 #two_sides_top_bottom
                else:
                    if(bottomleft):
                        if(bottomright):
                            self.thirdLayer[i][j] = 65 #topwall_bottomright_bottomleft_corners top wall both bottom corners
                        else:
                            self.thirdLayer[i][j] = 64 #topwall_bottomleft_corner top wall and bottomleft corner
                    elif(bottomright):
                        self.thirdLayer[i][j] = 66 #topwall_bottomright_corner top wall and bottomright corner
                    else:
                        self.thirdLayer[i][j] = 16 #wall_top_mid2 top wall
            elif(bottom):
                if(topleft):
                    if(topright):
                        self.thirdLayer[i][j] = 68 #bottomwall_topleft_topright_corners bottom wall and both top corners
                    else:
                        self.thirdLayer[i][j] = 67 #bottomwall_topleft_corner bottom wall and topleft corner
                elif(topright):
                    self.thirdLayer[i][j] = 69 #bottomwall_topright_corner bottom wall and topright corner
                else:
                    self.thirdLayer[i][j] = 15 #wall_top_mid bottom wall
            elif(topright):
                if(topleft):
                    if(bottomright):
                        if(bottomleft):
                            self.thirdLayer[i][j] = 54 #four_corners
                        else:
                            self.thirdLayer[i][j] = 52 #bottomright_topleft_topright_corners
                    elif(bottomleft):
                        self.thirdLayer[i][j] = 48 #bottomleft_topleft_topright_corners
                    else:
                        self.thirdLayer[i][j] = 55 #topright, topleft
                elif(bottomright):
                    if(bottomleft):
                        self.thirdLayer[i][j] = 50 #bottomright_bottomleft_topright_corners
                    else:
                        self.thirdLayer[i][j] = 53 #bottomright_topright_corners
                elif(bottomleft):
                    self.thirdLayer[i][j] = 56 #topright, bottomleft
                else:
                    self.thirdLayer[i][j] = 41 #top_right_corner dot corner
            elif(topleft):
                if(bottomright):
                    if(bottomleft):
                        self.thirdLayer[i][j] = 49 #bottomright_bottomleft_topleft_corners
                    else:
                        self.thirdLayer[i][j] = 51 #bottomright_topleft_corners
                elif(bottomleft):
                    self.thirdLayer[i][j] = 57 #topleft, bottomleft
                else:
                    self.thirdLayer[i][j] = 40 #top_left_corner dot corner
            elif(bottomright):
                if(bottomleft):
                    self.thirdLayer[i][j] = 47 #bottomleft_bottomright_corners
                else:
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
                        
                        self.thirdLayer[i][j] = genID
                        self.floorMap[i][j] = 1

    def __isHole__(self, i, j):
        if (self.floorMap[i][j] == '-1'):
            if (self.floorMap[i-1][j] != '-1') and (self.floorMap[i+1][j] != '-1') and (self.floorMap[i][j-1] != '-1') and (self.floorMap[i][j+1] != '-1'):
                if(self.floorMap[i-1][j-1] != '-1' and self.floorMap[i-1][j+1] != '-1' and self.floorMap[i+1][j-1] != '-1' and self.floorMap[i+1][j+1] != '-1'):
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
                    self.wallMap[i][j] = 42 #black tile collidable


    def genDoors(self, roomIndex, num):
        flag = True
        flag2 = True
        if(roomIndex == 0):
            flag = False
        if(roomIndex == num):
            flag2 = False
        while(flag):
            i = randint(0, 8) #actually y 
            j = randint(1, 13) #actually x
            if(self.wallMap[i][j] == 13) and (self.wallMap[i][j - 1] == 13 or self.wallMap[i][j + 1] == 13):
                self.wallMap[i][j] = 71
                flag = False
        while(flag2):
            i = randint(0, 8)
            j = randint(1, 14)
            if(self.wallMap[i][j] == 14) and (self.wallMap[i][j - 1] == 14 or self.wallMap[i][j + 1] == 14) and (self.thirdLayer[i][j] == -1 or self.thirdLayer[i][j] == 16):
                if(i == 0):
                    if(j > 4 and j < 12):
                        self.wallMap[i][j] = 70
                        flag2 = False
                        #print('should be in between')
                        #print(roomIndex)
                        #print(i)
                        #print(j)
                else:
                    self.wallMap[i][j] = 70
                    flag2 = False
            

#right self.floorMap[i + 1][j]
#left  self.floorMap[i - 1][j]
#top self.floorMap[i][j - 1]
#bottom self.floorMap[i][j + 1]

#topright self.floorMap[i + 1][j - 1]
#topleft self.floorMap[i - 1][j - 1]
#bottomright self.floorMap[i + 1][j + 1]
#bottomleft self.floorMap[i - 1][j + 1]

#len(self.wallMap) = 9
#len(self.wallMap[0]) = 16



        
        

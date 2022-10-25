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
        self.genMap(roomIndex)

    def initMap(self):
        self.wallMap = [[-1 for x in range(16)] for y in range(9)]

    def genMap(self, roomIndex):
        self.initMap()
        self.genWalls(self)
        self.genFloors(self)

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_2.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.wallMap)

            file.close()

    def genWalls(self):
        '''
        for i in range(9):
            if self.floorMap[i][1] != "-1":
                self.wallMap[i][0] = 17
            if self.floorMap[i][14] != "-1":
                self.wallMap[i][15] = 18
        for i in range(16):
            if self.floorMap[1][i] != "-1":
                self.wallMap[0][i] = 13
            if self.floorMap[7][i] != "-1":
                self.wallMap[8][i] = 13
        '''
        
        print(self.floorMap)
        #for i in range(1, len(self.wallMap) - 1):
        #    for j in range(1, len(self.wallMap[0]) - 1):
        #        if(self.floorMap[i][j] == "-1"):
        #            self.checkAdjacent(self.floorMap, self.wallMap, i, j)

        for i in range(1, len(self.wallMap) - 1):
            for j in range(1, len(self.wallMap[0]) - 1):
                if(self.floorMap[i][j] != "-1"):
                    self.checkAdjacent(self.floorMap, self.wallMap, i, j)
        
        
        '''
        for i in range(1, len(self.floorMap)):
            for j in range(len(self.floorMap[0])):
                if self.floorMap[i][j] == 1:
                    adjacent = self.checkAdjacent(self.floorMap, self.wallMap, i, j)
        '''

    def checkAdjacent(self, i, j):
        top = False
        topright = False
        topleft = False
        right = False
        left = False
        bottom = False
        bottomleft = False
        bottomright = False

        if(self.floorMap[i][j - 1] == '-1'):
            left = True
            print("left " + self.floorMap[i][j - 1])
        if(self.floorMap[i][j + 1] == '-1'):
            right = True
            print("right " + self.floorMap[i][j + 1])
        if(self.floorMap[i + 1][j] == "-1"):
            bottom = True
            print("bottom " + self.floorMap[i + 1][j])
        if(self.floorMap[i - 1][j] == "-1"):
            top = True
            print("top " + self.floorMap[i - 1][j])
        if(self.floorMap[i + 1][j - 1] == "-1"):
            bottomleft = True
            print("bottomleft " + self.floorMap[i + 1][j - 1])
        if(self.floorMap[i + 1][j + 1] == "-1"):
            bottomright = True
            print("bottomright " + self.floorMap[i + 1][j + 1])
        if(self.floorMap[i - 1][j + 1] == "-1"):
            topright = True
            print("topright " + self.floorMap[i - 1][j + 1])
        if(self.floorMap[i - 1][j - 1] == "-1"):
            topleft = True
            print("topleft " + self.floorMap[i - 1][j - 1])

        
        #i is y, j is x

        if(self.floorMap[i][j] != '-1'):
            #if(top == False and self.wallMap[i - 1][j] == -1):
                #self.wallMap[i - 1][j] = 13
            #if(bottom == False and self.wallMap[i + 1][j] == -1):
                #self.wallMap[i + 1][j] = 13
            #if(left == False and self.wallMap[i][j - 1] == -1):
                #self.wallMap[i][j - 1] = 17
            #if(right == False and self.wallMap[i][j + 1] == -1):
                #self.wallMap[i][j + 1] = 18
            '''
            if(left == False):
                if(bottom == False):
                    if(not top):
                        self.wallMap[i][j] = 11
                    elif(not right):
                        self.wallMap[i][j] = 10
                    else:
                        self.wallMap[i][j] = 28
                elif(not top):
                    self.wallMap[i][j] = 30
                else:
                    self.wallMap[i][j] = 18
            if(not right):
                if(not bottom):
                    if(not top):
                        self.wallMap[i][j] = 9
                    elif(not left):
                        self.wallMap[i][j] = 12
                    else:
                        self.wallMap[i][j] = 29
                elif(not top):
                    self.wallMap[i][j] = 31
                else:
                    self.wallMap[i][j] = 19
        #else:
            #if(bottom):
                #if(top):
                    #if(right or left):
                        #self.floorMap[i][j] = 1
            '''
            if(right):
                if(bottom):
                    if(top):
                        if(left):
                            self.wallMap[i][j] = -1
                        else:
                            self.wallMap[i][j] = 33
                    elif(left):
                        self.wallMap[i][j] = 35
                    else:
                        self.wallMap[i][j] = 20
                elif(top):
                    if(left):
                        self.wallMap[i][j] = 34
                    else:
                        self.wallMap[i][j] = 31
                elif(left):
                    self.wallMap[i][j] = 36
                else:
                    self.wallMap[i][j] = 17
            elif(left):
                if(bottom):
                    if(top):
                        self.wallMap[i][j] = 32
                    else:
                        self.wallMap[i][j] = 28
                elif(top):
                    self.wallMap[i][j] = 30
                else:
                    self.wallMap[i][j] = 18
            elif(top):
                if(bottom):
                    self.wallMap[i][j] = 37
                else:
                    self.wallMap[i][j] = 16
            elif(bottom):
                self.wallMap[i][j] = 15

        '''
        if(self.floorMap[i + 1][j] != "-1" and self.floorMap[i - 1][j] != "-1" and self.floorMap[i][j + 1] != "-1" and self.floorMap[i][j - 1] != "-1"):
            return
        if(self.floorMap[i + 1][j] == "-1"): #right is empty
            if(self.floorMap[i][j + 1] == "-1"): # bottom is empty
                self.wallMap[i +1][j] = 11
            elif(self.floorMap[i][j - 1] == "-1"): #top is empty
                if(self.floorMap[i + 1][j - 1] == "-1"): #topright is empty
                    self.wallMap[i +1][j - 1] = 11
                else:
                    self.wallMap[i][j - 1] = 18
                self.wallMap[i + 1][j] = 19
            else: 
                self.wallMap[i + 1][j] = 11
        if(self.floorMap[i - 1][j] == "-1"): #left is empty
            if(self.floorMap[i][j + 1] == "-1"): # bottom is empty
                self.wallMap[i +1][j] = 16
            elif(self.floorMap[i][j - 1] == "-1"): #top is empty
                if(self.floorMap[i - 1][j - 1] == "-1"): #topleft is empty
                    self.wallMap[i +1][j - 1] = 17
                else:
                    self.wallMap[i][j - 1] = 18
                self.wallMap[i + 1][j] = 19
            else: 
                self.wallMap[i + 1][j] = 10

            '''

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
#right self.floorMap[i + 1][j]
#left  self.floorMap[i - 1][j]
#top self.floorMap[i][j - 1]
#bottom self.floorMap[i][j + 1]

#topright self.floorMap[i + 1][j - 1]
#topleft self.floorMap[i - 1][j - 1]
#bottomright self.floorMap[i + 1][j + 1]
#bottomleft self.floorMap[i - 1][j + 1]



        
        

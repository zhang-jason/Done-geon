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
        wallMap = [[-1 for x in range(16)] for y in range(9)]
        '''
        for i in range(9):
            if floorMap[i][1] != "-1":
                wallMap[i][0] = 17
            if floorMap[i][14] != "-1":
                wallMap[i][15] = 18
        for i in range(16):
            if floorMap[1][i] != "-1":
                wallMap[0][i] = 13
            if floorMap[7][i] != "-1":
                wallMap[8][i] = 13
        '''
        
        print(floorMap)
        #for i in range(1, len(wallMap) - 1):
        #    for j in range(1, len(wallMap[0]) - 1):
        #        if(floorMap[i][j] == "-1"):
        #            self.checkAdjacent(floorMap, wallMap, i, j)

        for i in range(1, len(wallMap) - 1):
            for j in range(1, len(wallMap[0]) - 1):
                if(floorMap[i][j] != "-1"):
                    self.checkAdjacent(floorMap, wallMap, i, j)
        
        
        '''
        for i in range(1, len(floorMap)):
            for j in range(len(floorMap[0])):
                if floorMap[i][j] == 1:
                    adjacent = self.checkAdjacent(floorMap, wallMap, i, j)
        '''

        with open(os.path.join(os.path.dirname(__file__), '..', 'assets/tiles/temprooms', f'room{roomIndex}_2.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(wallMap)

            file.close()

    def checkAdjacent(self, floorMap, wallMap, i, j):
        top = False
        topright = False
        topleft = False
        right = False
        left = False
        bottom = False
        bottomleft = False
        bottomright = False

        if(floorMap[i][j - 1] == '-1'):
            left = True
            print("left " + floorMap[i][j - 1])
        if(floorMap[i][j + 1] == '-1'):
            right = True
            print("right " + floorMap[i][j + 1])
        if(floorMap[i + 1][j] == "-1"):
            bottom = True
            print("bottom " + floorMap[i + 1][j])
        if(floorMap[i - 1][j] == "-1"):
            top = True
            print("top " + floorMap[i - 1][j])
        if(floorMap[i + 1][j - 1] == "-1"):
            bottomleft = True
            print("bottomleft " + floorMap[i + 1][j - 1])
        if(floorMap[i + 1][j + 1] == "-1"):
            bottomright = True
            print("bottomright " + floorMap[i + 1][j + 1])
        if(floorMap[i - 1][j + 1] == "-1"):
            topright = True
            print("topright " + floorMap[i - 1][j + 1])
        if(floorMap[i - 1][j - 1] == "-1"):
            topleft = True
            print("topleft " + floorMap[i - 1][j - 1])

        
        #i is y, j is x

        if(floorMap[i][j] != '-1'):
            #if(top == False and wallMap[i - 1][j] == -1):
                #wallMap[i - 1][j] = 13
            #if(bottom == False and wallMap[i + 1][j] == -1):
                #wallMap[i + 1][j] = 13
            #if(left == False and wallMap[i][j - 1] == -1):
                #wallMap[i][j - 1] = 17
            #if(right == False and wallMap[i][j + 1] == -1):
                #wallMap[i][j + 1] = 18
            '''
            if(left == False):
                if(bottom == False):
                    if(not top):
                        wallMap[i][j] = 11
                    elif(not right):
                        wallMap[i][j] = 10
                    else:
                        wallMap[i][j] = 28
                elif(not top):
                    wallMap[i][j] = 30
                else:
                    wallMap[i][j] = 18
            if(not right):
                if(not bottom):
                    if(not top):
                        wallMap[i][j] = 9
                    elif(not left):
                        wallMap[i][j] = 12
                    else:
                        wallMap[i][j] = 29
                elif(not top):
                    wallMap[i][j] = 31
                else:
                    wallMap[i][j] = 19
        #else:
            #if(bottom):
                #if(top):
                    #if(right or left):
                        #floorMap[i][j] = 1
            '''
            if(right):
                if(bottom):
                    if(top):
                        if(left):
                            wallMap[i][j] = -1
                        else:
                            wallMap[i][j] = 33
                    elif(left):
                        wallMap[i][j] = 35
                    else:
                        wallMap[i][j] = 20
                elif(top):
                    if(left):
                        wallMap[i][j] = 34
                    else:
                        wallMap[i][j] = 31
                elif(left):
                    wallMap[i][j] = 36
                else:
                    wallMap[i][j] = 17
            elif(left):
                if(bottom):
                    if(top):
                        wallMap[i][j] = 32
                    else:
                        wallMap[i][j] = 28
                elif(top):
                    wallMap[i][j] = 30
                else:
                    wallMap[i][j] = 18
            elif(top):
                if(bottom):
                    wallMap[i][j] = 37
                else:
                    wallMap[i][j] = 16
            elif(bottom):
                wallMap[i][j] = 15

        '''
        if(floorMap[i + 1][j] != "-1" and floorMap[i - 1][j] != "-1" and floorMap[i][j + 1] != "-1" and floorMap[i][j - 1] != "-1"):
            return
        if(floorMap[i + 1][j] == "-1"): #right is empty
            if(floorMap[i][j + 1] == "-1"): # bottom is empty
                wallMap[i +1][j] = 11
            elif(floorMap[i][j - 1] == "-1"): #top is empty
                if(floorMap[i + 1][j - 1] == "-1"): #topright is empty
                    wallMap[i +1][j - 1] = 11
                else:
                    wallMap[i][j - 1] = 18
                wallMap[i + 1][j] = 19
            else: 
                wallMap[i + 1][j] = 11
        if(floorMap[i - 1][j] == "-1"): #left is empty
            if(floorMap[i][j + 1] == "-1"): # bottom is empty
                wallMap[i +1][j] = 16
            elif(floorMap[i][j - 1] == "-1"): #top is empty
                if(floorMap[i - 1][j - 1] == "-1"): #topleft is empty
                    wallMap[i +1][j - 1] = 17
                else:
                    wallMap[i][j - 1] = 18
                wallMap[i + 1][j] = 19
            else: 
                wallMap[i + 1][j] = 10

            '''
#right floorMap[i + 1][j]
#left  floorMap[i - 1][j]
#top floorMap[i][j - 1]
#bottom floorMap[i][j + 1]

#topright floorMap[i + 1][j - 1]
#topleft floorMap[i - 1][j - 1]
#bottomright floorMap[i + 1][j + 1]
#bottomleft floorMap[i - 1][j + 1]



        
        

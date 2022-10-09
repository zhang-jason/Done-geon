import csv
import os
from random import randint

class RoomGen():
    def __init__(self, roomType, roomIndex, width, height):
        self.rows = height
        self.columns = width
        self.roomType = roomType

        match(roomType):
            case 'dungeon':
                self.genDungeon(roomIndex)
    
    def genDungeon(self, roomIndex):
        #self.genDungeonBg()

        file = open(os.path.join(os.path.dirname(__file__), 'assets/tiles/temprooms', f'room{roomIndex}.csv'), 'w', newline='')
        writer = csv.writer(file)

        for n in range(self.rows):
            currentRow = []
            for n in range(self.columns):
                currentRow.append(randint(1,19))
            print(currentRow)
            writer.writerow(currentRow)

        file.close()

    def genDungeonBg(self, roomIndex):
        file = open(f'tempRooms/room{roomIndex}_bg')
        writer = csv.writer(file)
        
        with open(f'tempRooms/room{roomIndex}_bg', 'w', newline='') as file:
            writer = csv.writer(file)

            for n in range(self.rows - 1):
                currentRow = []
                for n in range(self.columns - 1):
                    currentRow.append(randint(1,19))
                writer.writerow(currentRow)

            file.close()

    



import pygame
from os import listdir, rename
from os.path import join, dirname, isfile

def getDirCount(dir):
    count = 0
    for path in listdir(dir):
        if isfile(join(dir, path)):
            count += 1

    return count

def getImages(dir, scale):
    spriteList = []
    for path in listdir(dir):
        file = join(dir, path)
        if isfile(file):
            image = pygame.transform.scale(pygame.image.load(
                file), scale)
            spriteList.append(image)

    trans_image = pygame.image.load(join(dir, '0.png'))
    trans_color = trans_image.get_at((0, 0))
    for x in spriteList:
        x.set_colorkey(trans_color)

    return spriteList

# For when GetImages goes bonkers
def __getSprites__(type, status, size):
    spriteList = []

    dirPath = join(dirname(dirname(__file__)), f'game/assets/{type}/{status}')
    for i, file in enumerate(listdir(dirPath)):
        f = join(dirPath, f'{i}.png')
        if isfile(f):
            spriteList.append(pygame.transform.scale(pygame.image.load(f), size))

    trans_image = pygame.image.load(join(dirPath, '0.png'))
    trans_color = trans_image.get_at((0, 0))
    for x in spriteList:
        x.set_colorkey(trans_color)

    return spriteList

# Let's you easily rename files to match the input required for sprites
def main():
    dir = input('Input Directory:')
    for count, filename in enumerate(listdir(dir)):
        dst = f'{str(count)}.png'
        src = f'{dir}/{filename}'
        dst = f'{dir}/{dst}'

        rename(src,dst)

if __name__ == "__main__":
    main()
    print('Success')
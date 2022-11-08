from os import listdir, rename

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
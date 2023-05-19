import pygame

SPRITE_PATH = 'sprites/'
FILE_EXTENSION = '.png'

def load_sprites(name:str) -> list[pygame.Surface]:
    res = list[pygame.Surface]()
    try:
        res.append(pygame.image.load(SPRITE_PATH + name + FILE_EXTENSION))
    except FileNotFoundError:
        while True:
            i = 0
            try:
                res.append(pygame.image.load(SPRITE_PATH + name + '_' + str(i) + FILE_EXTENSION))
                i += 1
            except FileNotFoundError:
                break

    if len(res) == 0:
        raise FileNotFoundError

    return res
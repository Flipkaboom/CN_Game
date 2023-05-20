import pygame

pygame.init()

SPRITE_PATH = 'sprites/'
FILE_EXTENSION = '.png'

def load_sprites(name:str) -> list[pygame.Surface]:
    res = list[pygame.Surface]()
    try:
        res.append(pygame.image.load(SPRITE_PATH + name + FILE_EXTENSION).convert_alpha())
    except FileNotFoundError:
        i = 0
        while True:
            try:
                res.append(pygame.image.load(SPRITE_PATH + name + '_' + str(i) + FILE_EXTENSION).convert_alpha())
                i += 1
            except FileNotFoundError:
                break

    if len(res) == 0:
        raise FileNotFoundError(name)

    return res
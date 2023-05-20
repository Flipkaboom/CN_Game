import pygame

from Entities import animation

import os

os.chdir('../')

pygame.init()
clock = pygame.time.Clock()
running = True

a = animation.Animation('host_button', loop=True, alterable=True)
a.restore_unaltered()
a.reset()
print('a')
a.update()
print('b')

pygame.quit()
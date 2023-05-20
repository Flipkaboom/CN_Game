import pygame

import user_input
import instance as inst


def handle_pygame_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            inst.screen_closed = True

        if e.type == pygame.VIDEORESIZE:
            inst.renderer.update_screen_size()

        if e.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
                      pygame.TEXTINPUT, pygame.KEYDOWN]:
            user_input.handle_event(e)
import pygame

import game_input
import instance


def handle_pygame_events(inst:instance.Instance):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            inst.screen_closed = True

        if e.type == pygame.VIDEORESIZE:
            inst.renderer.update_screen_size()

        if e.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN]:
            game_input.handle_event(e)
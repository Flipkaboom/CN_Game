import pygame
import drawing


def handle_pygame_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kill_game = True
        if event.type == pygame.VIDEORESIZE:
            drawing.update_screen_size()
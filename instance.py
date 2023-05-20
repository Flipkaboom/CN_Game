import time

import pygame

import drawing
import events
from States.game_state import GameState


state:GameState
screen_closed: bool
clock: pygame.time
name:str = 'UNSET'

renderer:drawing.Renderer

def initialize():
    global renderer, clock, state, screen_closed

    pygame.init()

    renderer = drawing.Renderer()

    pygame.display.set_caption("Don't forget to change this")
    clock = pygame.time.Clock()

    from States import main_menu
    state = main_menu.MainMenu()
    screen_closed = False

    start_loop()

def start_loop():
    global state, renderer, screen_closed
    time_start = time.time()
    frame_count = 0
    while not screen_closed:
        events.handle_pygame_events()

        #handle network incoming

        state.frame_logic()

        #send network outgoing

        renderer.render_canvas()

        frame_count += 1

        # clock.tick(60)

    time_total = time.time() - time_start
    print('Ran ', frame_count, ' frames in ', time_total, ' seconds.')
    print('Average ', frame_count / time_total, ' fps.')

    pygame.quit()

def change_state(new_state:GameState):
    global state
    state.stop()
    state = new_state
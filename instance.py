import pygame

class Instance:
    pass

import drawing
import events
import States

# noinspection PyRedeclaration
class Instance:
    state:States.GameState
    screen_closed: bool

    renderer:drawing.Renderer

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Don't forget to change this")
        self.clock = pygame.time.Clock()

        self.state = States.MainMenu(self)
        self.screen_closed:bool = False

        self.renderer = drawing.Renderer(self)

    def start_loop(self):
        while not self.screen_closed:
            events.handle_pygame_events(self)

            #handle network incoming

            self.state.frame_logic()

            #send network outgoing

            self.renderer.render_canvas()

            self.clock.tick(60)

        pygame.quit()

    def change_state(self, state:States.GameState):
        self.state.stop()
        self.state = state

global_instance: Instance

def initialize():
    global global_instance
    global_instance = Instance()
    global_instance.start_loop()

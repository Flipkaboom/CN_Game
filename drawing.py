import pygame

class Renderer:
    pass

import instance as inst

CANVAS_SIZE = (1920, 1080)


# noinspection PyRedeclaration
class Renderer:
    screen:pygame.Surface
    canvas:pygame.Surface

    hor_offset = 0
    vert_offset = 0
    scale_factor = 1

    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.canvas = pygame.Surface(CANVAS_SIZE)
        self.update_screen_size()

    def render_canvas(self):
        self.screen.fill('black')
        self.canvas.fill('pink')
        #start testing code
        # self.canvas.fill('pink')
        # self.canvas.fill('blue', pygame.Rect((200, 100), (100, 200)))
        #end testing code

        self.draw_all_entities()

        canvas_scaled = pygame.transform.smoothscale_by(self.canvas, self.scale_factor)
        #enable for fps boost
        # canvas_scaled = pygame.transform.scale_by(self.canvas, self.scale_factor)
        # canvas_scaled = self.canvas
        self.screen.blit(canvas_scaled, (self.hor_offset, self.vert_offset))

        pygame.display.flip()

    def draw_all_entities(self):
        for l in inst.state.layers.values():
            for e in l.entities:
                if e.visible:
                    self.canvas.blit(e.curr_anim.sprite, e.bbox)

    def update_screen_size(self):
        hor_scale_factor = self.screen.get_width() / CANVAS_SIZE[0]
        vert_scale_factor = self.screen.get_height() / CANVAS_SIZE[1]
        if hor_scale_factor < vert_scale_factor:
            self.scale_factor = hor_scale_factor
            proportional_height = self.scale_factor * CANVAS_SIZE[1]
            self.hor_offset = 0
            self.vert_offset = (self.screen.get_height() - proportional_height) / 2
        else:
            self.scale_factor = vert_scale_factor
            proportional_width = self.scale_factor * CANVAS_SIZE[0]
            self.vert_offset = 0
            self.hor_offset = (self.screen.get_width() - proportional_width) / 2
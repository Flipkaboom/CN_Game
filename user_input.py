import pygame

import instance as inst

text_input = str()

def mouse_canvas_pos():
    pos = pygame.mouse.get_pos()

    pos = (pos[0] - inst.renderer.hor_offset,
           pos[1] - inst.renderer.vert_offset)

    pos = (pos[0] * (1 / inst.renderer.scale_factor),
           pos[1] * (1 / inst.renderer.scale_factor))

    return pos

def handle_event(e:pygame.event.Event):
    global text_input

    if e.type == pygame.MOUSEMOTION:
        return

    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == 1:
            inst.state.mouse_event(mouse_canvas_pos(), True)

    if e.type == pygame.MOUSEBUTTONUP:
        if e.button == 1:
            inst.state.mouse_event(mouse_canvas_pos(), False)

    if e.type == pygame.TEXTINPUT:
        text_input += e.text

    if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_BACKSPACE:
            text_input = text_input[:-1]
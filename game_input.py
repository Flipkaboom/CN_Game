import pygame

import instance


def mouse_canvas_pos():
    pos = pygame.mouse.get_pos()

    pos = (pos[0] - instance.global_instance.renderer.hor_offset,
           pos[1] - instance.global_instance.renderer.vert_offset)

    pos = (pos[0] * (1 / instance.global_instance.renderer.scale_factor),
           pos[1] * (1 / instance.global_instance.renderer.scale_factor))

    return pos

def handle_event(e:pygame.event.Event):
    if e.type == pygame.MOUSEMOTION:
        return

    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == 1:
            instance.global_instance.state.mouse_event(mouse_canvas_pos(), True)

    if e.type == pygame.MOUSEBUTTONUP:
        if e.button == 1:
            instance.global_instance.state.mouse_event(mouse_canvas_pos(), False)
